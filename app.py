from flask import Flask, render_template, json, request
from flask_socketio import SocketIO, emit, join_room, leave_room

from RoomAPI import RoomHandler, Room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatisthis'
socketio = SocketIO(app)
room_handler = RoomHandler()

@app.route('/', methods=['GET'])
def lobby():
    return render_template('lobby.html')

@app.route('/rps', methods=['GET'])
def rps_room():
    return render_template('rps.html')

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

# end chat
# begin rps event handling

@socketio.on('connect', namespace='/rps')
def handle_rps_connect():
    print('A user connected!')

@socketio.on('disconnect',  namespace='/rps')
def handle_rps_disconnect():
    print('A user has disconnected')

@socketio.on('rps_chat_send_to_server', namespace='/rps')
def handle_rps_chat_message(message):
    emit('rps_chat_send_to_user', message, broadcast=True)

@socketio.on('rps_server_update', namespace='/rps')
def handle_rps_server_update(server_update):
    emit('rps_user_update', server_update, broadcast=True)

# end rps event handling

# begin lobby / room handling
@socketio.on('lobby_create_room')
def handle_lobby_create_room(data):
    room = room_handler.create_room(data['creator'])
    join_room(room.get_id())
    emit('lobby_room_created', {'data': 'ayylmao'})

@socketio.on('lobby_get_rooms')
def handle_lobby_get_rooms():
    rooms = room_handler.get_room_ids()
    rooms_d = {}
    rooms_d["rooms"] = rooms 
    emit('lobby_return_rooms', json.dumps(rooms_d))

if __name__ == '__main__':
    socketio.run(app)
