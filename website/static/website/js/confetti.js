document.querySelector(".confetti1").addEventListener("load", function (e) {
    t1 = this;
    party.confetti(t1);
    setTimeout(function(e){
        party.confetti(t1);
        console.log("here");
    }, 500);
    setTimeout(function(e){
        party.confetti(t1);
        console.log("here");
    }, 1000);
});
document.querySelector(".confetti2").addEventListener("load", function (e) {
    t2 = this;
    party.confetti(t2);
    setTimeout(function(e){
        party.confetti(t2);
        console.log("here");
    }, 500);
    setTimeout(function(e){
        party.confetti(t2);
        console.log("here");
    }, 1000);
});