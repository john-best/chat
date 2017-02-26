$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/');

    socket.on('rps_user_update', function(message) {
        $("div.chat-text").append("A user has selected " + message.data + "! <br />");
        return false;
    });

    $('#rps_choose_rock').click(function(e) {
        socket.emit('rps_server_update', {'data':'rock'});
        return false;
    });
    
    $('#rps_choose_paper').click(function(e) {
        socket.emit('rps_server_update', {'data':'paper'});
        return false;
    });

    $('#rps_choose_scissor').click(function(e) {
        socket.emit('rps_server_update', {'data':'scissor'});
        return false;
    });

    socket.on('chat_send_to_user', function(message) {
        $("div.chat-text").append("User said: " + message.data + "<br />");
        return false;
    });

    $('#chat-input-text').keypress(function(e) {
        if (e.which == '13') {
            if ($('#chat-input-text').val()) {
                socket.emit('chat_send_to_server', {'data': $('#chat-input-text').val()});
                $('#chat-input-text').val("");
            }
        }

    });

});
