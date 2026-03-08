"""
Preprocessing utilities for job posting text data
"""
import re
import string
import numpy as np
import pandas as pd
from typing import Dict, List
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK data if not already downloaded
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/wordnet')
except (LookupError, OSError):
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

# Initialize NLTK components
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def clean_text(text: str) -> str:
    """
    Clean and preprocess text data
    
    Steps:
    1. Convert to lowercase
    2. Remove URLs
    3. Remove email addresses
    4. Remove HTML tags
    5. Remove special characters
    6. Tokenization
    7. Remove stopwords
    8. Lemmatization
    """
    if not text or pd.isna(text):
        return ""
    
    # Convert to string and lowercase
    text = str(text).lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and len(word) > 2]
    
    return ' '.join(tokens)


def extract_text_features(text: str) -> Dict[str, float]:
    """Extract statistical features from text"""
    if not text or pd.isna(text):
        return {
            'length': 0,
            'word_count': 0,
            'avg_word_length': 0
        }
    
    text = str(text)
    words = text.split()
    
    return {
        'length': len(text),
        'word_count': len(words),
        'avg_word_length': np.mean([len(word) for word in words]) if words else 0
    }


def extract_pattern_features(text: str) -> Dict[str, int]:
    """Extract pattern-based features"""
    if not text or pd.isna(text):
        return {
            'has_email': 0,
            'has_url': 0,
            'has_phone': 0,
            'uppercase_ratio': 0.0,
            'special_char_count': 0,
            'exclamation_count': 0
        }
    
    text = str(text)
    
    return {
        'has_email': int(bool(re.search(r'\S+@\S+', text))),
        'has_url': int(bool(re.search(r'http\S+|www\S+', text))),
        'has_phone': int(bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text))),
        'uppercase_ratio': sum(1 for c in text if c.isupper()) / len(text) if len(text) > 0 else 0,
        'special_char_count': sum(1 for c in text if c in string.punctuation),
        'exclamation_count': text.count('!')
    }


def extract_country(location: str) -> str:
    """Extract country from location string"""
    if not isinstance(location, str) or location == '':
        return 'Unknown'
    
    # Common patterns: "City, State, Country" or "City, Country"
    parts = [p.strip() for p in location.split(',')]
    
    if len(parts) >= 2:
        return parts[-1]  # Last part is usually country
    return location


def engineer_features(data: Dict[str, str]) -> np.ndarray:
    """
    Engineer all features from raw job posting data
    
    Returns a feature vector matching the training pipeline
    """
    # Extract text from each field
    title = data.get('title', '')
    company_profile = data.get('company_profile', '')
    description = data.get('description', '')
    requirements = data.get('requirements', '')
    benefits = data.get('benefits', '')
    location = data.get('location', '')
    
    # Combine all text for TF-IDF
    combined_text = ' '.join([
        str(title),
        str(company_profile),
        str(description),
        str(requirements),
        str(benefits)
    ])
    
    # Clean the combined text
    cleaned_text = clean_text(combined_text)
    
    # Extract features for each field
    title_features = extract_text_features(title)
    description_features = extract_text_features(description)
    requirements_features = extract_text_features(requirements)
    benefits_features = extract_text_features(benefits)
    company_profile_features = extract_text_features(company_profile)
    combined_features = extract_text_features(combined_text)
    
    # Extract pattern features from combined text
    pattern_features = extract_pattern_features(combined_text)
    
    # Location features
    country = extract_country(location)
    has_location = 1 if location and str(location).strip() != '' else 0
    
    # Top 5 countries based on training data
    top_countries = ['US', 'GB', 'IN', 'CA', 'AU']  # US, Great Britain, India, Canada, Australia
    country_features = {}
    for top_country in top_countries:
        feature_name = f'is_{top_country.lower()}'
        country_features[feature_name] = 1 if country == top_country else 0
    
    # Create feature array (must match training order)
    feature_dict = {
        # Boolean features (first in feature_columns)
        'telecommuting': int(data.get('telecommuting', 0)),
        'has_company_logo': int(data.get('has_company_logo', 0)),
        'has_questions': int(data.get('has_questions', 0)),
        
        # Text length features
        'text_length': combined_features['length'],
        'word_count': combined_features['word_count'],
        'avg_word_length': combined_features['avg_word_length'],
        'title_length': title_features['length'],
        'description_length': description_features['length'],
        'requirements_length': requirements_features['length'],
        'benefits_length': benefits_features['length'],
        'company_profile_length': company_profile_features['length'],
        
        # Pattern features
        'has_email': pattern_features['has_email'],
        'has_url': pattern_features['has_url'],
        'has_phone': pattern_features['has_phone'],
        'uppercase_ratio': pattern_features['uppercase_ratio'],
        'special_char_count': pattern_features['special_char_count'],
        'exclamation_count': pattern_features['exclamation_count'],
        
        # Categorical features (will be encoded by label encoders)
        'employment_type': data.get('employment_type', 'Unknown'),
        'required_experience': data.get('required_experience', 'Unknown'),
        'required_education': data.get('required_education', 'Unknown'),
        'industry': data.get('industry', 'Unknown'),
        'function': data.get('function', 'Unknown'),
        
        # Location features
        'has_location': has_location,
        **country_features  # Add is_us, is_gb, is_in, is_ca, is_au
    }
    
    return cleaned_text, feature_dict
