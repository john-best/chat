from flask import Flask, render_template, json, request, flash, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_login import AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy 
from RoomAPI import RoomHandler, Room
from werkzeug.security import generate_password_hash, check_password_hash
import random

# setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatisthis'

socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

room_handler = RoomHandler()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rps.db'
db = SQLAlchemy(app)

# flask-login user class
class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(250))
    email = db.Column('email',db.String(50),unique=True , index=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = self.set_password(password)
        self.email = email

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


# flask anon user class
class AnonUser(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'

login_manager.anonymous_user = AnonUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# will create tables if not exist
db.create_all()
db.session.commit()

# routes
@app.route('/', methods=['GET'])
def lobby():
    return render_template('lobby.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user is not None and user.check_password(password):
        login_user(user, remember=True)
        flash('Successfully logged in.')
        return redirect(url_for('lobby'))
    else:
        flash('Invalid credentials.', 'error')
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    user = User(request.form['username'], request.form['password'], request.form['email'])

    user_exists = db.session.query(User.id).filter_by(username=request.form['username']).scalar() is not None
    email_exists = db.session.query(User.id).filter_by(email=request.form['email']).scalar() is not None

    if user_exists or email_exists:
        flash('Username or Email already taken', 'error')
        return redirect(url_for('register'))
    else:
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            flash('An internal server error has occured.', 'error')
            return redirect(url_for('register'))

        flash('You have successfully registered. Please login.')
        return redirect(url_for('lobby'))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('lobby'))

# begin chat

@socketio.on('chat_send_to_server', namespace='/')
def handle_chat_message(message):
    emit('chat_send_to_user', message, broadcast=True)

@socketio.on('connect', namespace='/')
def handle_chat_connect():
    emit('chat_self_connected', {'username':current_user.username})
    emit('chat_user_connected',
    {'message':'{} has connected'.format(current_user.username)}, broadcast=True, include_self=False)

@socketio.on('disconnect', namespace='/')
def handle_chat_disconnect():
    emit('chat_user_disconnected', {'message':'{} has disconnected'.format(current_user.username)}, broadcast=True)
    ghost_room = room_handler.get_room_by_owner(current_user.username)
    if ghost_room is not None:
        room_handler.delete_room(ghost_room)

# end chat

# begin lobby / room handling
@socketio.on('lobby_create_room')
def handle_lobby_create_room(data):
    if not room_handler.room_check_exists(data['creator']):
        room = room_handler.create_room(data['creator'], data['password'])
        room_json = room_handler.get_room_json(room)
        join_room(room.get_id())
        emit('lobby_room_created', json.dumps(room_json))
    else:
        emit('lobby_room_already_exists')

@socketio.on('lobby_get_rooms')
def handle_lobby_get_rooms():
    rooms = room_handler.get_rooms_json()
    emit('lobby_return_rooms', json.dumps(rooms))

@socketio.on('lobby_delete_room')
def handle_lobby_delete_room(data):
    deleted = None
    room = room_handler.get_room(data['id'])
    
    if room is None:
        emit('lobby_room_does_not_exist')
        return

    if room.get_owner() == data['user']:
        deleted = room_handler.delete_room(room)

    if deleted is not None:
        emit('lobby_room_deleted_by_owner')
    else:
        emit('lobby_room_fail_delete')

if __name__ == '__main__':
    socketio.run(app)
