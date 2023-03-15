/* globals Chart, getComputedStyle */

function getCssVar (varName) {
  return getComputedStyle(document.body).getPropertyValue(`--${varName}`)
}

function makeSkillsChart (canvas, labels, scores) {
  canvas.width = 15
  canvas.height = labels.length

  const skillsChart = new Chart(canvas, {
    type: 'horizontalBar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Skill Level',
          data: scores,
          backgroundColor: getCssVar('salmon')
        }
      ]
    },
    options: {
      scales: {
        xAxes: [{
          ticks: {
            beginAtZero: true,
            stepSize: 1
          }
        }]
      }
    }
  })

  return skillsChart
}
