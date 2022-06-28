function updateBaseGallery(){
    var lastWasActive = false;
    $("#basegallery img.galleryimg").each(function(i) {
        if($(this).css('opacity') == 1){
            lastWasActive = true;
            $(this).animate({'opacity': 0}), 2000;
        }
        else if(lastWasActive){
            lastWasActive = false;
            $(this).animate({'opacity': 1}, 2000);
        }
    });
    if(lastWasActive){
        lastWasActive = false;
        //first activate
        $(".basegalleryimgwrapper").children(":first").animate({'opacity': 1}, 2000);
    }
}
var baseGalleryIntervalId = setInterval(updateBaseGallery, 4000);