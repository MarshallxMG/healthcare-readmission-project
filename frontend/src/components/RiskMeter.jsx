import React from "react";

export default function RiskMeter({ probability }) {
  const percent = (probability * 100).toFixed(1);

  let color = "text-green-600";
  let label = "LOW RISK";

  if (percent >= 20 && percent < 40) {
    color = "text-yellow-600";
    label = "MEDIUM RISK";
  }
  if (percent >= 40) {
    color = "text-red-600";
    label = "HIGH RISK";
  }

  return (
    <div className="flex flex-col items-center mt-6">
      <div
        className="w-40 h-40 rounded-full flex items-center justify-center shadow-lg"
        style={{
          border: `8px solid ${
            color === "text-red-600"
              ? "#dc2626"
              : color === "text-yellow-600"
              ? "#ca8a04"
              : "#16a34a"
          }`,
        }}
      >
        <span className={`text-2xl font-bold ${color}`}>{percent}%</span>
      </div>
      <p className={`mt-3 text-xl font-semibold ${color}`}>{label}</p>
    </div>
  );
}
