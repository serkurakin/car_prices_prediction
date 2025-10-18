from fastapi import FastAPI, Request
import pickle
import pandas as pd
from pydantic import BaseModel
import uvicorn
import joblib
import os

app = FastAPI(title=os.getenv("APP_NAME", "Default App"))

# Использование переменных окружения
MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")


# Загрузка модели из файла pickle
model = joblib.load("model.pkl")

# Счетчик запросов
request_count = 0

# Модель для валидации входных данных
class PredictionInput(BaseModel):
    vehicle_type: str
    registration_year: int
    gearbox: str
    power: int
    model: str
    kilometer: int
    fuel_type: str
    brand: str
    repaired: str   

@app.get("/")
def read_root():
    return {
        "app_name": os.getenv("APP_NAME"),
        "environment": ENVIRONMENT
    }

@app.get("/stats")
def stats():
    return {"request_count": request_count}

@app.get("/health")
def health():
    return {"status": "OK"}

@app.post("/predict_model")
def predict_model(input_data: PredictionInput):
    global request_count
    request_count += 1

    # Создание DataFrame из данных
    new_data = pd.DataFrame({
        'vehicle_type': [input_data.vehicle_type],
        'registration_year': [input_data.registration_year],
        'gearbox': [input_data.gearbox],
        'power': [input_data.power],
        'model': [input_data.model],
        'kilometer': [input_data.kilometer],
        'fuel_type': [input_data.fuel_type],
        'brand': [input_data.brand],
        'repaired': [input_data.repaired]
    })

    # Предсказание
    predictions = model.predict(new_data)
    prediction_value = float(predictions.tolist()[0])

    return {"prediction": prediction_value} 

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)