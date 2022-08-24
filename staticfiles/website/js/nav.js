$(document).scroll(function() { 
    if($(window).scrollTop() === 0) {
        $(".nav").css("box-shadow", "none");
    }
    else{
        $(".nav").css("box-shadow", "0 2px 4px 0 rgba(0,0,0,.2)");
    }
 });