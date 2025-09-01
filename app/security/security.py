import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

# Memuat variabel dari file .env
load_dotenv()

# Nama header yang akan kita gunakan
API_KEY_NAME = "X-API-KEY"
# Ambil nilai API_KEY dari file .env
API_KEY = os.getenv("API_KEY")

# Penting: Pastikan punya file .env berisi: API_KEY="gconnect-2025"
if not API_KEY:
    # Ini akan stop aplikasi jika API_KEY tidak disetel, lebih baik daripada error nanti.
    raise ValueError("API_KEY tidak ditemukan di file .env. Harap buat file .env")

# Membuat objek untuk 'meminta' header dari request
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def get_api_key(api_key: str = Security(api_key_header)):
    # Cek jika header tidak ada atau kosong
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Header X-API-KEY tidak ada atau kosong",
        )
    # Cek jika key tidak cocok
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key tidak valid",
        )
