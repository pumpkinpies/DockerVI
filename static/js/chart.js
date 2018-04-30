var mchart = null;
var cchart = null;
var nchart = null;

function requestData(){
	$.ajax({
        type: 'POST',
        url: './Stats/chart',
        data: {'memory':[],'cpu':[],'tx':[],'rx':[]},
        success: function(point){
            var series = mchart.series[0],
                shift = series.data.length > 60;

            mchart.series[0].addPoint(point['memory'],true,shift);

            var series = cchart.series[0],
                shift = series.data.length > 60;

            cchart.series[0].addPoint(point['cpu'],true,shift);
            
            var series = nchart.series[0],
                shift = series.data.length > 60;
            console.log(point['tx']);
            nchart.series[0].addPoint(point['tx'],true,shift);
            nchart.series[1].addPoint(point['rx'],true,shift);
  
            setTimeout(requestData, 20000);
		},
        cache: false
	});
}


$(document).ready(function(){
    //memory
	mchart = new Highcharts.Chart({
    	chart:{
    		renderTo: 'memory',
    		type: 'spline',
    		
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
                    radius: 3,
                    lineWidth: 0
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
    
    //cpu
    cchart = new Highcharts.Chart({
        chart:{
            renderTo: 'cpu',
            type: 'spline',
        },
        title:{
            text: 'CPU'
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
            valueSuffix: ' %'
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
                    radius: 3,
                    lineWidth: 0
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
            name: 'CPU',
            data: []
        }],
    });

    //network
    nchart = new Highcharts.Chart({
        chart:{
            renderTo: 'network',
            type: 'spline',
            event: {
                load: requestData() //图表加载完毕后执行回调函数
            }
        },
        title:{
            text: 'Network'
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
            valueSuffix: ' Kbps'
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
                    radius: 3,
                    lineWidth: 0
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
            name: 'tx',
            data: []
        },
        {
            name: 'rx',
            color: '#ffb4ae',
            data: []
        }],
    });
});


