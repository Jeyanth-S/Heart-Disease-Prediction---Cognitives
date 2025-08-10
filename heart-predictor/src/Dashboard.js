import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaHeartbeat, FaLeaf, FaRobot } from "react-icons/fa";
import "./Dashboard.css";

export default function Dashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    deaths: "Loading...",
    preventable: "Loading...",
    accuracy: "Loading...",
  });

  useEffect(() => {
    // Simulated fetch with fallback data
    // Replace with real API if available
    setTimeout(() => {
      setStats({
        deaths: "17.9M",
        preventable: "80%",
        accuracy: "74%",
      });
    }, 1500);
  }, []);

  return (
    <div className="dashboard-container">
      {/* HEADER */}
      <header className="dashboard-header">
        <h1 className="dashboard-title">Heart Disease Prediction</h1>
        <div className="header-buttons">
          <button
            className="header-btn researcher-btn"
            onClick={() => navigate("/researcher")}
          >
            Researcher
          </button>
          <button
            className="header-btn individual-btn"
            onClick={() => navigate("/prediction")}
          >
            Individual
          </button>
        </div>
      </header>

      {/* MAIN CONTENT */}
      <main className="dashboard-main">
        {/* Stats Section */}
        <section className="stats-section">
          <h2>Heart Health Insights</h2>
          <div className="stats-cards">
            <div className="stat-card">
              <FaHeartbeat size={40} color="#e63946" />
              <h3>{stats.deaths}</h3>
              <p>Annual global deaths from cardiovascular diseases</p>
            </div>
            <div className="stat-card">
              <FaLeaf size={40} color="#2a9d8f" />
              <h3>{stats.preventable}</h3>
              <p>Cases preventable with healthy lifestyle</p>
            </div>
            <div className="stat-card">
              <FaRobot size={40} color="#264653" />
              <h3>{stats.accuracy}</h3>
              <p>Prediction accuracy using AI models</p>
            </div>
          </div>
        </section>

        {/* Blog Insights Section */}
        <section className="blog-insights">
          <h2>Heart Disease: Causes & Complications</h2>
          <div className="insights-list">
            <article className="insight-item">
              <strong>Complications of Heart Disease:</strong> Heart disease can lead to heart failure, heart attacks, stroke, pulmonary embolism, cardiac arrest, peripheral artery disease, and atrial fibrillation.{" "}
              <a href="https://www.healthline.com/health/heart-disease/complications" target="_blank" rel="noopener noreferrer">Learn more</a>
            </article>
            <article className="insight-item">
              <strong>Hypertension Effects:</strong> High blood pressure strains the heart, causing left ventricular hypertrophy (LVH), which may progress to heart failure, arrhythmias, ischemic stroke, and even end-stage renal disease.{" "}
              <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC10277698/" target="_blank" rel="noopener noreferrer">Learn more</a>
            </article>
            <article className="insight-item">
              <strong>Global Impact:</strong> Cardiovascular disease accounts for roughly one-third of all global deaths, making it the leading cause worldwide and emphasizing the need for prevention.{" "}
              <a href="https://www.cdc.gov/heart-disease/data-research/facts-stats/index.html" target="_blank" rel="noopener noreferrer">Learn more</a>
            </article>
          </div>
        </section>
      </main>

      {/* Logout Button at Bottom Right */}
      <div className="bottom-logout">
        <button className="logout-btn" onClick={() => navigate("/")}>
          Logout
        </button>
      </div>
    </div>
  );
}
