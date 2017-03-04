$(document).ready(function() {
    var username = 'Gamer' + parseInt(Math.random() * 1000);
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/');

    socket.emit('lobby_get_rooms');

    socket.on('chat_send_to_user', function(message) {
        $("div.chat-text").append("User said: " + message.data + "<br />");
        return false;
    });

    socket.on('lobby_room_created', function(room) {
        var parsed = JSON.parse(room);
        $("div.rooms").append("Room (yours!) <br />");
    });

    socket.on('lobby_return_rooms', function(rooms) {
        var parsed = JSON.parse(rooms);
        for (var i = 0; i < parsed.rooms.length; i++) {
            if (rooms.owner == username) {
                $("div.rooms").append("Room (yours!) <br />");
            } else {
                $("div.rooms").append("Lobby <br />");
            }
        }
    });

    socket.on('lobby_room_already_exists', function() {
        console.log("Error: You already have a room.")
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

    $('#lobby-refresh-rooms').click(function(e) {
        $("div.rooms").html("");
        socket.emit('lobby_get_rooms');
        return false;
    });


});
