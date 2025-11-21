import React, { useState } from "react";
import axios from "axios";
import ProbabilityChart from "./ProbabilityChart";
import InputChart from "./InputChart";

export default function PredictForm() {
  const [formData, setFormData] = useState({
    time_in_hospital: "",
    num_lab_procedures: "",
    num_procedures: "",
    num_medications: "",
    number_outpatient: "",
    number_inpatient: "",
    number_emergency: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const backendURL = process.env.REACT_APP_API_URL 
    ? `${process.env.REACT_APP_API_URL}/predict`
    : "http://localhost:8000/predict";

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: Number(e.target.value),
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post(backendURL, { data: formData });
      setResult(response.data);
    } catch (error) {
      console.error("Prediction error:", error);
      setResult({ error: "Failed to connect to backend. Please ensure the server is running." });
    }

    setLoading(false);
  };

  const fieldDescriptions = {
    time_in_hospital: "Days spent in the hospital (1-14)",
    num_lab_procedures: "Number of lab tests performed",
    num_procedures: "Number of procedures",
    num_medications: "Number of medications",
    number_outpatient: "Outpatient visits (last year)",
    number_inpatient: "Inpatient visits (last year)",
    number_emergency: "Emergency visits (last year)",
  };

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl w-full bg-white card-shadow p-8 rounded-xl animate-fade-in">
        <h1 className="text-3xl font-bold text-center text-slate-800 mb-2">
          Readmission Risk Predictor
        </h1>
        <p className="text-center text-slate-500 mb-10">
          Enter patient metrics to assess readmission probability
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          <div className="lg:col-span-2">
            <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {Object.keys(formData).map((key) => (
                <div key={key}>
                  <label className="block text-sm font-medium text-slate-700 mb-1 capitalize">
                    {key.replaceAll("_", " ")}
                  </label>
                  <input
                    type="number"
                    name={key}
                    value={formData[key]}
                    onChange={handleChange}
                    required
                    min="0"
                    className="w-full bg-slate-50 border border-slate-300 rounded-md px-3 py-2 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-shadow"
                    placeholder="0"
                  />
                  <p className="text-xs text-slate-400 mt-1">
                    {fieldDescriptions[key]}
                  </p>
                </div>
              ))}

              <div className="col-span-1 md:col-span-2 mt-6">
                <button
                  type="submit"
                  disabled={loading}
                  className={`w-full py-3 rounded-md text-white font-semibold shadow-sm transition-colors ${
                    loading
                      ? "bg-slate-400 cursor-not-allowed"
                      : "bg-blue-600 hover:bg-blue-700"
                  }`}
                >
                  {loading ? "Analyzing..." : "Predict Risk"}
                </button>
              </div>
            </form>
          </div>

          <div className="lg:col-span-1 border-l border-slate-100 pl-0 lg:pl-12 flex flex-col justify-center">
             <div className="h-full flex flex-col items-center justify-center text-slate-500 text-sm">
                {!result && (
                  <div className="text-center p-6 bg-slate-50 rounded-lg border border-slate-100 w-full">
                    <p>Results will appear here</p>
                  </div>
                )}
                
                {result && result.error && (
                    <div className="text-red-600 text-center p-4 bg-red-50 rounded-lg w-full">
                        <p className="font-semibold">Error</p>
                        <p>{result.error}</p>
                    </div>
                )}

                {result && !result.error && (
                  <div className="w-full animate-fade-in flex flex-col items-center">
                    
                    <div className="relative w-48 h-48 mb-6">
                      {/* Circular Progress Meter */}
                      <svg className="w-full h-full transform -rotate-90">
                        <circle
                          cx="96"
                          cy="96"
                          r="88"
                          stroke="currentColor"
                          strokeWidth="12"
                          fill="transparent"
                          className="text-slate-100"
                        />
                        <circle
                          cx="96"
                          cy="96"
                          r="88"
                          stroke="currentColor"
                          strokeWidth="12"
                          fill="transparent"
                          strokeDasharray={2 * Math.PI * 88}
                          strokeDashoffset={2 * Math.PI * 88 * (1 - result.probability)}
                          className={`transition-all duration-1000 ease-out ${
                            result.probability > 0.5 ? "text-red-500" : 
                            result.probability > 0.2 ? "text-yellow-500" : "text-green-500"
                          }`}
                          strokeLinecap="round"
                        />
                      </svg>
                      <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-4xl font-bold text-slate-800">
                          {(result.probability * 100).toFixed(1)}%
                        </span>
                        <span className="text-xs text-slate-400 uppercase tracking-wide mt-1">Probability</span>
                      </div>
                    </div>

                    <div className="mb-8 text-center">
                      <div className={`inline-flex items-center px-6 py-2 rounded-full shadow-sm border ${
                        result.risk_label === "HIGH RISK" ? "bg-red-50 border-red-100 text-red-600" :
                        result.risk_label === "MEDIUM RISK" ? "bg-yellow-50 border-yellow-100 text-yellow-600" :
                        "bg-green-50 border-green-100 text-green-600"
                      }`}>
                        <span className={`w-2 h-2 rounded-full mr-2 ${
                          result.risk_label === "HIGH RISK" ? "bg-red-500 animate-pulse" :
                          result.risk_label === "MEDIUM RISK" ? "bg-yellow-500" :
                          "bg-green-500"
                        }`}></span>
                        <span className="font-bold tracking-wide text-sm">{result.risk_label}</span>
                      </div>
                    </div>

                    <div className="w-full h-32 opacity-50 grayscale hover:grayscale-0 transition-all duration-500">
                        <ProbabilityChart probability={result.probability} />
                    </div>
                  </div>
                )}
             </div>
          </div>
        </div>

        {result && !result.error && (
          <div className="mt-12 pt-8 border-t border-slate-100 animate-fade-in">
             <h2 className="text-lg font-bold text-slate-800 mb-6">
                Patient Metrics
              </h2>
              <div className="h-64 w-full">
                <InputChart data={formData} />
              </div>
          </div>
        )}
      </div>
    </div>
  );
}
