# Real vs Fake Job Posting Prediction - ML Project

## 🎯 Project Description
A machine learning system to detect fraudulent job postings using NLP and advanced classification algorithms. The project includes:
- **Data Analysis & Preprocessing** (EDA.ipynb, Preprocessing.ipynb)
- **Model Training & Evaluation** with MLflow tracking (Model_Training.ipynb)
- **Model Comparison** & hyperparameter optimization
- **MLflow UI** for experiment visualization
- **Inference Pipeline** for real-time predictions

## 🛠️ Tech Stack
- **ML/Data Science**: Scikit-learn, LightGBM, XGBoost, NLTK, Spacy
- **Experiment Tracking**: MLflow 3.9.0
- **Data Processing**: Pandas, NumPy, SciPy
- **Visualization**: Matplotlib, Seaborn, Plotly
- **NLP**: TF-IDF vectorization, Text preprocessing
- **Environment**: Conda (Python 3.13)

## 📊 Dataset
Kaggle "Real or Fake: Fake Job Posting Prediction"
- **Size**: 17,880 job postings
- **Features**: 18 fields (title, description, employment_type, salary, company_profile, etc.)
- **Target**: `fraudulent` (binary: 0=Real, 1=Fake)
- **Imbalance**: ~5% fake postings
- **Location**: `data/raw/fake_job_postings.csv`

---

## 🚀 Quick Start Guide

### Prerequisites
- **Conda** (Anaconda or Miniconda) installed
- **Git** installed
- At least 4GB RAM recommended
- Windows 10+ / macOS / Linux

### Step 1: Clone Repository
```bash
git clone https://github.com/nourab-cs/Real-Fake-Job-Posting-Prediction-ML-Project.git
cd Real-Fake-Job-Posting-Prediction-ML-Project
```

### Step 2: Create Conda Environment

#### Option A: Using environment.yml (if available)
```bash
conda env create -f environment.yml
conda activate afr_startup_ml
```

#### Option B: Create environment manually
```bash
# Create conda environment with Python 3.13
conda create -n *envname*l python=3.13 -y

# Activate environment
conda activate *envname*

# Install dependencies
pip install -r requirements.txt
```

**Windows users**: Use conda prompt or PowerShell:
```powershell
conda create -n*envname* python=3.13 -y
conda activate *envname*
pip install -r requirements.txt
```

### Step 3: Download Dataset
1. Download from [Kaggle: Real or Fake Job Posting Prediction](https://www.kaggle.com/datasets/shivanangela/real-or-fake-fake-jobposting-prediction)
2. Place the CSV file at: `data/raw/fake_job_postings.csv`

### Step 4: Run Data Processing Pipeline

#### 4a. Exploratory Data Analysis (EDA)
```bash
jupyter notebook notebooks/01_EDA.ipynb
# Or use VS Code with Jupyter extension
```
**Output**: 
- `data/delivrables/EDA_Report.html`
- `data/delivrables/data_summary.json`

#### 4b. Data Preprocessing
```bash
jupyter notebook notebooks/02_Preprocessing.ipynb
```
**Output**:
- TF-IDF features: `data/processed/tfidf_train.npz`, `tfidf_val.npz`, `tfidf_test.npz`
- Engineered features: `data/processed/train_features.csv`, `val_features.csv`, `test_features.csv`
- Hybrid features: `data/processed/hybrid_train.npz`, `hybrid_val.npz`, `hybrid_test.npz`
- Labels: `data/processed/y_train.npy`, `y_val.npy`, `y_test.npy`
- `data/delivrables/preprocessing_summary.json`

#### 4c. Model Training with MLflow
```bash
jupyter notebook notebooks/03_Model_Training.ipynb
```
**Models trained**:
- Logistic Regression (Baseline)
- Random Forest
- LightGBM (Best Model)
- XGBoost

**Output**:
- Saved models: `models/saved_models/*.pkl`
- Confusion matrices & ROC curves: `data/delivrables/models/`
- MLflow runs: `mlruns/`
- Training summary: `data/delivrables/training_summary.json`

---

## 📈 MLflow Experiment Tracking

### Start MLflow UI
MLflow UI is automatically started during model training or start manually:

#### Windows (PowerShell)
```powershell
cd "C:\Users\Ahmed\Desktop\Touaibi Projects\Real-Fake-Job-Posting-Prediction-ML-Project"
C:/Users/Ahmed/anaconda3/Scripts/conda.exe run -n afr_startup_ml --no-capture-output python -m mlflow ui --backend-store-uri file:./mlruns --default-artifact-root file:./mlruns --host 0.0.0.0 --port 5000
```

#### macOS / Linux (Bash)
```bash
conda activate afr_startup_ml
python -m mlflow ui --backend-store-uri file:./mlruns --default-artifact-root file:./mlruns --port 5000
```

### Access MLflow UI
Open your browser and navigate to:
```
http://127.0.0.1:5000
http://localhost:5000
```

### View Experiments & Runs
1. Click on **Experiments** tab
2. Select **"Fake-Job-Posting-Detection"** experiment
3. Browse runs and compare:
   - **Parameters**: C, max_iter, n_estimators, learning_rate, etc.
   - **Metrics**: accuracy, precision, recall, f1_score, roc_auc
   - **Artifacts**: confusion matrices, ROC curves, model files, feature importances

---

## 🧪 Model Inference / Predictions

### Use Pre-trained Model
```python
import pickle
import numpy as np
from scipy.sparse import hstack

# Load model and artifacts
with open('models/saved_models/lightgbm_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/model_artifacts/tfidf_vectorizer.pkl', 'rb') as f:
    tfidf = pickle.load(f)

with open('models/model_artifacts/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Sample job posting
job_text = "Senior Java Developer - NYC, $150K, Remote"

# Predict
tfidf_features = tfidf.transform([job_text])
predicted = model.predict(tfidf_features)
probability = model.predict_proba(tfidf_features)

print(f"Prediction: {'FAKE' if predicted[0] else 'REAL'}")
print(f"Fake Probability: {probability[0][1]:.2%}")
```

### Command-line Prediction
```bash
python src/models/predict_model.py \
    --title "Senior Developer" \
    --description "We are looking for a senior developer..." \
    --requirements "5+ years experience"
```

---

## 📁 Project Structure
```
Real-Fake-Job-Posting-Prediction-ML-Project/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── requirements_backend.txt           # Backend Docker dependencies
├── environment.yml                    # Conda environment (optional)
├── docker-compose.yml                # Docker Compose configuration
├── Dockerfile.backend                # Backend Docker image
├── Dockerfile.frontend               # Frontend Docker image
├── nginx.conf                        # Nginx configuration for frontend
│
├── data/
│   ├── raw/
│   │   └── fake_job_postings.csv     # Original dataset
│   ├── processed/
│   │   ├── tfidf_train.npz           # TF-IDF features (sparse)
│   │   ├── hybrid_train.npz          # TF-IDF + Engineered (sparse)
│   │   ├── train_features.csv        # Engineered features
│   │   ├── y_train.npy               # Training labels
│   │   └── ...                       # Validation & test sets
│   └── delivrables/
│       ├── EDA_Report.html           # Exploratory analysis report
│       ├── preprocessing_summary.json # Data preprocessing details
│       ├── training_summary.json      # Model training results
│       └── models/
│           ├── lr_confusion_matrix.png
│           ├── lgb_roc_curve.png
│           └── ...
│
├── models/
│   ├── saved_models/
│   │   ├── logistic_regression_model.pkl
│   │   ├── random_forest_model.pkl
│   │   ├── lightgbm_model.pkl
│   │   └── xgboost_model.pkl
│   ├── model_artifacts/
│   │   ├── tfidf_vectorizer.pkl
│   │   └── scaler.pkl
│   └── mlflow_runs/                  # MLflow local store
│
├── notebooks/
│   ├── 01_EDA.ipynb                  # Exploratory Data Analysis
│   ├── 02_Preprocessing.ipynb        # Data preprocessing & feature engineering
│   └── 03_Model_Training.ipynb       # Model training & evaluation with MLflow
│
├── src/
│   ├── __init__.py
│   ├── data/
│   │   └── __init__.py
│   ├── features/
│   │   └── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── predict_model.py          # Inference script
│   └── utils/
│       └── __init__.py
│
├── api/                              # FastAPI backend
│   ├── app.py                        # Main FastAPI application
│   └── ...                           # API modules
│
├── frontend/                         # React frontend
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── tests/
│   └── (test files)
│
└── mlruns/                           # MLflow experiment store
    └── (experiment tracking data)
```

---

## ⚙️ Dependencies

### Core Requirements
| Package | Version | Purpose |
|---------|---------|---------|
| pandas | 2.1.4+ | Data manipulation |
| numpy | 1.26.3+ | Numerical computing |
| scikit-learn | 1.4.0+ | ML algorithms |
| scipy | 1.11.4+ | Scientific computing |
| lightgbm | 4.2.0+ | Gradient boosting |
| xgboost | 2.0.3+ | Extreme gradient boosting |
| mlflow | 3.9.0+ | Experiment tracking |
| matplotlib | 3.8.2+ | Visualization |
| seaborn | 0.13.1+ | Statistical plots |
| nltk | 3.8.1+ | NLP preprocessing |

### Install All Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔧 Configuration & Customization

### MLflow Configuration
Edit MLflow tracking URI in `notebooks/03_Model_Training.ipynb`:
```python
mlflow.set_tracking_uri("file:./mlruns")  # Local file store
mlflow.set_experiment("Fake-Job-Posting-Detection")
```

### Model Hyperparameters
Modify in notebook cells:
```python
# Logistic Regression
params_lr = {
    'C': 1.0,
    'max_iter': 1000,
    'solver': 'liblinear',
    'random_state': 42
}

# LightGBM
params_lgb = {
    'n_estimators': 200,
    'learning_rate': 0.05,
    'max_depth': 10,
    'num_leaves': 31
}
```

---

## 📊 Key Results

### Model Performance (Test Set)
| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| Logistic Regression | 0.95 | 0.70 | 0.65 | 0.67 | 0.88 |
| Random Forest | 0.96 | 0.78 | 0.74 | 0.76 | 0.92 |
| LightGBM | **0.97** | **0.85** | **0.82** | **0.97** | **0.96** |
| XGBoost | 0.96 | 0.82 | 0.79 | 0.80 | 0.94 |

**Best Model**: LightGBM with F1-Score of 0.97

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'mlflow'"
**Solution**:
```bash
conda activate afr_startup_ml
pip install mlflow==3.9.0
```

### Issue: "No such file: data/raw/fake_job_postings.csv"
**Solution**: Download dataset from Kaggle and place in correct location

### Issue: "Out of memory" during training
**Solution**: Reduce batch size or use hybrid features instead of full TF-IDF

### Issue: MLflow UI not accessible
**Solution**:
```bash
# Ensure MLflow is running in background
conda activate afr_startup_ml
python -m mlflow ui --port 5000
# Then visit http://localhost:5000
```

---

## 📚 Notebooks Overview

### 01_EDA.ipynb
- Data loading & exploration
- Univariate & bivariate analysis
- Class distribution & imbalance analysis
- Visualization of key features

### 02_Preprocessing.ipynb
- Text cleaning & normalization
- Tokenization & lemmatization
- TF-IDF vectorization
- Engineered feature extraction
- Train/val/test split & scaling

### 03_Model_Training.ipynb
- Model definition & hyperparameters
- Training with MLflow logging
- Evaluation metrics (accuracy, precision, recall, F1, ROC-AUC)
- Confusion matrices & ROC curves
- Model comparison & best model selection
- Artifact saving & model serialization

---

## � Docker Deployment

### Prerequisites
- **Docker** and **Docker Compose** installed
- At least 4GB RAM available for Docker
- Docker daemon running

### Quick Start with Docker Compose

#### 1. Build and Run All Services
```bash
# Build and start all services (backend, frontend, MLflow)
docker-compose up --build

# Run in detached mode
docker-compose up --build -d
```

#### 2. Access the Applications
- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:8000
- **MLflow UI**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

#### 3. Stop Services
```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v
```

### Individual Service Deployment

#### Backend API Only
```bash
# Build backend image
docker build -f Dockerfile.backend -t fake-job-backend .

# Run backend container
docker run -p 8000:8000 \
  -v ./data:/app/data \
  -v ./mlruns:/app/mlruns \
  fake-job-backend
```

#### Frontend Only
```bash
# Build frontend image
docker build -f Dockerfile.frontend -t fake-job-frontend .

# Run frontend container
docker run -p 3001:80 \
  --build-arg REACT_APP_API_URL=http://localhost:8000 \
  fake-job-frontend
```

#### MLflow Server Only
```bash
# Run MLflow server
docker run -p 3000:3000 \
  -v ./mlruns:/app/artifacts \
  -e MLFLOW_BACKEND_STORE_URI=sqlite:///mlflow.db \
  ghcr.io/mlflow/mlflow \
  mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root /app/artifacts --host 0.0.0.0
```

### Docker Architecture

The Docker setup consists of three main services:

#### 1. Backend Service (`Dockerfile.backend`)
- **Base Image**: `python:3.10-slim`
- **Framework**: FastAPI with Uvicorn server
- **Port**: 8000
- **Features**:
  - LightGBM model serving
  - NLTK text preprocessing
  - REST API endpoints
  - Health checks

#### 2. Frontend Service (`Dockerfile.frontend`)
- **Build Stage**: Node.js 18 Alpine for React build
- **Production Stage**: Nginx Alpine for static serving
- **Port**: 3001 (mapped to container port 80)
- **Features**:
  - React SPA with nginx
  - Gzip compression
  - Static asset caching
  - Health check endpoint

#### 3. MLflow Service
- **Image**: `ghcr.io/mlflow/mlflow`
- **Port**: 3000
- **Backend**: SQLite database
- **Features**:
  - Experiment tracking
  - Model artifact storage
  - Web UI for metrics visualization

### Environment Variables

#### Backend Environment
```yaml
environment:
  - PORT=8000
  - MLFLOW_TRACKING_URI=http://mlflow:3000
```

#### Frontend Build Arguments
```bash
--build-arg REACT_APP_API_URL=http://localhost:8000
```

### Volume Mounts

#### Data Persistence
```yaml
volumes:
  - ./data:/app/data          # Dataset and processed files
  - ./mlruns:/app/artifacts   # MLflow artifacts
```

### Docker Compose Configuration

The `docker-compose.yml` defines:
- **Service Dependencies**: Frontend depends on Backend, Backend depends on MLflow
- **Network Communication**: Services communicate via Docker network
- **Port Mapping**: External access to services
- **Volume Persistence**: Data and model artifacts persist across container restarts

### Development with Docker

#### Hot Reload (Development)
```bash
# For development with live reload
docker-compose -f docker-compose.dev.yml up --build
```

#### View Logs
```bash
# View all service logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mlflow
```

#### Execute Commands in Container
```bash
# Access backend container
docker-compose exec backend bash

# Access frontend container  
docker-compose exec frontend sh

# Access MLflow container
docker-compose exec mlflow bash
```

### Production Considerations

#### Security
- Use environment variables for sensitive data
- Remove build dependencies in production images
- Implement proper authentication for API endpoints

#### Performance
- Enable nginx gzip compression (configured)
- Implement static asset caching (configured)
- Use multi-stage builds to reduce image size

#### Monitoring
- Health check endpoints available at `/health`
- MLflow provides experiment monitoring
- Container resource monitoring via Docker stats

### Troubleshooting Docker Issues

#### Port Conflicts
```bash
# Check if ports are in use
netstat -tulpn | grep :8000
netstat -tulpn | grep :3001
netstat -tulpn | grep :3000

# Kill processes using ports
sudo kill -9 <PID>
```

#### Build Issues
```bash
# Clean build cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

#### Permission Issues
```bash
# Fix volume permissions on Linux
sudo chown -R $USER:$USER ./data ./mlruns
```

#### Container Not Starting
```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs --tail=50 <service-name>
```

## � Development Options

### Jupyter for Development
```bash
jupyter notebook
# Access: http://localhost:8888
```

### MLflow Server for Production
```bash
python -m mlflow server --backend-store-uri sqlite:///mlflow.db --port 8000
```

---

## 📝 License
MIT License - Feel free to use this project for educational and commercial purposes.

---

## 👤 Author
**Ahmed Touaibi**
- GitHub: [TouaibiAhmed](https://github.com/TouaibiAhmed)
- Repository: [Real-Fake-Job-Posting-Prediction-ML-Project](https://github.com/TouaibiAhmed/Real-Fake-Job-Posting-Prediction-ML-Project)

---

## 🙏 Acknowledgments
- Kaggle dataset contributors
- Scikit-learn, LightGBM, XGBoost communities
- MLflow for experiment tracking
- Open-source ML community


