"""
Generate tfidf_idf.npy from tfidf_vectorizer.pkl to fix "idf vector is not fitted" error.
Run once from project root:  python scripts/fix_tfidf_idf.py
"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import numpy as np

tfidf_path = project_root / "models" / "model_artifacts" / "tfidf_vectorizer.pkl"
idf_path = project_root / "models" / "model_artifacts" / "tfidf_idf.npy"

if not tfidf_path.exists():
    print(f"Error: {tfidf_path} not found. Run 02_Preprocessing.ipynb first.")
    sys.exit(1)

import pickle
with open(tfidf_path, "rb") as f:
    vec = pickle.load(f)
idf_arr = vec.idf_
np.save(idf_path, idf_arr)
print(f"Saved tfidf_idf.npy ({len(idf_arr)} values)")
print("Restart the API and try /predict again.")
