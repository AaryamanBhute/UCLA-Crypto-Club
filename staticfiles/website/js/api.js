function cryptoSearch(term){
    let full_url = "/search/" + term;
    return($.ajax({
        url : full_url,
        type : "GET",
        dataType: "json",
        data: {
        },
    }));
}