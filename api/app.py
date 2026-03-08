"""
FastAPI application for Fake Job Posting Detection
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict
import pickle
import joblib
import numpy as np
import scipy.sparse as sp
from pathlib import Path
import logging

from api.preprocessing import engineer_features
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Fake Job Posting Detection API",
    description="API for predicting whether a job posting is real or fake using ML",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models" / "saved_models"
ARTIFACTS_DIR = BASE_DIR / "models" / "model_artifacts"

# Global variables for model and artifacts
model = None
tfidf_vectorizer = None
label_encoders = None
scaler = None


class JobPosting(BaseModel):
    """Job posting input schema"""
    title: str = Field(..., description="Job title")
    company_profile: Optional[str] = Field("", description="Company description")
    description: str = Field(..., description="Job description")
    requirements: Optional[str] = Field("", description="Job requirements")
    benefits: Optional[str] = Field("", description="Benefits offered")
    employment_type: Optional[str] = Field("Unknown", description="Employment type")
    required_experience: Optional[str] = Field("Unknown", description="Required experience level")
    required_education: Optional[str] = Field("Unknown", description="Required education")
    industry: Optional[str] = Field("Unknown", description="Industry")
    function: Optional[str] = Field("Unknown", description="Job function")
    location: Optional[str] = Field("", description="Job location")
    telecommuting: Optional[int] = Field(0, description="Remote work option")
    has_company_logo: Optional[int] = Field(0, description="Has company logo")
    has_questions: Optional[int] = Field(0, description="Has screening questions")


class PredictionResponse(BaseModel):
    """Prediction response schema"""
    prediction: str = Field(..., description="Real or Fake")
    confidence: float = Field(..., description="Confidence score (0-1)")
    probabilities: Dict[str, float] = Field(..., description="Probability for each class")
    risk_level: str = Field(..., description="Risk assessment (Low/Medium/High)")


@app.on_event("startup")
async def load_model_and_artifacts():
    """Load model and preprocessing artifacts on startup"""
    global model, tfidf_vectorizer, label_encoders, scaler
    
    try:
        logger.info("Loading model and artifacts...")
        
        # Load the best model (LightGBM)
        model_path = MODEL_DIR / "lightgbm_model.pkl"
        model = joblib.load(model_path)
        logger.info(f"✅ Model loaded from {model_path}")
        
        # Load TF-IDF vectorizer (use pickle to match notebook's pickle.dump for compatibility)
        tfidf_path = ARTIFACTS_DIR / "tfidf_vectorizer.pkl"
        with open(tfidf_path, "rb") as f:
            tfidf_vectorizer = pickle.load(f)
        # Repair: if idf_ is not properly fitted (cross-env pickle issue), restore from backup
        idf_backup_path = ARTIFACTS_DIR / "tfidf_idf.npy"
        try:
            _ = tfidf_vectorizer.transform(["test"])
        except Exception as e:
            if "idf" in str(e).lower() and idf_backup_path.exists():
                idf_arr = np.load(idf_backup_path)
                tfidf_vectorizer.idf_ = idf_arr
                logger.info("✅ TF-IDF idf_ restored from backup (tfidf_idf.npy)")
            else:
                raise
        logger.info(f"✅ TF-IDF vectorizer loaded from {tfidf_path}")
        
        # Load label encoders
        encoders_path = ARTIFACTS_DIR / "label_encoders.pkl"
        label_encoders = joblib.load(encoders_path)
        logger.info(f"✅ Label encoders loaded from {encoders_path}")
        
        # Load scaler
        scaler_path = ARTIFACTS_DIR / "scaler.pkl"
        scaler = joblib.load(scaler_path)
        logger.info(f"✅ Scaler loaded from {scaler_path}")
        
        logger.info("🚀 All models and artifacts loaded successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error loading model/artifacts: {str(e)}")
        raise


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Fake Job Posting Detection API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "tfidf_loaded": tfidf_vectorizer is not None,
        "encoders_loaded": label_encoders is not None,
        "scaler_loaded": scaler is not None
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(job: JobPosting):
    """
    Predict whether a job posting is real or fake
    
    Args:
        job: JobPosting object with job details
        
    Returns:
        PredictionResponse with prediction, confidence, and risk level
    """
    try:
        # Check if model is loaded
        if model is None or tfidf_vectorizer is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Convert input to dict
        job_data = job.dict()
        
        # Engineer features
        cleaned_text, feature_dict = engineer_features(job_data)
        
        # Create TF-IDF features
        tfidf_features = tfidf_vectorizer.transform([cleaned_text])
        
        # Feature order must match training:
        # 1. Boolean features (3)
        # 2. Text length features (8)
        # 3. Pattern features (6)
        # 4. Encoded categorical (5)
        # 5. Location features (1 + 5 = 6)
        # Total: 28 features
        
        # Encode categorical features
        categorical_encoded = []
        for col in ['employment_type', 'required_experience', 'required_education', 'industry', 'function']:
            value = feature_dict[col]
            encoder = label_encoders[col]
            
            # Handle unseen categories
            if value not in encoder.classes_:
                # Use the most frequent class or a default
                encoded_value = encoder.transform(['Unknown'])[0] if 'Unknown' in encoder.classes_ else 0
            else:
                encoded_value = encoder.transform([value])[0]
            
            categorical_encoded.append(encoded_value)
        
        # Construct feature array in exact training order
        engineered_features = [
            # Boolean features (3)
            feature_dict['telecommuting'],
            feature_dict['has_company_logo'],
            feature_dict['has_questions'],
            
            # Text length features (8)
            feature_dict['text_length'],
            feature_dict['word_count'],
            feature_dict['avg_word_length'],
            feature_dict['title_length'],
            feature_dict['description_length'],
            feature_dict['requirements_length'],
            feature_dict['benefits_length'],
            feature_dict['company_profile_length'],
            
            # Pattern features (6)
            feature_dict['has_email'],
            feature_dict['has_url'],
            feature_dict['has_phone'],
            feature_dict['uppercase_ratio'],
            feature_dict['special_char_count'],
            feature_dict['exclamation_count'],
            
            # Encoded categorical (5)
            *categorical_encoded,
            
            # Location features (6)
            feature_dict['has_location'],
            feature_dict['is_us'],
            feature_dict['is_gb'],
            feature_dict['is_in'],
            feature_dict['is_ca'],
            feature_dict['is_au'],
        ]
        
        # Convert to numpy array
        engineered_features = np.array(engineered_features).reshape(1, -1)
        
        # Scale the engineered features
        engineered_features_scaled = scaler.transform(engineered_features)
        
        # Combine TF-IDF and engineered features (hybrid approach)
        hybrid_features = sp.hstack([tfidf_features, engineered_features_scaled])
        
        # Make prediction
        # LightGBM Booster uses .predict() for probabilities (returns probability of class 1)
        y_proba = model.predict(hybrid_features, num_iteration=model.best_iteration)
        
        # Get probability of positive class (fake = 1)
        if isinstance(y_proba, np.ndarray):
            fake_prob = float(y_proba[0])
        else:
            fake_prob = float(y_proba)
        
        real_prob = 1 - fake_prob
        
        # Determine prediction (threshold = 0.5)
        prediction = 1 if fake_prob > 0.5 else 0
        probabilities = np.array([real_prob, fake_prob])
        
        # Interpret results
        prediction_label = "Real" if prediction == 0 else "Fake"
        confidence = float(max(probabilities))
        
        # Determine risk level
        fake_probability = float(probabilities[1])
        if fake_probability < 0.3:
            risk_level = "Low"
        elif fake_probability < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return PredictionResponse(
            prediction=prediction_label,
            confidence=confidence,
            probabilities={
                "real": float(probabilities[0]),
                "fake": float(probabilities[1])
            },
            risk_level=risk_level
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/model-info")
async def model_info():
    """Get information about the loaded model"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": "LightGBM",
        "features": "Hybrid (TF-IDF + Engineered)",
        "performance": {
            "test_accuracy": 0.9871,
            "test_f1": 0.8553,
            "test_roc_auc": 0.9969
        },
        "tfidf_vocabulary_size": len(tfidf_vectorizer.vocabulary_) if tfidf_vectorizer else 0,
        "total_features": tfidf_vectorizer.max_features if tfidf_vectorizer else 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
