function floatToString(f){
    if(f.indexOf("e") != -1){
        return(f);
    }
    var val = "" + f;
    var ind = val.indexOf(".");
    var counter = 0;
    while(ind > 0){
        if(counter == 3){
            counter = 0;
            val = val.substring(0, ind) + "," + val.substring(ind);
        }
        ind -= 1;
        counter += 1;
    }
    if(val.indexOf(".") != -1){
        val = val.substring(0, val.indexOf(".")+3);
    }
    return(val);
}