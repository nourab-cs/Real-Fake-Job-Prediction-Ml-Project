# Fake Job Posting Detection API

FastAPI application for predicting whether a job posting is real or fake using machine learning.

## Features

- **Model**: LightGBM classifier with 98.7% accuracy
- **Feature Engineering**: Hybrid approach (TF-IDF + 22 engineered features)
- **Real-time Predictions**: Fast REST API with automatic preprocessing
- **Risk Assessment**: Low/Medium/High risk levels based on fake probability

## Installation

### 1. Install Dependencies

```bash
cd api
pip install -r requirements.txt
```

### 2. Download NLTK Data (first time only)

```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

## Running the API

### Development Mode

```bash
cd api
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
cd api
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### 1. Root
```
GET /
```
Returns API information and available endpoints.

### 2. Health Check
```
GET /health
```
Check if the API and model are loaded properly.

### 3. Predict
```
POST /predict
```

**Request Body:**
```json
{
  "title": "Senior Software Engineer",
  "company_profile": "We are a leading tech company...",
  "description": "We are looking for a talented software engineer...",
  "requirements": "5+ years of Python experience, BS in Computer Science",
  "benefits": "Health insurance, 401k, remote work",
  "employment_type": "Full-time",
  "required_experience": "Mid-Senior level",
  "required_education": "Bachelor's Degree",
  "industry": "Information Technology",
  "function": "Engineering",
  "telecommuting": 1,
  "has_company_logo": 1,
  "has_questions": 0
}
```

**Response:**
```json
{
  "prediction": "Real",
  "confidence": 0.9845,
  "probabilities": {
    "real": 0.9845,
    "fake": 0.0155
  },
  "risk_level": "Low"
}
```

### 4. Model Info
```
GET /model-info
```
Returns information about the loaded model and its performance.

## Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example Usage

### Using cURL

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Work from home - Easy money",
    "company_profile": "",
    "description": "Make $5000 per week from home! No experience needed!",
    "requirements": "Just need a computer",
    "benefits": "Unlimited income potential",
    "employment_type": "Full-time",
    "required_experience": "Entry level",
    "required_education": "High School",
    "industry": "Other",
    "function": "Other"
  }'
```

### Using Python

```python
import requests

url = "http://localhost:8000/predict"

data = {
    "title": "Senior Software Engineer",
    "company_profile": "Leading tech company",
    "description": "We are looking for an experienced software engineer...",
    "requirements": "5+ years Python, AWS experience",
    "benefits": "Health insurance, 401k",
    "employment_type": "Full-time",
    "required_experience": "Mid-Senior level",
    "required_education": "Bachelor's Degree",
    "industry": "Information Technology",
    "function": "Engineering",
    "telecommuting": 1,
    "has_company_logo": 1,
    "has_questions": 0
}

response = requests.post(url, json=data)
print(response.json())
```

### Using JavaScript (Axios)

```javascript
const axios = require('axios');

const data = {
  title: "Senior Software Engineer",
  company_profile: "Leading tech company",
  description: "We are looking for an experienced software engineer...",
  requirements: "5+ years Python, AWS experience",
  benefits: "Health insurance, 401k",
  employment_type: "Full-time",
  required_experience: "Mid-Senior level",
  required_education: "Bachelor's Degree",
  industry: "Information Technology",
  function: "Engineering",
  telecommuting: 1,
  has_company_logo: 1,
  has_questions: 0
};

axios.post('http://localhost:8000/predict', data)
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.error(error);
  });
```

## Model Performance

- **Accuracy**: 98.71%
- **F1-Score**: 0.8553
- **ROC-AUC**: 0.9969
- **Features**: 5000 TF-IDF + 22 engineered features

## Feature Engineering

The API automatically extracts:

**Text Features:**
- Text length, word count, average word length
- Individual field lengths (title, description, requirements, etc.)

**Pattern Features:**
- Email/URL/phone presence
- Uppercase ratio
- Special character count
- Exclamation marks

**Categorical Features:**
- Employment type
- Required experience
- Required education
- Industry
- Function

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Successful prediction
- `422`: Validation error (invalid input)
- `500`: Server error
- `503`: Service unavailable (model not loaded)

## Architecture

```
api/
├── app.py                 # FastAPI application
├── preprocessing.py       # Text preprocessing & feature engineering
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Next Steps

1. **Week 5**: Build React frontend to consume this API
2. **Week 6**: Containerize with Docker
3. **Week 7**: Deploy to cloud platform

## License

MIT License
