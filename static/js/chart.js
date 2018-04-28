var mchart = null;
var cchart = null;
var nchart = null;

function requestData(){
	$.ajax({
		url: '/stats',
		type:'GET',
		dataType: 'json',
		data: {
			'memorydata' :[],
			'cpudata' :[],
			'networkdata' :[]
		},
		success:function(data){
			var mseries = mchart.series[0];
			mshift = mseries.data[0].length > 120;
			mchart.series[0].addPoint(point, true, mshift);

			setTimeout(requestdata, 10000);
		}
	});
}


$(document).ready(function(){
	mchart = new Highcharts.Chart({
	chart:{
		renderTo: 'memory',
		type: 'spline',
		event: {
			load: requestData //图表加载完毕后执行回调函数
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
            pointInterval: 10000, // one hour
            pointStart: Date.UTC(2009, 1, 6, 0, 0, 0)
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
