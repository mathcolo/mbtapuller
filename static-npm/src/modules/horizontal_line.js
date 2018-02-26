var horizonalLinePlugin = {
    afterDraw: function (chartInstance) {
      var yValue;
      var yScale = chartInstance.scales["y-axis-0"];
      var canvas = chartInstance.chart;
      var ctx = canvas.ctx;
      var index;
      var line;
      var style;
  
      if (chartInstance.options.horizontalLine) {
        for (index = 0; index < chartInstance.options.horizontalLine.length; index++) {
          line = chartInstance.options.horizontalLine[index];
  
          if (!line.style) {
            style = "rgba(169,169,169, .6)";
          } else {
            style = line.style;
          }
  
          if (line.y) {
            yValue = yScale.getPixelForValue(line.y);
          } else {
            yValue = 0;
          }
  
          ctx.lineWidth = 1;
  
          if (yValue) {
            ctx.beginPath();
            ctx.moveTo(72, yValue);
            ctx.lineTo(canvas.width - 6, yValue);
            ctx.strokeStyle = style;
            ctx.stroke();
          }
  
          if (line.text) {
            ctx.fillStyle = style;
            ctx.fillText(line.text, 0, yValue + ctx.lineWidth);
          }
        }
        return;
      }
    }
  };

  export default horizonalLinePlugin;