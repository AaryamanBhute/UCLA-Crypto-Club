$("#nextupdate .timer").ready(function(){
    setInterval(function(){
        let d = new Date();
        var now = new Date(d.getTime() + d.getTimezoneOffset() * 60000);
        var m = 59-now.getMinutes();
        var s = 60-now.getSeconds();
        if(s === 60){
            s = 0;
            m += 1;
        }
        if(m == 60){
            m = 0;
        }
        if(m < 10){
            m = `0${m}`;
        }
        if(s < 10){
            s = `0${s}`;
        }
        $("#nextupdate .timer").text(`${m}:${s}`)
    }, 1000)
});