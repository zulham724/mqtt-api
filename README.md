# MQTT API dengan FastAPI

Project Python dengan FastAPI dan MQTT Mosquitto client untuk mengirim pesan ke MQTT broker.

## Fitur
- FastAPI endpoint GET `/{topic}/{message}`
- MQTT client untuk publish pesan ke broker Mosquitto
- Broker IP: 158.140.183.210

## Instalasi

### Menggunakan Python Virtual Environment

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Jalankan aplikasi:
```bash
uvicorn main:app --reload
```

Atau jalankan langsung:
```bash
python main.py
```

Server akan berjalan di `http://localhost:8000`

### Menggunakan Docker

1. Copy file environment:
```bash
cp .env.example .env
```

2. Edit `.env` sesuai kebutuhan (opsional, default sudah tersedia)

3. Build dan jalankan dengan Docker Compose:
```bash
docker-compose up -d
```

4. Cek logs:
```bash
docker-compose logs -f
```

5. Stop container:
```bash
docker-compose down
```

### Menggunakan Docker Manual

1. Build image:
```bash
docker build -t mqtt-api .
```

2. Run container:
```bash
docker run -d -p 8000:8000 --name mqtt-api mqtt-api
```

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

Konfigurasi MQTT broker dapat dilakukan melalui environment variables (untuk Docker) atau langsung di `main.py`:

Environment Variables (gunakan file `.env`):
- `MQTT_BROKER`: IP/hostname broker MQTT (default: 158.140.183.210)
- `MQTT_PORT`: Port broker MQTT (default: 1883)
- `MQTT_KEEPALIVE`: Keepalive interval dalam detik (default: 60)
- `MQTT_USERNAME`: Username untuk autentikasi (opsional)
- `MQTT_PASSWORD`: Password untuk autentikasi (opsional)
- `API_PORT`: Port untuk FastAPI (default: 8000)

Contoh file `.env`:
```env
MQTT_BROKER=158.140.183.210
MQTT_PORT=1883
MQTT_KEEPALIVE=60
API_PORT=8000
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
