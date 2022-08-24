//align account popup
$( document ).ready(function() {
    alignAccountPopup();
});
$( window ).resize(function() {
    alignAccountPopup();
});

function alignAccountPopup(){
    var pos = $(".accountimgwrapper").position();
    var right = $(window).width() - pos.left - $(".accountimgwrapper").width();
    var offset = ($(".accountimgwrapper").width() - ($(".corner").width() * Math.sqrt(2)))/2;
    $("#accountpopup").css({"right" : right + offset});
}