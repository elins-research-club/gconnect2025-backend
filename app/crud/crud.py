from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import database
from schemas import schemas

def create_sensor_reading(db: Session, data: schemas.SensorDataCreate):
    """
    Fungsi ini untuk menerima data sensor (divalidasi oleh skema), terus disimpan ke DB.

    Data sensor yang sudah tervalidasi akan dikonversi jadi objek `SensorReading`,
    lalu disimpan ke dalam database menggunakan session aktif.

    Args:
        db (Session): Session database aktif dari SQLAlchemy.
        data (SensorDataCreate): Data sensor hasil input dari perangkat (sudah tervalidasi).

    Returns:
        SensorReading: Data sensor yang berhasil disimpan ke database.
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
    # Ambil data sensor paling baru (yang paling terakhir masuk)
    """
    Mengambil data sensor terbaru dari database.

    Query mencari data dengan timestamp paling akhir (paling baru)
    dari tabel `SensorReading`.

    Args:
        db (Session): Session database aktif dari SQLAlchemy.

    Returns:
        SensorReading | None: Data sensor terbaru atau None jika belum ada data.
    """
    return db.query(database.SensorReading).order_by(database.SensorReading.timestamp.desc()).first()

def get_sensor_readings_by_range(db: Session, days: int):
    # Hitung tanggal mulai dari 'days' hari yang lalu
    """
    Mengambil data sensor berdasarkan rentang hari terakhir.

    Fungsi ini untuk mencari data sensor dari tanggal sekarang
    dikurangi jumlah hari (misalnya 7 hari terakhir).

    Args:
        db (Session): Session database aktif.
        days (int): Jumlah hari ke belakang dari hari ini.

    Returns:
        List[SensorReading]: List data sensor dalam rentang waktu tersebut.
    """
    start_date = datetime.now() - timedelta(days=days)
    # Ambil semua data sensor dari tanggal itu sampai sekarang, urut dari yang paling lama
    return db.query(database.SensorReading).filter(database.SensorReading.timestamp >= start_date).order_by(database.SensorReading.timestamp.asc()).all()