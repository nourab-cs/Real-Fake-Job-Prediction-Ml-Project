# 🚀 Fake Job Posting Detection API - Quick Start

## ✅ API is Running Successfully!

Your API is now live at **http://localhost:5000**

---

## 📚 Interactive API Documentation

Visit these URLs in your browser for interactive documentation:

- **Swagger UI (Recommended)**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

---

## 🧪 Test Results

All tests passed successfully:

### 1. Health Check ✅
```json
{
  "status": "healthy",
  "model_loaded": true,
  "tfidf_loaded": true,
  "encoders_loaded": true,
  "scaler_loaded": true
}
```

### 2. Model Performance ✅
- **Model**: LightGBM with Hybrid Features
- **Accuracy**: 98.71%
- **F1-Score**: 0.8553
- **ROC-AUC**: 0.9969

### 3. Real Job Posting Detection ✅
**Input**: Legitimate Google job posting

**Result**:
- **Prediction**: Real
- **Confidence**: 97.78%
- **Risk Level**: Low

### 4. Fake Job Posting Detection ✅
**Input**: Suspicious "work from home" posting

**Result**:
- **Prediction**: Fake
- **Confidence**: 99.84%
- **Risk Level**: High

---

## 🔌 API Endpoints

### GET `/health`
Check if API is running and models are loaded

### GET `/model-info`
Get model type, features, and performance metrics

### POST `/predict`
Predict whether a job posting is real or fake

**Required Fields**:
- `title`: Job title
- `description`: Job description

**Optional Fields**:
- `company_profile`, `requirements`, `benefits`
- `employment_type`, `required_experience`, `required_education`
- `industry`, `function`, `location`
- `telecommuting`, `has_company_logo`, `has_questions`

---

## 💻 Example Usage

### Python
```python
import requests

url = "http://localhost:5000/predict"
data = {
    "title": "Senior Software Engineer",
    "description": "We are looking for an experienced software engineer...",
    "company_profile": "Leading tech company",
    "requirements": "5+ years Python, AWS experience",
    "benefits": "Health insurance, 401k",
    "employment_type": "Full-time",
    "industry": "Information Technology",
    "location": "San Francisco, CA, US"
}

response = requests.post(url, json=data)
print(response.json())
```

### cURL
```bash
curl -X POST "http://localhost:5000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Software Engineer",
    "description": "We are looking for an experienced engineer..."
  }'
```

### JavaScript (Fetch)
```javascript
fetch('http://localhost:5000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: "Senior Software Engineer",
    description: "We are looking for..."
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## 🎯 Next Steps

### Week 5: React Frontend
Build a user interface to interact with this API

### Week 6: Docker
Containerize the API for easy deployment

### Week 7: Deployment
Deploy to cloud (AWS, Azure, Railway, etc.)

---

## 🛑 Stopping the API

To stop the server, press `Ctrl+C` in the terminal where it's running.

---

## 📝 Notes

- The API uses the best performing model (LightGBM) trained on hybrid features
- Preprocessing includes text cleaning, feature engineering, and TF-IDF vectorization
- All preprocessing happens automatically when you call the `/predict` endpoint
- The model returns both prediction and confidence scores for transparency

---

**Week 4 Complete! ✅**
