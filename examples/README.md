# MicroCrate Examples

This folder contains code samples and fully working example code for the MicroCrate driver.

* `example_usage.py`: Demonstrates various types of query.  This does not have any specific microcontroller dependencies, and can be run on desktop MicroPython.
* `object_examples.py`: Demonstrates operations using an [OBJECT](https://cratedb.com/docs/crate/reference/en/latest/general/ddl/data-types.html#objects) column in CrateDB.  Also demonstrates the use of the [ARRAY](https://cratedb.com/docs/crate/reference/en/latest/general/ddl/data-types.html#array) container data type.
* `picow_demo.py`: A complete demo script for the [Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#picow-technical-specification) microcontroller. The script connects to a wifi network (you'll need to configure your own SSID and password) and sends temperature readings to a CrateDB database every 10 seconds.  The code creates a table in CrateDB if needed.  To use this, you'll need a free [CrateDB cloud instance](https://console.cratedb.cloud/).  No external sensors are required: the temperature is calculated from the Pico W's internal temperature.

We're always on the look out for more example code... if you have a script that you'd like to share, please [raise an issue](/issues) to discuss it with us, or send a [pull request](/pulls).  Thanks!