from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import database
from app.routers import sensor_data, websocket

# Inisialisasi dan setup database saat app dijalankan
database.create_db_and_tables()

# Deskripsi aplikasi (ditampilkan di /docs Swagger UI)
description = """
API Backend untuk dashboard monitoring lingkungan berbasis IoT, **G-Connect 2025**. 🚀

API ini jadi jembatan utama buat:
1. **Menerima (Ingest)** data dari sensor node di lapangan
2. **Menyajikan (Serve)** data ke dashboard monitoring (via REST API & WebSocket)

### Endpoint yang tersedia:
- `POST /api/v1/data` → Kirim data sensor baru (butuh API Key)
- `GET /api/v1/data/latest` → Ambil data sensor terbaru, Untuk menampilkan data terakhir pada saat frontend pertama kali running.
- `GET /api/v1/data/history` → Ambil histori data sensor
- `WS /ws` → WebSocket buat live data stream ke dashboard Frontend
"""

# Inisialisasi FastAPI instance
app = FastAPI(
    title="G-Connect API",
    description=description,
    version="1.0.0"
)

# Konfigurasi CORS → biar bisa diakses dari frontend (contoh: React/Next.js)
origins = [
    "http://localhost:3000"  # TODO: ganti dengan domain frontend pas production
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register router dari fitur backend
app.include_router(sensor_data.router, prefix="/api/v1", tags=["Sensor Data"])
app.include_router(websocket.router, tags=["WebSocket"])

@app.get("/", tags=["Health Check"])
def read_root():
    """
    Endpoint default buat cek status backend.
    """
    return {"status": "G-Connect Backend is running 🚀"}
