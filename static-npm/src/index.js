import _ from 'lodash';
import Chart from 'chart.js'
import horizonalLinePlugin from './modules/horizontal_line.js'
import {movement_chart, pie_chart} from './modules/custom_charts.js'

import { render } from 'react-dom';
import React, { Component } from 'react';
import FleetPie from './components/fleet-pie'

render(<FleetPie title="Red Line" />, document.getElementById('app'));

const ROUTES_SUBWAY = ['Red', 'Orange', 'Blue', 'Green-B', 'Green-C', 'Green-D', 'Green-E']
const ROUTES_SUBWAY_COLORS = {
  'Red': ['#da291c', '#704545', '#704545', '#704545', '#10ff00'],
  'Orange': ['#ed8b00', '#ed8b00', '#ed8b00', '#ed8b00', '#ed8b00'],
  'Blue': ['#1D3863', '#8296B5'],
  'Green-B': ['#002C0F', '#317F4B', '#002C0F'],
  'Green-C': ['#002C0F', '#317F4B', '#002C0F'],
  'Green-D': ['#002C0F', '#317F4B', '#002C0F'],
  'Green-E': ['#002C0F', '#317F4B', '#002C0F'],
}

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

function fleet_pie_all() {

  fetch('/puller/fleet/today.json')
  .then((resp) => resp.json())
  .then((data) => {

    _.map(ROUTES_SUBWAY, (route) => {
      const chart_ctx = document.getElementById(`fleet_${route}`).getContext('2d')
      pie_chart(chart_ctx, {
        datasets: [
          {
            label: 'Red Line fleet',
            backgroundColor: ROUTES_SUBWAY_COLORS[route],
            data: data[route].labels
          }
        ],
        labels: data[route].counts
      });
    })

  });

  
}


Chart.pluginService.register(horizonalLinePlugin);
// stat_pull()
fleet_pie_all()