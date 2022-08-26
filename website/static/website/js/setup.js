
$( document ).ready(function() {
    if(color_mode === "light"){
        document.documentElement.setAttribute('data-theme', 'light');
    }
    else{
        document.documentElement.setAttribute('data-theme', 'dark');
    }
    if(is_anonymous === "False"){
        $(".anon-switch input").first().prop("checked", true)
    }
    if(color_mode === "dark"){
        $(".light-mode input").first().prop("checked", true)
    }
    if($("#popup").text().includes("!")){
        $("#popup p").css("color", "green")
    }
    else{
        $("#popup p").css("color", "red")
    }
    if(window.location.href === window.location.origin + "/"){
        
        $('html, body').css('overflowY', 'hidden');
        $("#loading").css("opacity", 1);
        setTimeout(() => {
            $("#loading").animate({"opacity" : 0});
        }, 1200);
        setTimeout(() => {
            $('html, body').css('overflowY', 'auto');
            $("#hider").animate({"opacity" : 0});
            $("#hider").css("pointer-events", "none");
        }, 1500);
    }
    else{
        setTimeout(() => {
            $('html, body').css('overflowY', 'auto');
            $("#hider").animate({"opacity" : 0});
            $("#hider").css("pointer-events", "none");
        }, 200);
    }
    let e = $(".atcv")
    try{
        let f = parseFloat(e.text())
        if(f > 0){
            $(e).css("color", "green")
        }
        else if(f < 0){
            $(e).css("color", "red")
        }
        else{
            $(e).css("color", "grey")
        }
    }
    catch{}
    e = $(".cslv")
    try{
        let f = parseFloat(e.text())
        if(f > 0){
            $(e).css("color", "green")
        }
        else if(f < 0){
            $(e).css("color", "red")
        }
        else{
            $(e).css("color", "grey")
        }
    }
    catch{}
});

