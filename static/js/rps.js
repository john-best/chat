$(function(){
    $('#rps_choose').click(function(){

        $.ajax({
            url: '/rps_choose',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
                $("div.rps_text").replaceWith("Successfully chosen!");
            },
            error: function(error){
                console.log(error);
                $("div.rps_text").prepend("An error has occured <br />");
            }
        });
    });
});
