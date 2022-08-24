
$( document ).ready(function() {
    if(is_anonymous === "False"){
        $("#button-1 input").first().prop("checked", true)
    }
    if($("#popup").text().includes("!")){
        $("#popup").css("color", "green")
    }
    else{
        $("#popup").css("color", "red")
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

