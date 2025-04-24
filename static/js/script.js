// Example animations or alerts for buttons
document.querySelectorAll('button').forEach(button => {
    button.addEventListener('mouseenter', () => {
      button.classList.add('scale-105');
    });
    button.addEventListener('mouseleave', () => {
      button.classList.remove('scale-105');
    });
  });

  fetch('/data')
  .then(response => response.json())
  .then(data => {
    const labels = data.map(item => item.date);
    const stepsData = data.map(item => item.steps);

    const chartData = {
      labels: labels,
      datasets: [{
        label: 'Steps',
        data: stepsData,
        borderColor: '#F59E0B',
        backgroundColor: 'rgba(245, 158, 11, 0.5)',
        tension: 0.4,
        fill: true
      }]
    };

    const config = {
      type: 'line',
      data: chartData,
      options: { responsive: true }
    };

    new Chart(document.getElementById('progressChart'), config);
  });

  