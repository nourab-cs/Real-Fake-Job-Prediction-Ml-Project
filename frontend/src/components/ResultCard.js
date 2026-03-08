import React from 'react';
import './ResultCard.css';

const ResultCard = ({ result, onReset }) => {
  const isFake = result.prediction === 'Fake';
  const confidencePercent = (result.confidence * 100).toFixed(1);

  const getRiskColor = (level) => {
    switch (level) {
      case 'Low': return '#11998e';
      case 'Medium': return '#f39c12';
      case 'High': return '#e74c3c';
      default: return '#95a5a6';
    }
  };

  return (
    <div className={`result-card ${isFake ? 'fake' : 'real'}`}>
      <div className="result-icon">
        {isFake ? '🚨' : '✅'}
      </div>

      <div className="result-header">
        <h2>{result.prediction} Job Posting</h2>
        <p className="result-subtitle">
          {isFake 
            ? 'Warning: This job posting shows signs of being fraudulent'
            : 'This job posting appears to be legitimate'}
        </p>
      </div>

      <div className="result-stats">
        <div className="stat-card">
          <div className="stat-icon">🎯</div>
          <div className="stat-content">
            <div className="stat-label">Confidence</div>
            <div className="stat-value">{confidencePercent}%</div>
            <div className="confidence-bar">
              <div 
                className="confidence-fill" 
                style={{ width: `${confidencePercent}%` }}
              ></div>
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <div className="stat-label">Risk Level</div>
            <div 
              className="stat-value risk-badge"
              style={{ color: getRiskColor(result.risk_level) }}
            >
              {result.risk_level}
            </div>
          </div>
        </div>
      </div>

      <div className="probabilities">
        <div className="probability-row">
          <div className="prob-label">
            <span className="prob-icon real-icon">✓</span>
            <span>Legitimate</span>
          </div>
          <div className="prob-bar-container">
            <div 
              className="prob-bar real-bar" 
              style={{ width: `${result.probabilities.real * 100}%` }}
            >
              <span className="prob-value">{(result.probabilities.real * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>

        <div className="probability-row">
          <div className="prob-label">
            <span className="prob-icon fake-icon">✗</span>
            <span>Fraudulent</span>
          </div>
          <div className="prob-bar-container">
            <div 
              className="prob-bar fake-bar" 
              style={{ width: `${result.probabilities.fake * 100}%` }}
            >
              <span className="prob-value">{(result.probabilities.fake * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>
      </div>

      <div className="warning-section">
        {isFake ? (
          <div className="warning-box danger">
            <h3>⚠️ Warning Signs</h3>
            <ul>
              <li>Do NOT send money for training, equipment, or background checks</li>
              <li>Be wary of guaranteed high earnings with minimal effort</li>
              <li>Verify the company exists and check reviews</li>
              <li>Research the contact information provided</li>
              <li>Trust your instincts - if it seems too good to be true, it probably is</li>
            </ul>
          </div>
        ) : (
          <div className="warning-box safe">
            <h3>✓ Looks Good</h3>
            <p>This job posting appears legitimate, but always:</p>
            <ul>
              <li>Research the company independently</li>
              <li>Verify job details during the interview</li>
              <li>Never provide sensitive personal information upfront</li>
              <li>Be cautious of requests for money or payment</li>
            </ul>
          </div>
        )}
      </div>

      <button onClick={onReset} className="btn-analyze-another">
        Analyze Another Job Posting
      </button>
    </div>
  );
};

export default ResultCard;
