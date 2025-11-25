# MQTT API dengan FastAPI dan Mosquitto

Project Python dengan FastAPI dan MQTT Mosquitto broker terintegrasi dalam satu Docker Compose project.

## Fitur
- FastAPI endpoint GET `/{topic}/{message}` untuk publish MQTT
- Mosquitto MQTT broker terintegrasi dalam Docker Compose
- MQTT WebSocket support di port 9001
- Auto-reconnect dan persistent storage untuk Mosquitto

## Arsitektur

Project ini menggunakan Docker Compose dengan 2 services:
1. **mosquitto**: MQTT broker (Mosquitto v1.6.9)
2. **mqtt-api**: FastAPI application yang connect ke mosquitto broker

Services berkomunikasi melalui Docker network `mqtt-network`.

## Instalasi

### Menggunakan Docker Compose (Recommended)

1. Copy file environment:
```bash
cp .env.example .env
```

2. Edit `.env` sesuai kebutuhan (opsional, default sudah bagus):
```env
API_PORT=8000
TCP_PORT=1883
WEBSOCKET_PORT=9001
MQTT_PORT=1883
MQTT_KEEPALIVE=60
```

3. Build dan jalankan dengan Docker Compose:
```bash
docker-compose up -d --build
```

4. Cek logs:
```bash
docker-compose logs -f mqtt-api
docker-compose logs -f mosquitto
```

5. Stop containers:
```bash
docker-compose down
```

6. Stop dan hapus volumes (reset data):
```bash
docker-compose down -v
```

### Menggunakan Python Virtual Environment (Development)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Jalankan aplikasi:
```bash
uvicorn main:app --reload
```

**Note**: Untuk development local, pastikan ada MQTT broker yang berjalan dan update `MQTT_BROKER` di environment variable atau di `main.py`.

## Penggunaan

### Endpoint Root
```
GET http://localhost:8000/
```

### Publish Pesan ke MQTT
```
GET http://localhost:8000/{topic}/{message}
```

Contoh:
```
GET http://localhost:8000/sensor/temperature/25
GET http://localhost:8000/home/light/on
```

### Dokumentasi API
FastAPI menyediakan dokumentasi interaktif:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Konfigurasi

### Environment Variables

File `.env` untuk konfigurasi:

- `API_PORT`: Port untuk FastAPI (default: 8000)
- `TCP_PORT`: Port MQTT broker TCP (default: 1883)
- `WEBSOCKET_PORT`: Port MQTT WebSocket (default: 9001)
- `MQTT_PORT`: Port untuk koneksi internal (default: 1883)
- `MQTT_KEEPALIVE`: Keepalive interval dalam detik (default: 60)
- `MQTT_USERNAME`: Username untuk autentikasi (opsional)
- `MQTT_PASSWORD`: Password untuk autentikasi (opsional)

### Mosquitto Configuration

File `mosquitto.conf` berisi konfigurasi broker:
- Listener TCP di port 1883
- Listener WebSocket di port 9001
- Allow anonymous connections (default: true)
- Persistent storage enabled

## Akses MQTT Broker

Setelah running, Mosquitto broker dapat diakses:

1. **Dari host machine**:
   - TCP: `localhost:1883`
   - WebSocket: `localhost:9001`

2. **Dari container lain** (dalam network yang sama):
   - TCP: `mosquitto:1883`

3. **Test dengan mosquitto_pub/sub**:
```bash
# Subscribe
docker exec -it mosquitto mosquitto_sub -h localhost -t test/#

# Publish
docker exec -it mosquitto mosquitto_pub -h localhost -t test/topic -m "Hello MQTT"
```

## Response Format

Success response:
```json
{
    "status": "success",
    "topic": "sensor/temperature",
    "message": "25",
    "broker": "158.140.183.210"
}
```

Error response:
```json
{
    "detail": "Error message"
}
```
