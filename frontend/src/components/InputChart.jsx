import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function InputChart({ data }) {
  const chartData = {
    labels: [
      "Time in Hospital",
      "Lab Procedures",
      "Procedures",
      "Medications",
      "Outpatient",
      "Inpatient",
      "Emergency",
    ],
    datasets: [
      {
        label: "Patient Metrics",
        data: [
          data.time_in_hospital,
          data.num_lab_procedures,
          data.num_procedures,
          data.num_medications,
          data.number_outpatient,
          data.number_inpatient,
          data.number_emergency,
        ],
        backgroundColor: "rgba(59, 130, 246, 0.6)", // Blue-500 with opacity
        borderColor: "#3b82f6", // Blue-500
        borderWidth: 1,
        hoverBackgroundColor: "rgba(59, 130, 246, 0.8)",
        borderRadius: 4,
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
      title: {
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
        grid: { color: "#f1f5f9" },
        ticks: { color: "#64748b" },
      },
      x: {
        grid: { display: false },
        ticks: { 
            color: "#64748b",
            font: {
                size: 10
            }
        },
      },
    },
  };

  return <Bar options={options} data={chartData} />;
}
