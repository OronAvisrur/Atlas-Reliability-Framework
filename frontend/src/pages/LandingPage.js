import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchMetrics } from '../services/api';
import './LandingPage.css';

function LandingPage() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadMetrics();
  }, []);

  const loadMetrics = async () => {
    try {
      setLoading(true);
      const data = await fetchMetrics();
      setMetrics(parseMetrics(data));
      setError(null);
    } catch (err) {
      setError('Failed to load metrics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const parseMetrics = (rawMetrics) => {
    const lines = rawMetrics.split('\n');
    const parsed = {
      totalRequests: 0,
      activeRequests: 0,
      avgLatency: 0
    };

    lines.forEach(line => {
      if (line.startsWith('http_requests_total')) {
        const match = line.match(/\s+([\d.]+)$/);
        if (match) parsed.totalRequests += parseFloat(match[1]);
      }
      if (line.startsWith('active_requests{')) {
        const match = line.match(/\s+([\d.]+)$/);
        if (match) parsed.activeRequests += parseFloat(match[1]);
      }
    });

    return parsed;
  };

  return (
    <div className="landing-page">
      <header className="header">
        <div className="logo-container">
          <h1 className="logo-text">ATLAS</h1>
          <p className="logo-subtitle">RELIABILITY FRAMEWORK</p>
        </div>
        <div className="auth-buttons">
          <button className="btn-secondary" onClick={() => navigate('/login')}>
            Login
          </button>
          <button className="btn-primary" onClick={() => navigate('/register')}>
            Register
          </button>
        </div>
      </header>

      <main className="main-content">
        <section className="hero">
          <h2>High Availability Book Search Service</h2>
          <p>FastAPI + PostgreSQL + Ollama LLM + Kubernetes</p>
        </section>

        <section className="metrics-section">
          <h3>System Metrics</h3>
          {loading && <p className="loading">Loading metrics...</p>}
          {error && <p className="error">{error}</p>}
          {metrics && (
            <div className="metrics-grid">
              <div className="metric-card">
                <div className="metric-value">{metrics.totalRequests}</div>
                <div className="metric-label">Total Requests</div>
              </div>
              <div className="metric-card">
                <div className="metric-value">{metrics.activeRequests}</div>
                <div className="metric-label">Active Requests</div>
              </div>
              <div className="metric-card">
                <div className="metric-value">{metrics.avgLatency.toFixed(2)}ms</div>
                <div className="metric-label">Avg Latency</div>
              </div>
            </div>
          )}
        </section>

        <section className="features">
          <h3>Features</h3>
          <div className="features-grid">
            <div className="feature-card">
              <h4>🔐 Secure Authentication</h4>
              <p>JWT-based authentication with PostgreSQL</p>
            </div>
            <div className="feature-card">
              <h4>📚 Smart Book Search</h4>
              <p>Ollama LLM extracts keywords from natural language</p>
            </div>
            <div className="feature-card">
              <h4>⚡ High Availability</h4>
              <p>3 replicas with Kubernetes self-healing</p>
            </div>
            <div className="feature-card">
              <h4>📊 Prometheus Monitoring</h4>
              <p>Real-time metrics and observability</p>
            </div>
          </div>
        </section>
      </main>

      <footer className="footer">
        <p>© 2024 Atlas Reliability Framework</p>
      </footer>
    </div>
  );
}

export default LandingPage;
