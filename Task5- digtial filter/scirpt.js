'use strict';

let canvas = document.querySelector('#z-plane');

let zeros = [];
let poles = [];
function setZplane(poles, zeros) {
  let radius = 130; // radius of unit circle
  let pSize = 4; // size of pole and zero graphic
  let zSize = 4;

  let ctx = canvas.getContext('2d');

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  let pad = (canvas.width - 2 * radius) / 2; // padding on each side

  // unit circle
  ctx.beginPath();
  ctx.strokeStyle = 'red';
  ctx.arc(radius + pad, radius + pad, radius, 0, 2 * Math.PI);
  ctx.stroke();

  // y axis
  ctx.beginPath();
  //ctx.lineWidth="1";
  ctx.strokeStyle = 'black';
  ctx.moveTo(radius + pad, 0);
  ctx.lineTo(radius + pad, canvas.height);
  ctx.font = 'italic 8px sans-serif';
  ctx.fillText('Im', radius + pad + 2, pad - 2);

  // x axis
  ctx.moveTo(0, radius + pad);
  ctx.lineTo(canvas.width, radius + pad);
  ctx.fillText('Re', radius + radius + pad + 2, radius + pad - 2);
  ctx.stroke(); // Draw it
  drawResponses();
}

function drawResponses() {
  // normalize

  let magDataArray = [];
  let phaseDataArray = [];

  // plot mag_response
  //Chart.js Setup
  const magLabels = ['1', '10', '100', '1000', '10000'];
  const magData = {
    labels: magLabels,
    datasets: [
      {
        label: 'Magnitude Response',
        data: [magDataArray],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };
  ///Chart.js config

  const magConfig = {
    type: 'line',
    data: magData,
  };
  var magChart = new Chart(document.getElementById('magChart'), magConfig);
  const phaseLabels = ['1', '10', '100', '1000', '10000'];
  const phaseData = {
    labels: phaseLabels,
    datasets: [
      {
        label: 'Phase Response',
        data: [phaseDataArray],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };
  ///Chart.js config

  const phaseConfig = {
    type: 'line',
    data: phaseData,
  };
  var myChart = new Chart(document.getElementById('phaseChart'), phaseConfig);
  // plot phase_response
  // container = document.getElementById('phase_response');
  // graph = Flotr.draw(container, [phaseData], { yaxis: { max: 4, min: -4 } });
}
setZplane();
console.log('test');
