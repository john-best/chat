$(document).ready(function() {
    var username = 'Gamer' + parseInt(Math.random() * 1000);
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    var room_count = 0;
    socket.emit('lobby_get_rooms');

    socket.on('chat_send_to_user', function(message) {
        $("div.chat-text").append("User said: " + message.data + "<br />");
        return false;
    });

    socket.on('lobby_room_created', function(room) {
        var parsed = JSON.parse(room);
        appendRoom(true);
    });

    socket.on('lobby_return_rooms', function(rooms) {
        var parsed = JSON.parse(rooms);
        for (var i = 0; i < parsed.rooms.length; i++) {
            if (i % 3 == 0) {
                $("div.rooms").append("<div class=\"row\">");
            }

            if (rooms.owner == username) {
                appendRoom(true);
            } else {
                appendRoom(false);
            }

            if (i % 3 == 0) {
                $("div.rooms").append("</div>");
            }

            room_count += 1;
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

    function appendRoom(isOwner) {
        var content = "<div class=\"col-md-4\"> \
            <div class=\"panel panel-default\"> \
            <div class=\"panel-heading\">Room";

        if (isOwner) {
            content += " (Yours!)";
        }

        content += "</div></div></div>";

        $("div.rooms").append(content);
    }

});
