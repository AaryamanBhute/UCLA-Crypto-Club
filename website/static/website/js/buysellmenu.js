$( document ).ready(function() {
    $("#buysellmenu").hide();
})

$(document).on('input', ".buyinput", function() {
    if($(this).val() === ""){
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

function generateBuyMenu(info){
    return(
        `
        <img src="${static_url}website/images/closebutton.png" class="closebuysellbutton">
        <img src=${static_url}website/images/icon/${selected_asset_info.symbol}.png class="asseticon">
        <p>Asset Name: <span class="accent">${selected_asset_info.name}</span></p>
        <p>Asset Symbol: <span class="accent">${selected_asset_info.symbol}</span></p>
        <p class="price"> Price Per: <span class="red">${floatToString(info.priceUsd)}$</span></p>
        <p class="funds"> Available Funds: <span class="green">${users_money}$</span></p>
        <label for="totalAmt">Enter Amount:</label>
        <input type="number" step="0.01" id="totalAmt" class="buyinput">
        <p class="orderprice"> Order Cost: <span class="red" id="orderprice">0$</span></p>
        <div class="breaker"></div>
        <div class="buysubmit submit">submit</div>`
    );
}

function generateSellMenu(info){
    return(
        `
        <img src="${static_url}website/images/closebutton.png" class="closebuysellbutton">
        <img src=${static_url}website/images/icon/${selected_asset_info.symbol}.png class="asseticon">
        <p>Asset Name: <span class="accent">${selected_asset_info.name}</span></p>
        <p>Asset Symbol: <span class="accent">${selected_asset_info.symbol}</span></p>
        <p class="price"> Price Per: <span class="red">${floatToString(info.priceUsd)}$</span></p>
        <p class="funds"> Owned Amount: <span class="green">${symbolsToAmountOwned[selected_asset_info.symbol]}</span></p>
        <label for="totalAmt">Sell Amount:</label>
        <input type="number" step="0.01" id="totalAmt" class="sellinput">
        <p class="orderprice"> Sell For: <span class="red" id="sellprice">0$</span></p>
        <div class="breaker"></div>
        <div class="sellsubmit submit">submit</div>`
    );
}

function generateErrorMenu(info){
    
}

function openbuysellmenu(asset, buy){
    $("#buysellmenu").show();
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
            //error menu
        }
        else if(buy === true){
            selected_asset_info = info;
            $("#buysellmenu .content").first().append(generateBuyMenu(info));
        }
        else{
            selected_asset_info = info;
            $("#buysellmenu .content").first().append(generateSellMenu(info));
        }
    });
}
function closebuysellmenu(asset){
    $("#buysellmenu").hide();
}

$(".ownedassets .asset .asseticon").click(function(e){
    let asset = $(this).parent().attr('id');
    openbuysellmenu(asset, false);
});

$(".quickbuymenu .asset .asseticon").click(function(e){
    let asset = $(this).parent().attr('id');
    openbuysellmenu(asset, true);
});