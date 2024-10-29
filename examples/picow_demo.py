# micropython-cratedb Example for the Raspberry Pi Pico W.
# Configure your CrateDB credentials and WiFi SSID
# and password below before running this.

import machine
import network
import sys
import time

import cratedb

# Configure CrateDB driver.
crate = cratedb.CrateDB(
    host="hostname", 
    user="username", 
    password="password"
)

# Set up the WiFi and connect.
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("ssid", "password")

while not wlan.isconnected() and wlan.status() >= 0:
    print("Connecting to wifi...")
    time.sleep(0.5)

ip_addr = wlan.ifconfig()[0]
print(f"Connected to wifi as {ip_addr}")

# Create a table in CrateDB if necessary.
try:
    crate.execute(
        """
            CREATE TABLE IF NOT EXISTS picow_test (
            id TEXT, 
            ts TIMESTAMP WITH TIME ZONE GENERATED ALWAYS AS current_timestamp, 
            temp DOUBLE PRECISION
            )
        """, 
        return_response = False
    )

except Exception as e:
    print("Error creating table:")
    print(e)
    sys.exit(1)

num_iterations = 0

while True:
    # Periodically insert data into a table in CrateDB and read back an average value.

    # Not particularly reliable but uses built in hardware.
    # Demos how to incorporate senasor data into this application.
    # Replace code here with something else for a 'real' sensor.
    # Algorithm used here is from:
    # https://www.coderdojotc.org/micropython/advanced-labs/03-internal-temperature/
    sensor_temp = machine.ADC(4)
    reading = sensor_temp.read_u16() * (3.3 / (65535))
    temperature = 27 - (reading - 0.706)/0.001721
    temperature = round(temperature, 1)

    response = crate.execute(
        "INSERT INTO picow_test (id, temp) VALUES (?, ?)",
        [
            ip_addr,
            temperature
        ]
    )

    if response["rowcount"] == 1:
        print("Inserted record into CrateDB.")
        num_iterations += 1

    # Every 10th iteration let's read back an average value for the last 24hrs.
    if num_iterations == 10:
        response = crate.execute(
            "SELECT trunc(avg(temp), 1) AS avg_temp FROM picow_test WHERE id=? AND ts >= (CURRENT_TIMESTAMP - INTERVAL '1' DAY)",
            [
                ip_addr
            ]
        )

        if response["rowcount"] == 1:
            print(f"Average temperature over last 24hrs: {response["rows"][0][0]}")
            num_iterations = 0

    time.sleep(10)
