$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/rps');
    socket.on('user_update', function(message) {
        $("div.rps_text").prepend("A user has selected something!");
        return false;
    });

    $('#rps_choose').click(function(e){

        socket.emit('server_update', $('form').serialize());

        return false;
    });
});
