$(".loginbutton").click(function(){
    window.location.assign(loginurl);
});
$(".logoutbutton").click(function(){
    window.location.assign("/logout");
});
$(".accountlogout").click(function(){
    window.location.assign("/logout");
});
$(".loginbutton1").click(function(){
    window.location.assign(loginurl);
});
$(".logoutbutton1").click(function(){
    window.location.assign("/logout");
});
$(".navimg").click(function(){
    window.location.assign("/");
});
$(".savebuttonwrapper").click(function(){
    
    let settings = "";
    if($(".anon-switch input").is(":checked")){
        settings += "false";
    }
    else{
        settings += "true";
    }
    settings += ";";
    if($(".light-mode input").is(":checked")){
        settings += "false";
    }
    else{
        settings += "true";
    }

    window.location.assign("/updatesettings/" + settings);
});
$(".nav p").click(function(){
    window.location.assign("/" + $(this).text());
})
$("#sidemenu .linkwrapper p").click(function(){
    window.location.assign("/" + $(this).text());
})
$(".closebutton").click(function(){
    $(this).parent().hide();
})