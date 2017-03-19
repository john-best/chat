from flask import Flask, render_template, json, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from RoomAPI import RoomHandler, Room
from werkzeug.security import generate_password_hash, check_password_hash

# setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatisthis'

socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

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
        self.password = password
        self.email = email

    def set_password(self , password):
        self.password = generate_password_hash(password)

    def check_password(self , password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


# routes
@app.route('/', methods=['GET'])
def lobby():
    return render_template('lobby.html')

@app.route('/rps', methods=['GET'])
def rps_room():
    return render_template('rps.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('lobby'))
    login_user(registered_user)
    flash('Logged in')
    return redirect(url_for('lobby'))

@app.route('/register', methods=['GET, POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
        
    user = User(request.form['username'], request.form['password'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User registered')
    return redirect(url_for('lobby'))

@app.route('/logout', methods=['POST'])
def logout():
    pass

# flask_login stuff



# begin chat

@socketio.on('chat_send_to_server', namespace='/')
def handle_chat_message(message):
    emit('chat_send_to_user', message, broadcast=True)

@socketio.on('connect', namespace='/')
def handle_chat_connect():
    pass

@socketio.on('disconnect', namespace='/')
def handle_chat_disconnect():
    pass

@socketio.on('chat_send_connected', namespace='/')
def handle_chat_connect_response(name):
    emit('chat_recv_user_connected', name, broadcast=True)

# end chat

# end rps event handling

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
