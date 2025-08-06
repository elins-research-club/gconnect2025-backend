# Mendefinisikan bentuk data JSON yang diterima dan dikirim oleh API
from pydantic import BaseModel
from datetime import datetime

# Skema untuk data yang DITERIMA dari mikrokontroler.
class SensorDataCreate(BaseModel):
    temperature: float
    humidity: float
    light_intensity: float
    soil_moisture: float
    wind_speed: float
    rain_detection: bool

# Skema untuk data yang DIBACA dari database.
class SensorData(SensorDataCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True