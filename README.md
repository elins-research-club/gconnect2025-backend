# G-Connect 2025 - Backend API

Repositori ini berisi kode backend untuk proyek G-Connect 2025.
Dibangun menggunakan FastAPI (Python) dan SQLite.
---
## Prasyarat (Prerequisites)

Pastikan perangkat lunak berikut sudah terpasang di komputer Anda:
* [Python 3.9+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)

---
## Instalasi & Setup

1.  **Clone Repositori**
    ```bash
    git clone https://github.com/elins-research-club/gconnect2025-backend.git
    cd gconnect-backend
    ```

2.  **Buat File Environment**
    Buat file bernama `.env` di direktori utama, lalu isi dengan format berikut. File ini berisi variabel untuk menjalankan aplikasi.
    ```env
    # Isi file .env
    API_KEY="gconnect-2025"
    ```

---
## Menjalankan Aplikasi

Untuk menjalankan aplikasi ini secara lokal dengan Virtual Environment.
1.  **Buat & Aktifkan Virtual Environment**
    ```bash
    # Buat venv (hanya sekali)
    python -m venv venv

    # Aktifkan venv (untuk Windows)
    .\venv\Scripts\activate
    ```

2.  **Install Dependensi**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Masuk Direktori App**
    ```bash
    cd app
    ```
 
4.  **Jalankan Server**
    ```bash
    uvicorn app.main:app --reload
    ```
5.  **Selesai!** Server sekarang berjalan dan dapat diakses di `http://localhost:8000`. Mode `--reload` akan me-restart server secara otomatis setiap kali menyimpan perubahan pada kode.

---
## Penggunaan API

Setelah server berjalan, dokumentasi API (Swagger UI) yang dibuat secara otomatis oleh FastAPI tersedia di:

**`http://localhost:8000/docs`**

Endpoint utama yang tersedia antara lain:
* **`POST /api/v1/data`**: Untuk mengirim paket berupa data sensor baru.
* **`GET /api/v1/data/latest`**: Untuk mengambil satu data sensor paling akhir.
* **`GET /api/v1/data/history`**: Untuk mengambil riwayat data sensor.
* **`WS /ws`**: Alamat untuk koneksi WebSocket real-time.
