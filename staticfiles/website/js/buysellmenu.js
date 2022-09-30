$( document ).ready(function() {
    $("#buysellmenu").hide();
})

$(document).on('input', ".buyinput", function() {
    if($(this).val() === ""){
        $("#orderprice").text("N/A");
    }
    else if(parseFloat($(this).val()) < 0){
        $("#orderprice").text("N/A");
    }
    else{
        let price = new Big(parseFloat(selected_asset_info.priceUsd));
        let amount = new Big(parseFloat($(this).val()));
        let v = price.times(amount);
        console.log(v.toString());
        $("#orderprice").text(floatToString(v.toString()) + "$");    
    }
});

$(document).on('input', ".sellinput", function() {
    if($(this).val() === ""){
        $("#sellprice").text("N/A");
    }
    else if(parseFloat($(this).val()) < 0){
        $("#sellprice").text("N/A");
    }
    else{
        let price = new Big(parseFloat(selected_asset_info.priceUsd));
        let amount = new Big(parseFloat($(this).val()));
        let v = price.times(amount);
        $("#sellprice").text(floatToString(v.toString()) + "$"); 
    }
});

$(document).on('click', ".closebuysellbutton", function() {
    $("#buysellmenu").hide();
    $("#buysellmenu .content").empty();
});

$(document).on('click', ".name", function(){
    console.log("here");
    let asset_n = selected_asset_info.id;
    $('#chartmenu .content').append(makeChartMenu(asset_n))
    $('#chartmenu').show();
    makeChart(asset_n, "chart1", 12, 'm15');
    makeChart(asset_n, "chart2", 24, 'm30');
    makeChart(asset_n, "chart3", 48, 'h1');
    makeChart(asset_n, "chart4", 168, 'h2');
    makeChart(asset_n, "chart5", 730, 'h12');
    makeChart(asset_n, "chart6", 2190, 'd1');
});

function generateBuyMenu(info){
    $("#buysellmenu .content").empty();
    return(
        `
        <img src="${static_url}website/images/closebutton.png" class="closebuysellbutton">
        <img src=${static_url}website/images/icon/${selected_asset_info.symbol.toLowerCase()}.png onerror='this.src = "${static_url}website/images/icon/DEFAULT.png"' class="asseticon">
        <p>Asset Name: <span class="accent name">${selected_asset_info.name}</span></p>
        <p>Asset Symbol: <span class="accent">${selected_asset_info.symbol}</span></p>
        <p class="price"> Price Per: <span class="red">${floatToString(info.priceUsd)}$</span></p>
        <p class="funds"> Available Funds: <span class="green">${users_money}$</span></p>
        <label for="totalAmt">Enter Amount:</label>
        <input type="number" step="0.01" min="0" maxlength="100" id="totalAmt" class="buyinput">
        <p class="orderprice"> Order Cost: <span class="red" id="orderprice">0$</span></p>
        <div class="breaker"></div>
        <div class="buysubmit submit" onclick="makeBuyRequest()">submit</div>`
    );
}

function generateSellMenu(info){
    $("#buysellmenu .content").empty();
    return(
        `
        <img src="${static_url}website/images/closebutton.png" class="closebuysellbutton">
        <img src=${static_url}website/images/icon/${selected_asset_info.symbol.toLowerCase()}.png onerror='this.src = "${static_url}website/images/icon/DEFAULT.png"' class="asseticon">
        <p>Asset Name: <span class="accent name">${selected_asset_info.name}</span></p>
        <p>Asset Symbol: <span class="accent">${selected_asset_info.symbol}</span></p>
        <p class="price"> Price Per: <span class="red">${floatToString(info.priceUsd)}$</span></p>
        <p class="funds"> Owned Amount: <span class="green">${symbolsToAmountOwned[selected_asset_info.symbol]}</span></p>
        <label for="totalAmt">Sell Amount:</label>
        <input type="number" step="0.01" min="0" maxlength="100" id="totalAmt" class="sellinput">
        <p class="orderprice"> Sell For: <span class="red" id="sellprice">0$</span></p>
        <div class="breaker"></div>
        <div class="sellsubmit submit" onclick="makeSellRequest()">submit</div>`
    );
}



function generateErrorMenu(searchTerm){
    $("#buysellmenu .content").empty();
    return(
        `
        <img src="${static_url}website/images/closebutton.png" class="closebuysellbutton">
        <p style="margin-top: 20px">Couldn't find:</p>
        <p class="red">${searchTerm}</>
        <p>Try another search!</>`
    );
}

function openbuysellmenu(asset, buy){
    $(".menupopup").empty();
    cryptoSearch(asset).done(function (result){
        var info = null
        data = result['data']
        //console.log(data);
        for(const index in data){
            var cryptoInfo = data[index]
            if(cryptoInfo.symbol.toLowerCase() === asset.toLowerCase() ||
            cryptoInfo.name.toLowerCase() === asset.toLowerCase()){
                info = cryptoInfo;
            }
        }
        if(info == null){
            $("#buysellmenu .content").first().append(generateErrorMenu(asset));
        }
        else if(buy === true){
            selected_asset_info = info;
            $("#buysellmenu .content").first().append(generateBuyMenu(info));
        }
        else{
            selected_asset_info = info;
            $("#buysellmenu .content").first().append(generateSellMenu(info));
        }
        $("#buysellmenu").show();
    });
}

function openbuysellmenuID(id, buy){
    console.log("ID USAGE");
    $(".menupopup").empty();
    cryptoSearchID(id).done(function (result){
        var info = result['data']
        if(info == null){
            $("#buysellmenu .content").first().append(generateErrorMenu(id));
        }
        else if(buy === true){
            selected_asset_info = info;
            $("#buysellmenu .content").first().append(generateBuyMenu(info));
        }
        else{
            selected_asset_info = info;
            $("#buysellmenu .content").first().append(generateSellMenu(info));
        }
        $("#buysellmenu").show();
    });
}

function makeSellRequest(){
    let amount = $(".sellinput").val()
    if(amount === "" ){
        $(".menupopup").empty();
        $(".menupopup").append("<p>Add Amount To Sell</p>")
    }
    else if(amount === "0" || amount.indexOf("-") >= 0){
        $(".menupopup").empty();
        $(".menupopup").append("<p>Amount must be greater than 0</p>")
    }
    else{
        window.location.assign(`/sell/${selected_asset_info.id}/${amount}`);
    }
}

function makeBuyRequest(){
    let amount = $(".buyinput").val()
    if(amount === ""){
        $(".menupopup").empty();
        $(".menupopup").append("<p>Add Amount To Buy</p>")
    }
    else if(amount === "0" || amount.indexOf("-") >= 0){
        $(".menupopup").empty();
        $(".menupopup").append("<p>Amount must be greater than 0</p>")
    }
    else{
        window.location.assign(`/buy/${selected_asset_info.id}/${amount}`);
    }
}


$(".ownedassets .asset .asseticon").click(function(){
    let id = $(this).parent().attr('id');
    openbuysellmenuID(id, false);
});

$(".quickbuymenu .asset .asseticon").click(function(){
    let id = $(this).parent().attr('id');
    openbuysellmenuID(id, true);
});

$(".searchButton").click(function(){
    openbuysellmenu($(".searchTerm").val(), true);
    $(".searchTerm").val('');
});

$('.searchTerm').keypress(function (e) {
    var key = e.which;
    if(key == 13)  // the enter key code
     {
        openbuysellmenu($(".searchTerm").val(), true);
        $(".searchTerm").val('');
     }
   });   