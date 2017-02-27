$(document).ready(function() {
    var username = 'Gamer' + parseInt(Math.random() * 1000);
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/');

    socket.emit('lobby_get_rooms');

    socket.on('chat_send_to_user', function(message) {
        $("div.chat-text").append("User said: " + message.data + "<br />");
        return false;
    });

    socket.on('lobby_return_rooms', function(rooms) {
        console.log(rooms);
    });

    $('#chat-input-text').keypress(function(e) {
        if (e.which == '13') {
            if ($('#chat-input-text').val()) {
                socket.emit('chat_send_to_server', {'data': $('#chat-input-text').val()});
                $('#chat-input-text').val("");
            }
        }

    });

    $('#lobby-create-room').click(function(e) {
        socket.emit('lobby_create_room', {'creator': username});
        return false;
    });

});
