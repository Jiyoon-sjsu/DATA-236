from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

MODEL_FILENAME = 'iris_model.pkl'
TARGET_NAMES_FILENAME = 'iris_target_names.pkl'
MODEL_PATH = os.path.join('.', MODEL_FILENAME)
TARGET_NAMES_PATH = os.path.join('.', TARGET_NAMES_FILENAME)


try:
    model = joblib.load(MODEL_PATH)
    target_names = joblib.load(TARGET_NAMES_PATH)
    print(f"Model '{MODEL_FILENAME}' and target names '{TARGET_NAMES_FILENAME}' loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model file '{MODEL_PATH}' or target names file '{TARGET_NAMES_PATH}' not found.")
    print("Please run model_training.py first to generate the model file.")
    model = None
    target_names = ["Model not loaded"] * 3
except Exception as e:
    print(f"Error loading model or target names: {e}")
    model = None
    target_names = ["Model load error"] * 3 

# FastAPI App Initialization
app = FastAPI(title="Iris Model API", description="API for predicting Iris species")


class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    # Example data for documentation
    class Config:
        schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }

@app.get("/", tags=["General"])
async def read_root():
    """Root endpoint providing basic API information."""
    return {"message": "Welcome to the Iris Prediction API!", "model_status": "loaded" if model else "not loaded"}

@app.post("/predict", tags=["Prediction"])
async def predict_iris(features: IrisFeatures):
    """
    Predict the Iris species based on input features.

    - **Input**: JSON object with sepal_length, sepal_width, petal_length, petal_width.
    - **Output**: JSON object with the predicted species index and name.
    """
    if model is None:
         raise HTTPException(status_code=503, detail="Model is not loaded. Cannot make predictions.")

    
    data = np.array([[
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width
    ]])

    try:
        prediction_index = model.predict(data)[0] 
        predicted_species = target_names[prediction_index] 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    return {
        "prediction_index": int(prediction_index),
        "predicted_species": predicted_species
        }


if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server...")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)