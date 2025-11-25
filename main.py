from fastapi import FastAPI, HTTPException
import paho.mqtt.client as mqtt
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MQTT API", description="FastAPI dengan MQTT Mosquitto Client")

# Konfigurasi MQTT Broker dari environment variables atau default
MQTT_BROKER = os.getenv("MQTT_BROKER", "158.140.183.210")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", "60"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

# Callback saat terhubung ke broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Berhasil terhubung ke MQTT Broker")
    else:
        logger.error(f"Gagal terhubung, return code: {rc}")

# Callback saat publish berhasil
def on_publish(client, userdata, mid):
    logger.info(f"Pesan berhasil dikirim, message id: {mid}")

# Inisialisasi MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish

# Set username dan password jika tersedia
if MQTT_USERNAME and MQTT_PASSWORD:
    mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    logger.info("MQTT authentication configured")

@app.on_event("startup")
async def startup_event():
    """Koneksi ke MQTT broker saat aplikasi dimulai"""
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        mqtt_client.loop_start()
        logger.info("MQTT client loop started")
    except Exception as e:
        logger.error(f"Error saat menghubungkan ke MQTT broker: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Putuskan koneksi MQTT saat aplikasi dimatikan"""
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    logger.info("MQTT client disconnected")

@app.get("/")
async def root():
    """Endpoint root untuk verifikasi API berjalan"""
    return {
        "message": "MQTT API is running",
        "broker": MQTT_BROKER,
        "endpoint": "GET /{topic}/{message}"
    }

@app.get("/{topic}/{message}")
async def publish_message(topic: str, message: str):
    """
    Endpoint untuk publish pesan ke MQTT broker
    
    Args:
        topic: Topic MQTT yang akan menerima pesan
        message: Pesan yang akan dikirim
    
    Returns:
        dict: Status publikasi pesan
    """
    try:
        # Publish pesan ke broker
        result = mqtt_client.publish(topic, message)
        
        # Cek status publish
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            logger.info(f"Pesan '{message}' berhasil dipublish ke topic '{topic}'")
            return {
                "status": "success",
                "topic": topic,
                "message": message,
                "broker": MQTT_BROKER
            }
        else:
            logger.error(f"Gagal publish pesan, return code: {result.rc}")
            raise HTTPException(
                status_code=500,
                detail=f"Gagal mengirim pesan ke MQTT broker, return code: {result.rc}"
            )
    except Exception as e:
        logger.error(f"Error saat publish pesan: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
