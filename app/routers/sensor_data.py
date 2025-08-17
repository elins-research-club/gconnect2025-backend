from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas import schemas
from app.routers.websocket import manager
from app.security.security import get_api_key
from app.crud import crud

# Router khusus untuk endpoint sensor
router = APIRouter(prefix="/data", tags=["Sensor Data"])

@router.post("", response_model=schemas.SensorData)
async def create_sensor_data(
    data: schemas.SensorDataCreate,
    db: Session = Depends(get_db),
    api_key: str = Security(get_api_key)  # Validasi API key dari header
):
    """
    Endpoint untuk menerima data sensor baru (dikirim dari hardware).
    - Data tervalidasi berdasarkan skema `SensorDataCreate`
    - Data disimpan ke database SQLite
    - Data dibroadcast ke frontend melalui WebSocket
    """
    # Simpan data sensor ke database
    new_reading = crud.create_sensor_reading(db=db, data=data)

    # Kirim data ke klien WebSocket (realtime)
    broadcast_data_model = schemas.SensorData.from_orm(new_reading)
    await manager.broadcast(broadcast_data_model.model_dump_json())

    return new_reading

@router.get("/latest", response_model=schemas.SensorData)
def read_latest_data(db: Session = Depends(get_db)):
    """
    Endpoint untuk mendapatkan data sensor terbaru.
    Untuk menampilkan data terakhir pada saat frontend pertama kali running.
    """
    latest_reading = crud.get_latest_sensor_reading(db=db)
    if latest_reading is None:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    return latest_reading

@router.get("/history", response_model=list[schemas.SensorData])
def read_history_data(
    days: int = 7, 
        db: Session = Depends(get_db)
    ):
    """
    Endpoint untuk mendapatkan data histori berdasarkan range hari.
    Contoh: `GET /history?days=7` -> Ambil data 7 hari terakhir.
    """
    return crud.get_sensor_readings_by_range(db=db, days=days)

# =====================
# TODO
# =====================
# - [ ] Tambahkan fitur filter data berdasarkan jenis sensor tertentu.
#       Contoh: /history?type=temperature
#
# - [ ] Tambahkan autentikasi JWT / OAuth jika ingin keamanan lebih tinggi.
#
# - [ ] Tambahkan pagination untuk data history agar tidak overload di frontend.
#
# - [ ] Buat endpoint /summary untuk menyajikan data statistik per hari (opsional).
#
# - [ ] Pertimbangkan cache / rate limiter karena data sering dikirim.

