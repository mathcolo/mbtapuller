import _ from 'lodash';
import Chart from 'chart.js'
import horizonalLinePlugin from './modules/horizontal_line.js'
import {movement_chart} from './modules/custom_charts.js'

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


Chart.pluginService.register(horizonalLinePlugin);
stat_pull()