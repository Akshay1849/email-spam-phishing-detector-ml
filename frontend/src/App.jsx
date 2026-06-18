import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import PieChart from "./PieChart";

function App() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);

  const fetchDashboard = async () => {
    try {
      const statsRes = await axios.get("http://127.0.0.1:5000/stats");
      const historyRes = await axios.get("http://127.0.0.1:5000/history");

      setStats(statsRes.data);
      setHistory(historyRes.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const analyzeEmail = async () => {
    if (!email.trim()) {
      setError("Please enter email text");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/predict",
        { email }
      );

      setResult(response.data);
      await fetchDashboard();
    } catch (err) {
      console.error(err);
      setError("Backend error. Check Flask server.");
    } finally {
      setLoading(false);
    }
  };

  const clearAll = () => {
    setEmail("");
    setResult(null);
    setError("");
  };

  return (
  <div className="container">
    {/* Header */}
    <header className="hero">
      <h1>AI Email Security Dashboard</h1>
      <p>Spam, phishing and malicious URL detection using ML + NLP</p>
    </header>

    {/* Input Section */}
    <div className="input-section">
      <textarea
        rows="10"
        placeholder="Paste email content here..."
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <div className="button-group">
        <button onClick={analyzeEmail} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>

        <button onClick={clearAll}>Clear</button>
      </div>

      {error && <p className="error">{error}</p>}
    </div>

    {/* Result */}
    {result && (
      <div
        className={`result-card ${
          result.prediction === "SPAM" ? "spam" : "safe"
        }`}
      >
        <h2>Prediction: {result.prediction}</h2>

        <p>
          <strong>Confidence:</strong> {result.confidence}%
        </p>

        <p>
          <strong>Risk Level:</strong> {result.risk_level}
        </p>

        <p>
          <strong>Phishing Score:</strong> {result.phishing_score}
        </p>

        <h3>Reasons:</h3>

        {result.reasons?.length > 0 ? (
          <ul>
            {result.reasons.map((reason, index) => (
              <li key={index}>{reason}</li>
            ))}
          </ul>
        ) : (
          <p>No suspicious patterns detected.</p>
        )}
      </div>
    )}

    {/* Dashboard */}
    {stats && (
      <div className="dashboard">
        <h2>Analytics Dashboard</h2>

        <div className="dashboard-layout">
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Scans</h3>
              <p>{stats.total}</p>
            </div>

            <div className="stat-card">
              <h3>Spam</h3>
              <p>{stats.spam}</p>
            </div>

            <div className="stat-card">
              <h3>Safe</h3>
              <p>{stats.ham}</p>
            </div>

            <div className="stat-card">
              <h3>High Risk</h3>
              <p>{stats.high_risk}</p>
            </div>
          </div>

          <div className="chart-section">
            <h2>Spam Distribution</h2>
            <PieChart stats={stats} />
          </div>
        </div>
      </div>
    )}

    {/* History */}
    {history.length > 0 && (
  <div className="history-section">
    <h2>Recent Scans</h2>

    <table className="history-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Prediction</th>
          <th>Confidence</th>
          <th>Risk</th>
          <th>Score</th>
        </tr>
      </thead>

      <tbody>
        {history.map((item) => (
          <tr key={item.id}>
            <td>{item.id}</td>
            <td
              className={
                item.prediction === "SPAM"
                  ? "spam-text"
                  : "safe-text"
              }
            >
              {item.prediction}
            </td>
            <td>{item.confidence}%</td>
            <td>{item.risk_level}</td>
            <td>{item.score}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)}
  </div>
);
}

export default App;