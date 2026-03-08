
"""
Model Inference Script for Fake Job Posting Detection
Usage: python predict.py --text "job posting text"
"""

import pickle
import numpy as np
from scipy.sparse import hstack
import argparse

class JobPostingPredictor:
    def __init__(self, model_path, tfidf_path, scaler_path):
        # Load model and preprocessing artifacts
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)

        with open(tfidf_path, 'rb') as f:
            self.tfidf = pickle.load(f)

        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)

    def preprocess_text(self, text):
        """Simple text preprocessing"""
        return text.lower().strip()

    def extract_features(self, job_data):
        """Extract features from job posting"""
        # Combine text
        full_text = f"{job_data.get('title', '')} {job_data.get('description', '')} {job_data.get('requirements', '')}"
        full_text = self.preprocess_text(full_text)

        # TF-IDF features
        tfidf_features = self.tfidf.transform([full_text])

        # Engineered features (simplified)
        eng_features = np.array([[
            len(full_text),  # text_length
            len(full_text.split()),  # word_count
            len(full_text) / (len(full_text.split()) + 1),  # avg_word_length
            '@' in full_text,  # has_email
            'http' in full_text or 'www' in full_text,  # has_url
            full_text.count('!'),  # exclamation_count
        ]])

        # Pad to match training feature count
        padded_features = np.zeros((1, 26))  # Adjust based on your feature count
        padded_features[0, :eng_features.shape[1]] = eng_features[0]

        # Scale features
        scaled_features = self.scaler.transform(padded_features)

        # Combine
        combined = hstack([tfidf_features, scaled_features])

        return combined

    def predict(self, job_data):
        """Predict if job posting is fake"""
        features = self.extract_features(job_data)
        proba = self.model.predict(features)[0]

        is_fake = proba > 0.5
        confidence = proba if is_fake else (1 - proba)

        return {
            'prediction': 'FAKE' if is_fake else 'REAL',
            'confidence': float(confidence),
            'probability_fake': float(proba),
            'probability_real': float(1 - proba)
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', type=str, required=True)
    parser.add_argument('--description', type=str, required=True)
    parser.add_argument('--requirements', type=str, default='')
    args = parser.parse_args()

    # Initialize predictor
    predictor = JobPostingPredictor(
        model_path='../models/saved_models/lightgbm_model.pkl',
        tfidf_path='../models/model_artifacts/tfidf_vectorizer.pkl',
        scaler_path='../models/model_artifacts/scaler.pkl'
    )

    # Make prediction
    result = predictor.predict({
        'title': args.title,
        'description': args.description,
        'requirements': args.requirements
    })

    print(f"\nPrediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']*100:.2f}%")
