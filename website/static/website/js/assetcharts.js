$(document).ready(function(){
    Chart.defaults.global.defaultFontStyle = '600';
    $(".assetchart").each(function(i){
        let asset_id = $(this).prop('id');
        let is_buy = asset_id.search('/b')
        if(is_buy != -1){
            asset_id = asset_id.substring(0, is_buy);
        }
        console.log(asset_id);
        priceHistory(asset_id).done(function(r){
            var xValues = [];
            var yValues = [];
            for (let i = 0; i < r.data.length; i++){
                xValues.push(i);
                yValues.push(parseFloat(r.data[i]['priceUsd']))
            }

            let dom_id = asset_id;
            if(is_buy != -1){
                dom_id += '/b';
            }
        
            new Chart(`${dom_id}`, {
                type: "line",
                data: {
                labels: xValues,
                datasets: [{
                    fill: false,
                    lineTension: 0,
                    backgroundColor: "rgba(0,0,255,1.0)",
                    borderColor: "rgba(0,0,255,0.1)",
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
        
    })
});