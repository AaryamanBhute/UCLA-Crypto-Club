String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

function makeChart(asset_id, dom_id, time, interval){
    priceHistory(asset_id, time, interval).done(function(r){
        console.log(r);
        var xValues = [];
        var yValues = [];
        for (let i = 0; i < r.data.length; i++){
            xValues.push(i);
            yValues.push(parseFloat(r.data[i]['priceUsd']))
        }
    
        new Chart(`${dom_id}`, {
            type: "line",
            data: {
            labels: xValues,
            datasets: [{
                fill: false,
                lineTension: 0,
                backgroundColor: "#00a8e8",
                borderColor: "#00a8e8",
                data: yValues
            }]
            },
            options: {
            legend: {display: false},
            scales: {
                xAxes: [{
                    display : false,
                }],
                yAxes: [{
                    ticks: {
                        callback: function(value, index, values) {
                        return value.toLocaleString("en-US",{style:"currency", currency:"USD"});
                        },
                        fontWeigth: 900,
                        font: { size: 12, }  
                    },
                    display : true,
                    gridLines: {
                        display: false
                     }
                }]
                
                },
            responsive : true,
            maintainAspectRatio : true,
            }
        });
    }); 
}

function makeChartMenu(asset_name){
    $("#chartmenu .content").empty();
    return(
        `
        <img src="${static_url}website/images/closebutton.png" class="closechartsbutton">
        <p class="chartstitle">${asset_name.toProperCase()} Charts</p>
        <div class="breaker"></div>
        <div class="assetchartwrapper">
            <p>24 Hour Chart</p>
            <canvas id="chart1" class="assetchart"></canvas>
        </div>
        <div class="assetchartwrapper">
            <p>48 Hour Chart</p>
            <canvas id="chart2" class="assetchart"></canvas>
        </div>
        <div class="assetchartwrapper">
            <p>1 Week Chart</p>
            <canvas id="chart3" class="assetchart"></canvas>
        </div>
        <div class="assetchartwrapper">
            <p>1 Month Chart</p>
            <canvas id="chart4" class="assetchart"></canvas>
        </div>
        <div class="assetchartwrapper">
            <p>3 Month Chart</p>
            <canvas id="chart5" class="assetchart"></canvas>
        </div>
        <div class="assetchartwrapper">
            <p>6 Month Chart</p>
            <canvas id="chart6" class="assetchart"></canvas>
        </div>
        `
    );
}

$(document).ready(function(){
    $('#chartmenu').hide()
    Chart.defaults.global.defaultFontStyle = '600';
});

$('.assetname').click(function(){
    let = asset_n = $(this).attr('id');
    $('#chartmenu .content').append(makeChartMenu(asset_n))
    $('#chartmenu').show();
    makeChart(asset_n, "chart1", 12, 'm15');
    makeChart(asset_n, "chart2", 24, 'm30');
    makeChart(asset_n, "chart3", 48, 'h1');
    makeChart(asset_n, "chart4", 168, 'h6');
    makeChart(asset_n, "chart5", 730, 'h12');
    makeChart(asset_n, "chart6", 2190, 'd1');
})

$(document).on('click', ".closechartsbutton", function() {
    $("#chartmenu").hide();
    $("#chartmenu .content").empty();
});