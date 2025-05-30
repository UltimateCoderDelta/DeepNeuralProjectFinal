import { getDimensions } from './api'
import {
  Chart,
  Colors,
  BubbleController,
  CategoryScale,
  LinearScale,
  PointElement,
  Legend
} from 'chart.js'

Chart.register(
  Colors,
  BubbleController,
  PointElement,
  CategoryScale,
  LinearScale,
  Legend
);

(async function() {
  const data = await getDimensions();
  
    const chartAreaBorder = {
    id: 'chartAreaBorder',

    beforeDraw(chart, args, options) {
      const { ctx, chartArea: { left, top, width, height } } = chart;

      ctx.save();
      ctx.strokeStyle = options.borderColor;
      ctx.lineWidth = options.borderWidth;
      ctx.setLineDash(options.borderDash || []);
      ctx.lineDashOffset = options.borderDashOffset;
      ctx.strokeRect(left, top, width, height);
      ctx.restore();
    }
  };

  new Chart(
    document.getElementById('dimensions'),
    {
      type: 'bubble',
      plugins: [chartAreaBorder],
      options: {
        aspectRatio: 1,
        scales: {
            x: {
                max: 500,
                ticks: {
                    callback: value => `${value / 100} m`
                }
            },
            y: {
                max: 500,
                callback: value => `${value / 100} m`
            }
        }
      },
      data: {
        labels: data.map(x => x.year),
// ...

        datasets: [
          {
            label: 'width = height',
            data: data
              .filter(row => row.width === row.height)
              .map(row => ({
                x: row.width,
                y: row.height,
                r: row.count
              }))
          },
          {
            label: 'width > height',
            data: data
              .filter(row => row.width > row.height)
              .map(row => ({
                x: row.width,
                y: row.height,
                r: row.count
              }))
          },
          {
            label: 'width < height',
            data: data
              .filter(row => row.width < row.height)
              .map(row => ({
                x: row.width,
                y: row.height,
                r: row.count
              }))
          }
        ]
      }
    }
  );
})();
