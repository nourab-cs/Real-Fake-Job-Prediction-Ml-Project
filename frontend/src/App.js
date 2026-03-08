import React, { useState } from 'react';
import axios from 'axios';
import JobForm from './components/JobForm';
import ResultCard from './components/ResultCard';
import Header from './components/Header';
import './App.css';

const API_URL = 'http://localhost:8000';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/predict`, formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get prediction. Make sure the API is running on port 5000.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="App">
      <Header />
      <div className="main-container">
        <JobForm onSubmit={handleSubmit} loading={loading} onReset={handleReset} />
        {error && (
          <div className="error-message">
            <div className="error-icon">⚠️</div>
            <div className="error-text">{error}</div>
          </div>
        )}
        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Analyzing job posting...</p>
          </div>
        )}
        {result && !loading && <ResultCard result={result} onReset={handleReset} />}
      </div>
    </div>
  );
}

export default App;
