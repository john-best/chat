from flask import Flask, render_template, json, request
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatisthis'
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('rps.html')

# begin socketio stuff
@socketio.on('server_update', namespace='/rps')
def handle_server_update(server_update):
    print('Successful rps recv')
    emit('user_update', {'data': 'HELP ME'}, broadcast=True)

@socketio.on('connect', namespace='/rps')
def handle_connect():
    print('A user connected!')

if __name__ == '__main__':
    socketio.run(app)
