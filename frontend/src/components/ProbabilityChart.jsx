import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function ProbabilityChart({ probability }) {
  const data = {
    labels: ["No Readmission", "Readmission"],
    datasets: [
      {
        label: "Probability",
        data: [1 - probability, probability],
        backgroundColor: ["#e2e8f0", "#3b82f6"], // Slate-200 and Blue-500
        borderColor: ["#cbd5e1", "#2563eb"],
        borderWidth: 1,
        hoverBackgroundColor: ["#cbd5e1", "#60a5fa"],
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: "#fff",
        titleColor: "#1e293b",
        bodyColor: "#475569",
        borderColor: "#e2e8f0",
        borderWidth: 1,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 1,
        grid: {
          color: "#f1f5f9",
        },
        ticks: {
          color: "#64748b",
          font: {
            family: "'Inter', sans-serif",
          },
        },
      },
      x: {
        grid: {
          display: false,
        },
        ticks: {
          color: "#64748b",
          font: {
            family: "'Inter', sans-serif",
            weight: "bold",
          },
        },
      },
    },
  };

  return (
    <div className="relative w-full h-full">
      <Bar data={data} options={options} />
    </div>
  );
}
