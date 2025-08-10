import React, { useState } from "react";
import "./Prediction.css";

export default function Prediction() {
  const initialFormData = {
    age: "",
    gender: "",
    height: "",
    weight: "",
    ap_hi: "",
    ap_lo: "",
    cholesterol: "",
    gluc: "",
    smoke: "",
    alco: "",
    active: ""
  };

  const [formData, setFormData] = useState(initialFormData);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handlePredict = async () => {
    if (Object.values(formData).some((v) => v === "")) {
      alert("Please fill in all fields before predicting.");
      return;
    }

    setLoading(true);

    try {
      const formattedData = Object.fromEntries(
        Object.entries(formData).map(([key, value]) => [key, Number(value)])
      );

      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formattedData),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const result = await response.json();

      if (result.prediction !== undefined) {
        alert(`Prediction: ${result.prediction}`);
      } else {
        alert("Prediction not found in response.");
        console.error("Unexpected API response:", result);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Prediction failed. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="prediction-container">
      <header className="prediction-header">
        <h1 className="prediction-title">Heart Disease Prediction</h1>
      </header>

      <main className="prediction-main">
        <div className="form-container">
          {Object.keys(formData).map((field) => (
            <div key={field} className="form-group">
              <label>{field.replace(/_/g, " ").toUpperCase()}:</label>
              <input
                type="number"
                name={field}
                value={formData[field]}
                onChange={handleChange}
                placeholder={`Enter ${field}`}
              />
            </div>
          ))}

          <div className="button-group">
            <button
              className="predict-btn"
              onClick={handlePredict}
              disabled={loading}
            >
              {loading ? "Predicting..." : "Predict"}
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
