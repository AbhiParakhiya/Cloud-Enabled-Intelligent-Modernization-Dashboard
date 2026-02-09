from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
import uvicorn
import os

app = FastAPI(title="Intelligent Analytics API", description="API for predicting customer risk and demand.")

# Load Models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, '../ml_core/models')
try:
    with open(f'{MODEL_DIR}/logistic_regression.pkl', 'rb') as f:
        lr_model = pickle.load(f)
    with open(f'{MODEL_DIR}/random_forest.pkl', 'rb') as f:
        rf_model = pickle.load(f)
    with open(f'{MODEL_DIR}/kmeans.pkl', 'rb') as f:
        kmeans_model = pickle.load(f)
    print("Models loaded successfully.")
except FileNotFoundError:
    print("Models not found. Please run train_models.py first.")
    lr_model = None
    rf_model = None
    kmeans_model = None

class TransactionInput(BaseModel):
    tx_hour: int
    tx_day_of_week: int
    account_age_days: int
    amount: float

@app.get("/")
def home():
    return {"message": "Intelligent Analytics API is running."}

@app.post("/predict/risk")
def predict_risk(data: TransactionInput):
    if not lr_model:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    
    # Prepare features for LR/RF (excluding amount if not used, but check training script)
    # Training used: ['tx_hour', 'tx_day_of_week', 'account_age_days']
    features = [[data.tx_hour, data.tx_day_of_week, data.account_age_days]]
    
    risk_prob = lr_model.predict_proba(features)[0][1] # Probability of 'is_high_value' (or risk class)
    prediction = lr_model.predict(features)[0]
    
    return {
        "risk_score": float(risk_prob),
        "is_high_risk": bool(prediction) # In our proxy, high value might be high priority/risk depending on definition
    }

@app.post("/predict/segment")
def predict_segment(data: TransactionInput):
    if not kmeans_model:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    
    # Training used: ['amount', 'tx_hour']
    features = [[data.amount, data.tx_hour]]
    cluster = kmeans_model.predict(features)[0]
    
    return {"segment_cluster": int(cluster)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
