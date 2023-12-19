import time
import board
import adafruit_bme680
import datetime
import json
import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

# Get required parameters from environment variables
MQTT_BROKER_ADDRESS = os.getenv('MQTT_BROKER_ADDRESS')
MQTT_BROKER_USERNAME = os.getenv('MQTT_BROKER_USERNAME')
MQTT_BROKER_PASSWORD = os.getenv('MQTT_BROKER_PASSWORD')
MQTT_TOPIC = "TEST/SENSOR/BME680"

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# Change this to match the location's pressure (hPa) at sea level
# for correct calculation of altitude
bme680.sea_level_pressure = 1013.25


# Get the current timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
time_now = int(time.time())

# Get all sensor values
temperature = bme680.temperature
relative_humidity = bme680.relative_humidity
gas = bme680.gas
pressure = bme680.pressure
altitude = bme680.altitude

# Print the values along with the timestamp
print("{} Temperature: {:.2f} C, Humidity: {:.2f} %, Gas: {:.2f}, Pressure: {:.2f} hPa, Altitude: {:.2f} m".format(timestamp, temperature, relative_humidity, gas, pressure, altitude))

# Define the message payload as a JSON object with time, humidity and temperature properties
message = {
    "time": time_now,
    "temperature": temperature,
    "humidity": relative_humidity,
    "gas": gas,
    "pressure": pressure,
    "altitude": altitude
}

# Set up the MQTT client
client = mqtt.Client()
client.username_pw_set(username=MQTT_BROKER_USERNAME, password=MQTT_BROKER_PASSWORD)

# Connect to the MQTT broker
client.connect(MQTT_BROKER_ADDRESS)

# Publish a message to the "test" topic
client.publish(MQTT_TOPIC, json.dumps(message))

# Disconnect from the broker
client.disconnect()