from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import database
from app.schemas import schemas


def create_sensor_reading(db: Session, data: schemas.SensorDataCreate):
    """Menyimpan satu paket data sensor baru ke dalam database.

    Fungsi ini mengonversi data sensor yang sudah divalidasi oleh Pydantic
    menjadi objek model SQLAlchemy (SensorReading) dan menyimpannya.

    Args:
        db: Session database aktif yang disediakan oleh FastAPI.
        data: Objek Pydantic berisi data sensor yang akan disimpan.

    Returns:
        Objek SensorReading yang baru saja dibuat, termasuk ID dan timestamp.
    """
    db_reading = database.SensorReading(
        temperature=data.temperature,
        humidity=data.humidity,
        light_intensity=data.light_intensity,
        soil_moisture=data.soil_moisture,
        wind_speed=data.wind_speed,
        rain_detection=data.rain_detection
    )
    
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading

def get_latest_sensor_reading(db: Session):
    """Mengambil data sensor paling akhir dari database.

    Melakukan query untuk mencari satu baris data dengan timestamp terbaru.

    Args:
        db: Session database aktif.

    Returns:
        Objek SensorReading terbaru, atau None jika tabel kosong.
    """
    return db.query(database.SensorReading).order_by(database.SensorReading.timestamp.desc()).first()

def get_sensor_readings_by_range(db: Session, days: int):
    """Mengambil daftar data sensor dalam rentang waktu tertentu.

    Query memfilter data sensor dari N hari terakhir hingga saat ini.

    Args:
        db: Session database aktif.
        days: Jumlah hari ke belakang sebagai rentang waktu.

    Returns:
        Sebuah list berisi objek SensorReading yang diurutkan dari yang paling lama.
    """
    start_date = datetime.now() - timedelta(days=days)
    return db.query(database.SensorReading).filter(database.SensorReading.timestamp >= start_date).order_by(database.SensorReading.timestamp.asc()).all()