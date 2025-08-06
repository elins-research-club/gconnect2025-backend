from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    """
    Class untuk ngatur koneksi WebSocket yang aktif.

    Bisa simpan daftar koneksi, penambahan/penghapusan koneksi,
    dan kirim broadcast data ke klien (Frontend).
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # Tambah koneksi baru dan terima permintaan WebSocket dari Frontend.
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        # Hapus koneksi klien (Frontend) dari daftar aktif pas klien disconnect.
        self.active_connections.remove(websocket)

    async def broadcast(self, data: str):
        """
        Kirim data ke semua klien yang lagi terhubung.
        Kalo ada satu koneksi error, lanjut terus kirim ke yang lain. Jika ada lebih dari satu klien
        """
        for connection in self.active_connections:
            try:
                await connection.send_text(data)
            except Exception:
                # jika koneksi sudah putus tapi belum sempat dihapus, abaikan
                pass

# Bikin instance ConnectionManager
manager = ConnectionManager()

# Endpoint WebSocket dengan routernya sendiri (router khusus untuk WebSocket)
router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Endpoint untuk WebSocket.
    Connect klien baru, terus jaga koneksi tetap hidup.
    """
    await manager.connect(websocket)
    try:
        while True:
            # tetap terhubung untuk menerima pesan (jika ada) atau menjaga koneksi tetap hidup
            await websocket.receive_text()
    except WebSocketDisconnect:
        # Kalo klien disconnect, hapus dari daftar koneksi
        manager.disconnect(websocket)