import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-icon">🔍</div>
        <div className="header-text">
          <h1>Fake Job Posting Detector</h1>
          <p>Protect yourself from fraudulent job postings using AI-powered detection</p>
        </div>
      </div>
      <div className="header-stats">
        <div className="stat">
          <div className="stat-value">98.7%</div>
          <div className="stat-label">Accuracy</div>
        </div>
        <div className="stat">
          <div className="stat-value">99.7%</div>
          <div className="stat-label">ROC-AUC</div>
        </div>
      </div>
    </header>
  );
};

export default Header;
