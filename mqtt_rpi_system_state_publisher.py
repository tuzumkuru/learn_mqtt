# monitor_stats.py
import os
from dotenv import load_dotenv
import psutil
import json
import time
import paho.mqtt.publish as publish

# Load environment variables from .env
load_dotenv()

# MQTT Broker Info
broker_address = os.getenv("MQTT_BROKER_ADDRESS")
port = int(os.getenv("MQTT_BROKER_PORT"))
topic = "TEST/COMPUTE/RPI5"  # Update the topic here
username = os.getenv("MQTT_BROKER_USERNAME")
password = os.getenv("MQTT_BROKER_PASSWORD")

def get_system_stats():
    # Get CPU usage
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)

    # Get memory usage
    memory_info = psutil.virtual_memory()

    # Get disk usage
    disk_info = psutil.disk_usage('/')

    # Get load averages
    load_avg = os.getloadavg()

    # Get CPU temperature using psutil
    temperature_info = psutil.sensors_temperatures()
    cpu_temp_info = temperature_info.get("cpu_thermal", [{}])[0]
    temperature = cpu_temp_info.current if cpu_temp_info else None

    stats = {
        "temperature": temperature,
        "cpu_usage": cpu_usage,
        "memory_usage": {
            "total": memory_info.total,
            "used": memory_info.used,
            "free": memory_info.free,
            "percent": memory_info.percent
        },
        "disk_usage": {
            "total": disk_info.total,
            "used": disk_info.used,
            "free": disk_info.free,
            "percent": disk_info.percent
        },
        "load_avg": {
            "1_min": load_avg[0],
            "5_min": load_avg[1],
            "15_min": load_avg[2]
        }
    }
    return stats

def publish_stats():
    stats = get_system_stats()
    payload = json.dumps(stats)
    auth = {'username': username, 'password': password}
    publish.single(topic, payload, hostname=broker_address, port=port, auth=auth)

if __name__ == "__main__":
    while True:
        publish_stats()
        time.sleep(1)
