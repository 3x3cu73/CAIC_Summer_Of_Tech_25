from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Literal
import numpy as np
import pandas as pd
import joblib
import uvicorn

# Define the request schema using Pydantic
class PredictionRequest(BaseModel):
    word_count: int
    char_count: int
    has_media: Literal[0, 1]
    hour: int
    sentiment: float

# Initialize FastAPI app
app = FastAPI()


model = joblib.load("like_predictor.pkl")

# Define the prediction route
@app.post("/predict")
async def predict(data: PredictionRequest):
    # Convert input data to NumPy array
    features = pd.DataFrame([{
        "word_count": data.word_count,
        "char_count": data.char_count,
        "has_media": data.has_media,
        "hour": data.hour,
        "sentiment": data.sentiment
    }])

    # Make prediction
    prediction = model.predict(features)[0]

    # Return result as JSON
    return {"predicted_likes": int(prediction)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
