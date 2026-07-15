# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import uvicorn

# Initialize the API
app = FastAPI(
    title="AI-Driven Student Performance API",
    description="Backend server for academic prediction and analytics.",
    version="2.0.0"
)

# Pydantic schema for strict data validation (Enterprise standard)
class StudentData(BaseModel):
    study_hours: float
    attendance: float
    prev_score: float
    sleep_hours: float
    tutoring: int
    internet: str
    extracurricular: str

@app.get("/")
def read_root():
    return {"status": "Backend Server is Running Active"}

@app.post("/api/predict")
def predict_performance(data: StudentData):
    try:
        # In a full production environment, this passes to ml_engine.py
        # Here, we simulate the complex model calculation for the API response
        int_access = 1 if data.internet == "Yes" else 0
        extra_val = {"High": 3, "Medium": 2, "Low": 1}[data.extracurricular]
        
        base = 20
        academic = (data.study_hours * 0.8) + (data.attendance * 0.3) + (data.prev_score * 0.35)
        lifestyle = (data.sleep_hours * 2) + (data.tutoring * 1.5) + (int_access * 4) + (extra_val * 1.5)
        
        prediction = min(max(base + academic + lifestyle, 0), 100)
        
        # Determine Risk Tier
        if prediction >= 75:
            risk = "On Track"
        elif prediction >= 60:
            risk = "Borderline"
        else:
            risk = "At Risk"
            
        return {
            "predicted_score": round(prediction, 2),
            "risk_category": risk,
            "confidence_score": 92.4, # Simulated SHAP/Model confidence
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    # Runs the server locally on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)