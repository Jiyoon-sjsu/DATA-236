from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import numpy as np
import os

app = FastAPI()

# Allow all CORS origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File paths
MODEL_PATH = "FastAPI/score_predictor.pkl"
DATA_PATH = "student_performance_dataset.csv"

# Pydantic input model
class ScoreInput(BaseModel):
    study_hours: float
    attendance: float

# Train model function
def train_model():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    X = df[['StudyHours', 'Attendance']]
    y = df['Score']

    model = LinearRegression()
    model.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print(f"Model trained on {len(df)} records")
    print(f"   Coefficients: {model.coef_}")
    print(f"   Intercept: {model.intercept_}")
    return model

# Load model at startup
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("Loaded existing model from file.")
else:
    model = train_model()

# Predict endpoint
@app.post("/predict")
async def predict_score(data: ScoreInput):
    try:
        features = np.array([[data.study_hours, data.attendance]])
        prediction = model.predict(features)[0]
        rounded_score = round(prediction, 2)

        print(f"Predicting with Study Hours: {data.study_hours}, Attendance: {data.attendance}")
        print(f"Predicted Score: {rounded_score}")

        # Print the predicted data for logging purposes
        print(f"Predicted data: Study Hours = {data.study_hours}, Attendance = {data.attendance}, Predicted Score = {rounded_score}")

        return {
            "input": {
                "study_hours": data.study_hours,
                "attendance": data.attendance
            },
            "predicted_score": rounded_score
        }
    except Exception as e:
        print("Prediction error:", e)
        return {"error": str(e)}

# Retrain endpoint
@app.post("/train")
async def retrain_model():
    try:
        new_model = train_model()
        sample_input = np.array([[5, 90]])
        sample_pred = new_model.predict(sample_input)[0]
        return {
            "message": "Model retrained successfully.",
            "sample_prediction": {
                "study_hours": 5,
                "attendance": 90,
                "predicted_score": round(sample_pred, 2)
            }
        }
    except Exception as e:
        print("Retrain error:", e)
        return {"error": str(e)}
