from flask import Flask, render_template, json, request
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatisthis'
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('rps.html')



@socketio.on('connect', namespace='/')
def handle_rps_connect():
    print('A user connected!')

@socketio.on('disconnect',  namespace='/')
def handle_rps_disconnect():
    print('A user has disconnected')


# begin rps event handling

@socketio.on('rps_server_update', namespace='/')
def handle_rps_server_update(server_update):
    emit('rps_user_update', server_update, broadcast=True)

# end rps event handling

# begin chat

@socketio.on('chat_send_to_server', namespace='/')
def handle_chat_message(message):
    emit('chat_send_to_user', message, broadcast=True)

# end chat
if __name__ == '__main__':
    socketio.run(app)
