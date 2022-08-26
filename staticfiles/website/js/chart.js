$(document).ready(function(){
    if($('#chart').length > 0){
        var xValues = [];
        var yValues = [];
        let price_history_recent = price_history.split(";");
        let c = 0;
        for (let i = 0; i < price_history_recent.length; i++){
            
            xValues.push(c);
            c += 1;
            yValues.push(parseFloat(price_history_recent[i]))
        }
    
        new Chart("chart", {
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
                        }
                      },
                      display : true,
                      gridLines: {
                        display: false
                     }
                  }],
                  responsive : true,
                  maintainAspectRatio : false,
              }
            }
          });
    }
});