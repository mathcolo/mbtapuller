import _ from 'lodash';

function pie_chart(ctx, data) {
  return new Chart(ctx, {
    type: 'pie',
    data: data,
    options: {
      responsive: true
    }
  });
}

function movement_chart(canvas, name, color_background, color_border, thresholds, data) {
  var chart = new Chart(canvas, {
    type: 'line',
    data: {
      labels: _.rangeRight(0, data.length),
      datasets: [{
        label: name,
        data: data,
        backgroundColor: [
          color_background
          // 'rgba(0, 255, 0, 0.2)',
          // 'rgba(255, 99, 132, 0.2)',
          // 'rgba(54, 162, 235, 0.2)',
          // 'rgba(255, 206, 86, 0.2)',
          // 'rgba(75, 192, 192, 0.2)',
          // 'rgba(153, 102, 255, 0.2)',
          // 'rgba(255, 159, 64, 0.2)'
        ],
        borderColor: [
          color_border
          // 'rgba(255,99,132,1)',
          // 'rgba(54, 162, 235, 1)',
          // 'rgba(255, 206, 86, 1)',
          // 'rgba(75, 192, 192, 1)',
          // 'rgba(153, 102, 255, 1)',
          // 'rgba(255, 159, 64, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      legend: {
        display: false
      },

      "elements": {
        point: {
          radius: 0
        }
      },
      "horizontalLine": [{
        "y": thresholds[0],
        "style": "rgba(0, 255, 0, .7)",
        "text": ""
      },
      {
        "y": thresholds[1],
        "style": "rgba(244, 182, 66, 1)",
        "text": ""
      },
      {
        "y": thresholds[2],
        "style": "rgba(255, 0, 0, 1)",
        "text": ""
      }
      ],
      responsive: true,
      scales: {
        yAxes: [{
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'average displacement last 10 min (ft)'
          },
          ticks: {
            suggestedMax: 12000,
            beginAtZero: true
          }
        }],
        xAxes: [{
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'minutes ago'

          }
        }]
      }
    }
  });
  return chart;
}

export {movement_chart, pie_chart};