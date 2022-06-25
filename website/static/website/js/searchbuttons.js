$(".searchbutton").click(function(){
    $(".searchbutton").each(function(){
        $(this).css("border", "4px solid transparent");
        $(this).removeClass("selected");
    });
    $(this).css("border", "4px solid var(--ucla-gold)");
    $(this).addClass("selected");
});