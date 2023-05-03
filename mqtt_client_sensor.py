import board
import busio
import adafruit_shtc3
import datetime
import json
import time
import os
import paho.mqtt.client as mqtt

# Get the absolute path of the current script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize the I2C bus and the SHTC3 sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_shtc3.SHTC3(i2c)

# Read temperature and humidity data from the SHTC3 sensor
temperature, humidity = sensor.measurements

# Get the current timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Print the temperature and humidity values along with the timestamp
print("{} Temperature: {:.2f} C, Humidity: {:.2f} %\n".format(timestamp, temperature, humidity))

# Write data to a file
filename = os.path.join(script_dir, "sensor_data.txt")
with open(filename, "a+") as file:
    file.write("{} Temperature: {:.2f} C, Humidity: {:.2f} %\n".format(timestamp, temperature, humidity))

# Define the message payload as a JSON object with time, humidity and temperature properties
message = {
    "time": int(time.time()),
    "humidity": humidity,
    "temperature": temperature
}

# Set up the MQTT client
client = mqtt.Client()

# Connect to the MQTT broker
broker_address = "raspberrypi" # Replace with the IP address of the broker
client.connect(broker_address)

# Publish a message to the "test" topic
topic = "SHTC3"
client.publish(topic, json.dumps(message))

# Disconnect from the broker
client.disconnect()