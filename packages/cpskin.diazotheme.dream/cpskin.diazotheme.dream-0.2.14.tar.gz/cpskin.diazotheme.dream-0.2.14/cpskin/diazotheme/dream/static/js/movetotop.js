$(document).ready(function(){   
    $(function () {
        $(window).scroll(function () {
            if ($(this).scrollTop() > 300) {
                $('#scroll-to-top').fadeIn();
            } else {
                $('#scroll-to-top').fadeOut();
            }
        });
 
        $('#scroll-to-top a').click(function () {
            $('body,html').animate({
                scrollTop: 0
            }, 700);
            return false;
        });
    });
    $("#scroll-to-top").hide();
});
