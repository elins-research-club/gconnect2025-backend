from sqlalchemy import create_engine, Column, Integer, Float, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

# URL untuk connect ke file database SQLite g-connect
SQLALCHEMY_DATABASE_URL = "sqlite:///./gconnect.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# sebagai blueprint untuk tabel di database
class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    # dari DHT 22
    temperature = Column(Float)
    humidity = Column(Float)
    # LDR
    light_intensity = Column(Float)
    # soil sensor
    soil_moisture = Column(Float)
    # anemometer
    wind_speed = Column(Float)
    # raindrop sensor
    rain_detection = Column(Boolean)

def get_db():
    """Buat koneksi ke DB, akan tutup otomatis kalau udah nggak dipakai."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    """Auto generate tabel di DB kalau belum ada"""
    Base.metadata.create_all(bind=engine)