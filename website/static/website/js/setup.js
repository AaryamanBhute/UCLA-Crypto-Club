
$( document ).ready(function() {
    if(is_anonymous === "False"){
        $("#button-1 input").first().prop("checked", true)
    }
    if($("#popup").text().includes("Invalid") || $("#popup").text().includes("Wrong")){
        $("#popup").css("color", "red")
    }
    else{
        $("#popup").css("color", "green")
    }
    console.log(window.location.href);
    console.log(window.location.origin);
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
});

