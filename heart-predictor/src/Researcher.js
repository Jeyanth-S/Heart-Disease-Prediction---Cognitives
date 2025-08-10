import React, { useState } from "react";
import "./Researcher.css";

export default function Researcher() {
  const [formData, setFormData] = useState({
    age: "",
    cholesterol: "",
    bloodPressure: ""
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handlePredict = () => {
    alert("Researcher prediction logic goes here");
  };

  const handleSummarize = () => {
    alert("Researcher summarization logic goes here");
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      alert(`Uploaded file: ${file.name}`);
    }
  };

  return (
    <div className="researcher-container">
      {/* HEADER */}
      <header className="researcher-header">
        <h2 className="researcher-title">Heart Disease Prediction - Researcher</h2>
        <div className="header-right">
          <label className="upload-btn">
            Upload Excel
            <input
              type="file"
              accept=".xlsx, .xls"
              onChange={handleFileUpload}
              style={{ display: "none" }}
            />
          </label>
        </div>
      </header>

      {/* MAIN CONTENT */}
      <main className="researcher-main">
        <div className="form-container">
          <label>Age:</label>
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
          />

          <label>Cholesterol:</label>
          <input
            type="number"
            name="cholesterol"
            value={formData.cholesterol}
            onChange={handleChange}
          />

          <label>Blood Pressure:</label>
          <input
            type="number"
            name="bloodPressure"
            value={formData.bloodPressure}
            onChange={handleChange}
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
