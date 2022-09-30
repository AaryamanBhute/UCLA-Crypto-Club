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

function cryptoSearchID(id){
    let full_url = "/search/id/" + id;
    return($.ajax({
        url : full_url,
        type : "GET",
        dataType: "json",
        data: {
        },
    }));
}


function priceHistory(id, time, interval){
    let full_url = `/search/history/${id}/${time}/${interval}`;
    return($.ajax({
        url : full_url,
        type : "GET",
        dataType: "json",
        data: {
        },
    }));
}