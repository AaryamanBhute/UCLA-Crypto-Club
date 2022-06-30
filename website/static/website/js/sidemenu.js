var sidemenustate = false;
$("#menuicon").click(function(){
    $("#hamburgericon").toggleClass('is-active');
    if(sidemenustate){
        $("#menuicon").animate({"left" : "50px"});
        $("#sidemenu").animate({"left" : "-80vw"})
        sidemenustate = false;
    }
    else{
        $("#menuicon").animate({"left" : "69vw"});
        $("#sidemenu").animate({"left" : "0"})
        sidemenustate = true;
    }
    
});