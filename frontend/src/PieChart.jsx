import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

import { Pie } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

function PieChart({ stats }) {
  const data = {
    labels: ["Spam", "Safe"],
    datasets: [
      {
        data: [stats.spam, stats.ham],
        backgroundColor: ["#ef4444", "#22c55e"],
        borderWidth: 1
      }
    ]
  };

  const options = {
    plugins: {
      legend: {
        labels: {
          color: "white"
        }
      }
    }
  };

  return (
    <div style={{ width: "350px", margin: "auto" }}>
      <Pie data={data} options={options} />
    </div>
  );
}

export default PieChart;