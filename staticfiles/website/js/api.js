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

function priceHistory(id){
    let full_url = "/search/history/" + id;
    return($.ajax({
        url : full_url,
        type : "GET",
        dataType: "json",
        data: {
        },
    }));
}