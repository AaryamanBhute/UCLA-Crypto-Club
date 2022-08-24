$("#nextupdate .timer").ready(function(){
    setInterval(function(){
        let d = new Date();
        var now = new Date(d.getTime() + d.getTimezoneOffset() * 60000);
        let m = 59-now.getMinutes();
        let s = 60-now.getSeconds();
        if(s === 60){
            s = 0;
            m += 1;
        }
        if(m == 60){
            m = 0;
        }
        if(m.length == 1){
            m = `0${m}`;
        }
        if(s.length == 1){
            s = `0${s}`;
        }
        $("#nextupdate .timer").text(`${m}:${s}`)
    }, 1000)
});