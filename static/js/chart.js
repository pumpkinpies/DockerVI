var mchart = null;
var cchart = null;
var nchart = null;

function requestData(){
	$.ajax({
        type: 'POST',
        url: './Stats/chart',
        data: {'memory':[]},
        success: function(point){
            var series = mchart.series[0],
                shift = series.data.length > 60;

            mchart.series[0].addPoint(point['memory'],true,shift);
            setTimeout(requestData, 20000);
		},
        cache: false
	});
}


$(document).ready(function(){
	mchart = new Highcharts.Chart({
    	chart:{
    		renderTo: 'memory',
    		type: 'spline',
    		event: {
    			load: requestData() //图表加载完毕后执行回调函数
    		}
    	},
    	title:{
    		text: 'Memory'
    	},
    	xAxis: {
            type: 'datetime',
            labels: {
                overflow: 'justify'
            }
        },
        yAxis: {
            title: {
                text: ''
            },
            min: 0,
            minorGridLineWidth: 0,
            gridLineWidth: 0,
            alternateGridColor: null,
        },
        tooltip: {
            valueSuffix: ' MB '
        },
        plotOptions: {
            spline: {
                lineWidth: 2,
                states: {
                    hover: {
                        lineWidth: 3
                    }
                },
                marker: {
                    enabled: false
                },
                pointInterval: 20000, // 20s
                pointStart: Date.parse(new Date())+28800000
            }
        },
        navigation: {
            menuItemStyle: {
                fontSize: '10px'
            }
        },
        credits:{
            enabled: false // 禁用版权信息
        },
        series: [{
            name: 'Memory',
            data: []
        }],
    });
});

