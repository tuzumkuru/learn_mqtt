import board
import busio
import adafruit_shtc3
import datetime
import json
import time
import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

# Get required parameters from environment variables
MQTT_BROKER_ADDRESS = os.getenv('MQTT_BROKER_ADDRESS')
MQTT_BROKER_USERNAME = os.getenv('MQTT_BROKER_USERNAME')
MQTT_BROKER_PASSWORD = os.getenv('MQTT_BROKER_PASSWORD')
MQTT_TOPIC = "NY/BEDROOM/SHTC3" # Write a good topic name for your own use

# Initialize the I2C bus and the SHTC3 sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_shtc3.SHTC3(i2c)

# Get the current time
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
time_now = int(time.time())

# Read temperature and humidity data from the SHTC3 sensor
temperature, humidity = sensor.measurements

# Print the temperature and humidity values along with the timestamp
print("{} Temperature: {:.2f} C, Humidity: {:.2f} %".format(timestamp, temperature, humidity))

# Define the message payload as a JSON object with time, humidity and temperature properties
message = {
    "time": time_now,
    "temperature": temperature,
    "humidity": humidity    
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


# # Write data to a file, commented out for now, 
# script_dir = os.path.dirname(os.path.abspath(__file__))

# filename = os.path.join(script_dir, "sensor_data.txt")
# with open(filename, "a+") as file:
#     file.write("{} Temperature: {:.2f} C, Humidity: {:.2f} %\n".format(timestamp, temperature, humidity))