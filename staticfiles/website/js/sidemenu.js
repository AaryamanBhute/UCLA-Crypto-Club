/*var sidemenustate = false;
var sidemenumoving = false;
$("#menuicon").click(function(){
    if(sidemenumoving){
        return;
    }
    sidemenumoving = true;
    setTimeout(function(){
        sidemenumoving = false;
    }, 1000);
    $("#hamburgericon").toggleClass('is-active');
    if(sidemenustate){
        setTimeout(function(){
            $("#sidemenu").animate({"left" : "-80vw"})
        }, 400);
        $("#menuicon").animate({"left" : "50px"});
        sidemenustate = false;
    }
    else{
        setTimeout(function(){
            $("#menuicon").animate({"left" : "69vw"});
        }, 400);
        $("#sidemenu").animate({"left" : "0"})
        sidemenustate = true;
    }
    
});*/
var sidemenustate = false;
var sidemenumoving = false;
$("#menuicon").click(function(){
    if(sidemenumoving){
        return
    }
    console.log("here")
    if(!sidemenustate){
        sidemenumoving = true
        $("#sidemenu").toggleClass('open-sidemenu')
        setTimeout(function(){
            $("#menuicon").toggleClass('open-menuicon');
            $("#hamburgericon").toggleClass('is-active');
            sidemenumoving = false;
        }, 200)
        sidemenustate = true;
    }
    else{
        sidemenumoving = true
        $("#menuicon").toggleClass('open-menuicon');
        $("#hamburgericon").toggleClass('is-active');
        setTimeout(function(){
            $("#sidemenu").toggleClass('open-sidemenu')
            sidemenumoving = false;
        }, 200)
        sidemenustate = false;
    }
})