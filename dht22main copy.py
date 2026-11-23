#Sofia
#22.11.2026
# Humidity and temperature sensor DHT22

# Import necessary libraries
import dht 
import machine
import time
from simple import MQTTClient
import network

# Set up Wi-Fi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Sofia", "MyPassword123") # I changed the password to a placeholder for security reasons. 

while not wlan.isconnected():
    time.sleep(1)

print("wifi connected")


# Set up the DHT22 sensor and LED pin
sensor = dht.DHT22(machine.Pin(21))
led = machine.Pin("LED", machine.Pin.OUT)

# Connect to the MQTT broker
client = MQTTClient(b"picow","iot.research.hamk.fi", keepalive=60)
client.connect()

# Define MQTT topics for temperature and humidity
temperature_topic = b"HAMK/Fo/DHT22/2606460/temperature"
humidity_topic = b"HAMK/Fo/DHT22/2606460/humidity"

# give variables for old values to compare with new values
old_temperature = None
old_humidity = None

# Main loop to read sensor data and publish to MQTT broker
while True:
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()

    print("Temperature:", temperature, "°C")
    print("Humidity:", humidity, "%")

    sent = False

    if old_temperature != temperature:
        client.publish(temperature_topic, str(temperature))
        old_temperature = temperature
        sent = True

    if old_humidity != humidity:
        client.publish(humidity_topic, str(humidity))
        old_humidity = humidity
        sent = True

    if sent:
        print("Data sent to MQTT broker.")
    else:
        print("No new data to send.")

# Wait for 10 seconds before the next reading
time.sleep(10)

