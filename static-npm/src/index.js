import _ from 'lodash';
import Chart from 'chart.js'
import horizonalLinePlugin from './modules/horizontal_line.js'
import {movement_chart, pie_chart} from './modules/custom_charts.js'

function stat_pull() {

  var red_canvas = document.getElementById("red_canvas").getContext('2d');
  var orange_canvas = document.getElementById("orange_canvas").getContext('2d');

  fetch('/puller/movement_average.json')
    .then((resp) => resp.json())
    .then((data) => movement_chart(red_canvas, 'Red Line', 'rgba(255, 99, 132, 0.2)', 'rgba(255,99,132,1)', [7500, 6000, 5000], data))

    fetch('/puller/orange_movement_average.json')
    .then((resp) => resp.json())
    .then((data) => movement_chart(orange_canvas, 'Orange Line', 'rgba(244, 161, 66, 0.4)', 'rgba(244,161,66,1)', [7000, 6000, 5000], data))
}


function fleet_pie() {

  var pie_red_fleet = document.getElementById("pie_red_fleet").getContext('2d');
  var pie_orange_fleet = document.getElementById("pie_orange_fleet").getContext('2d');

  fetch('/puller/fleet/today_red.json')
    .then((resp) => resp.json())
    .then((data) => pie_chart(pie_red_fleet,
      {
        datasets: [
          {
            label: 'Red Line fleet',
            backgroundColor: ['#da291c', '#704545', '#704545', '#704545', '#10ff00'],
            data: data.labels
          }
        ],
        labels: data.counts
      }, 
      data))

      fetch('/puller/fleet/today_orange.json')
    .then((resp) => resp.json())
    .then((data) => pie_chart(pie_orange_fleet,
      {
        datasets: [
          {
            label: 'Orange Line fleet',
            backgroundColor: ['#ed8b00', '#ed8b00', '#ed8b00', '#ed8b00', '#ed8b00'],
            data: data.labels
          }
        ],
        labels: data.counts
      }, 
      data))
}


Chart.pluginService.register(horizonalLinePlugin);
stat_pull()
fleet_pie()