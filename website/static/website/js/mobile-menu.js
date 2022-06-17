var menuState = false;
var menuCooldown = false

$("#mobile-menu-button").click(function(){
    if(menuCooldown){
        return;
    }
    $("#mobile-menu-button").css("pointer-events", "none");
    menuCooldown = true;
    setTimeout(function(){
        menuCooldown = false;
    }, 100);
    setTimeout(function(){
        $("#mobile-menu-button").css("pointer-events", "auto");
    }, 500);
    if(menuState){
        closeMenu();
        menuState = false;
    }
    else{
        openMenu();
        menuState = true;
    }
    console.log(menuState);
});

function openMenu(){
    $("#mobile-sidebar").animate({left: 0});
    $("#mobile-menu-button").animate({left: 670});
}

function closeMenu(){
    $("#mobile-sidebar").animate({left: -800});
    $("#mobile-menu-button").animate({left: 80});
}