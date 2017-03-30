$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    var room_count = 0;
    var own_room = -1;
    var username = "";

    socket.emit('lobby_get_rooms');
    
    socket.on('chat_server_recv', function(message) {
        appendText(message.data);
    });

    socket.on('chat_self_connected', function(user) {
        username = user.username;
        appendText("You have connected.");
    });

    socket.on('lobby_room_created', function(room) {
        var parsed = JSON.parse(room);
        appendRoom(true, parsed);
    });

    socket.on('chat_user_list', function(userlist) {
        //var parsed = JSON.parse(userlist);
        console.log(userlist);
    });

    socket.on('lobby_return_rooms', function(rooms) {
        var parsed = JSON.parse(rooms);
        for (var i = 0; i < parsed.rooms.length; i++) {
            if (i % 3 == 0) {
                $("div.rooms").append("<div class=\"row\">");
            }

            if (parsed.rooms[i].room.owner == username) {
                appendRoom(true, parsed.rooms[i]);
            } else {
                appendRoom(false, parsed.rooms[i]);
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

    socket.on('lobby_room_deleted_by_owner', function() {
        $("div.rooms").html("");
        own_room = -1;
        socket.emit('lobby_get_rooms');
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
        socket.emit('lobby_create_room', {'creator': username, 'password': $('#room-password').val()});
        return false;
    });

    $('#lobby-refresh-rooms').click(function(e) {
        $("div.rooms").html("");
        socket.emit('lobby_get_rooms');
        return false;
    });

    $(document).on('click', '#lobby-delete-room', function(e) {
        socket.emit('lobby_delete_room', {'user': username, 'id': own_room});
        return false;
    });

    function appendRoom(isOwner, json) {
        var content = "<div class=\"col-md-4\"> \
            <div class=\"panel panel-default\"> \
            <div class=\"panel-heading\">Room";

        content += " (ID: " + json.room.id + ")";

        if (isOwner) {
            content += " (Yours!)";
            own_room = parseInt(json.room.id);
        }

        content += "</div>";
        content += "<div class=\"panel-body\"><p>Owner: " + json.room.owner +"</p>";
        if (json.room.password == "true") {
            content += "<p>Password Protected</p>";
        }
        content += "</div>";

        content += "<div class=\"panel-footer\"> \
            <input type=\"button\" value=\"Join Room\" id=\"lobby-join-room\"> \
            <input type=\"button\" value=\"Delete Room\" id=\"lobby-delete-room\" ";

        if (!isOwner) {
            content += "disabled";
        }
        content += "></div>";

        $("div.rooms").append(content);
    }

    function appendText(text) {
        var date = new Date();
        var time = date.toLocaleTimeString();

        $("div.chat-text").append("<div class=\"text-text\">[" + time + "] " + text + "<br /></div>");
        var height = 0;
        $('div.text-text').each(function(i, value) {
            height += parseInt($(this).height());
        });

        height += '';

        $("div.chat-box").animate({scrollTop: height});
    }

});
