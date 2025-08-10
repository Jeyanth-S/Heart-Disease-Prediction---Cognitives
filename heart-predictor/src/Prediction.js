import React, { useState } from "react";
import "./Prediction.css";

export default function Prediction() {
  const [formData, setFormData] = useState({
    age: "",
    cholesterol: "",
    bloodPressure: ""
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handlePredict = async () => {
    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      alert(`Prediction: ${result.prediction}`);
    } catch (error) {
      console.error("Error:", error);
      alert("Prediction failed");
    }
  };

  const handleSummarize = async () => {
    try {
      const response = await fetch("http://localhost:5000/summarize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      alert(`Summary: ${result.summary}`);
    } catch (error) {
      console.error("Error:", error);
      alert("Summarization failed");
    }
  };

  return (
    <div className="prediction-container">
      <header className="prediction-header">
        <h1 className="prediction-title">Heart Disease Prediction</h1>
      </header>

      <main className="prediction-main">
        <div className="form-container">
          <label>Age:</label>
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            placeholder="Enter age"
          />

          <label>Cholesterol:</label>
          <input
            type="number"
            name="cholesterol"
            value={formData.cholesterol}
            onChange={handleChange}
            placeholder="Enter cholesterol level"
          />

          <label>Blood Pressure:</label>
          <input
            type="number"
            name="bloodPressure"
            value={formData.bloodPressure}
            onChange={handleChange}
            placeholder="Enter blood pressure"
          />

          <div className="button-group">
            <button className="predict-btn" onClick={handlePredict}>
              Predict
            </button>
            <button className="summarize-btn" onClick={handleSummarize}>
              Summarize
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
