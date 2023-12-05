import paho.mqtt.client as mqtt

# Get required parameters from environment variables
MQTT_BROKER_ADDRESS = ""    # Replace with the IP address of the broker
MQTT_BROKER_USERNAME = ""   # Replace with the username of the broker
MQTT_BROKER_PASSWORD = ""   # Replace with the password of the broker user
MQTT_TOPIC = "TEST"         # Write a good topic name for your own use

# Set up the MQTT client
client = mqtt.Client()

# if you have 
client.username_pw_set(username=MQTT_BROKER_USERNAME, password=MQTT_BROKER_PASSWORD)

# Connect to the MQTT broker
client.connect(MQTT_BROKER_ADDRESS)

# Publish a message to the MQTT_TOPIC topic
message = "Hello, world!"
client.publish(MQTT_TOPIC, message)

# Disconnect from the broker
client.disconnect()