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
