// This file contains the JavaScript code that renders the chart.
/**
 * This function is called by /demo/home.html template and receives a JSON object.
 * Data parameter contains CV, DV and Ion Current parsed data needed to plot the 3D Scatter Plot.
 * These JSON data equals to X-axis values, Y-axis values and Z-axis values.
 * Uses HighChart APIs to plot the data.
 *
 * Now displays a dummy plot from HighCharts examples. But real data is accessible with:
 * data['x_cv']
 * data['y_dv']
 * data['z_ic'][0] to data['z_ic][(data['y_dv'].length)-1]
 * @param data
 */
function render_chart(data) {
    var str_data = data['grid_data'];
    var float_data = []

    for (var index in str_data) {
        float_data.push(str_data[index].map(parseFloat));
    }


    // Give the points a 3D feel by adding a radial gradient
    Highcharts.getOptions().colors = $.map(Highcharts.getOptions().colors, function (color) {
        return {
            radialGradient: {
                cx: 0,
                cy: 0,
                r: 0
            },
            stops: [
                [0, color],
                [1, Highcharts.Color(color).brighten(-0.2).get('rgb')]
            ]
        };
    });

    // Set up the chart
    var chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container',
            margin: 100,
            animation: false,
            shadow: false,
            type: 'scatter',
            options3d: {
                enabled: true,
                alpha: 10,
                beta: 30,
                depth: 500,
                viewDistance: 50,

                frame: {
                    bottom: { size: 1, color: 'rgba(0,0,0,0.02)' },
                    back: { size: 1, color: 'rgba(0,0,0,0.04)' },
                    side: { size: 1, color: 'rgba(0,0,0,0.06)' }
                }
            }
        },
        title: {
            text: 'Owlstone Fingerprint'
        },
        subtitle: {
            text: 'Click and drag the plot area to rotate in space'
        },
        plotOptions: {
            scatter: {
                width: 10,
                height: 10,
                depth: 10
            }
        },
        tooltip: {
            animation: false,
            shadow: false
        },
        yAxis: {
            min: parseFloat(data['z_min']),
            max: parseFloat(data['z_max']),
            title: {
                text: 'Current'
            },
            tickInterval: 25
        },
        xAxis: {
            min: parseFloat(data['x_cv'][0]),
            max: parseFloat(data['x_cv'].pop()),
            gridLineWidth: 1,
            title: {
                text: 'CV'
            },
            tickInterval: 0.025
        },
        zAxis: {
            min: parseInt(data['y_dv'][0]) - 1,
            max: parseInt(data['y_dv'].pop()),
            //min: 0,
            //max: 55,
            gridLineWidth: 1,
            title: {
                text: 'Lines'
            },
            tickInterval: 1
        },
        legend: {
            enabled: false
        },
        series: [{
            name: 'Reading',
            colorByPoint: true,
            marker: {
                enabled: true,
                radius: 1
            },
            animation: false,
            shadow: false,
            turboThreshold: 60000,
            data: float_data
        }]
    });


    // Add mouse events for rotation
    $(chart.container).bind('mousedown.hc touchstart.hc', function (eStart) {
        eStart = chart.pointer.normalize(eStart);

        var posX = eStart.pageX,
            posY = eStart.pageY,
            alpha = chart.options.chart.options3d.alpha,
            beta = chart.options.chart.options3d.beta,
            newAlpha,
            newBeta,
            sensitivity = 5; // lower is more sensitive

        $(document).bind({
            'mousemove.hc touchdrag.hc': function (e) {
                // Run beta
                newBeta = beta + (posX - e.pageX) / sensitivity;
                chart.options.chart.options3d.beta = newBeta;

                // Run alpha
                newAlpha = alpha + (e.pageY - posY) / sensitivity;
                chart.options.chart.options3d.alpha = newAlpha;

                chart.redraw(false);
            },
            'mouseup touchend': function () {
                $(document).unbind('.hc');
            }
        });
    });
}
