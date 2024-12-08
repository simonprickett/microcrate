# micropython-cratedb - A CrateDB Driver for MicroPython

[![Tests](https://github.com/crate/micropython-cratedb/actions/workflows/tests.yml/badge.svg)](https://github.com/crate/micropython-cratedb/actions/workflows/tests.yml)
[![Test coverage](https://img.shields.io/codecov/c/gh/crate/micropython-cratedb.svg?style=flat-square)](https://codecov.io/gh/crate/micropython-cratedb/)

## Introduction

micropython-cratedb is a [CrateDB](https://cratedb.com) driver for the [MicroPython](https://micropython.org) language.  It connects to CrateDB using the [HTTP Endpoint](https://cratedb.com/docs/crate/reference/en/latest/interfaces/http.html).

To use this, you'll need a CrateDB database cluster.  Sign up for our cloud free tier [here](https://console.cratedb.cloud/) or get started with Docker [here](https://hub.docker.com/_/crate).

Want to learn more about CrateDB?  Take our free [Fundamentals course](https://learn.cratedb.com/course-overview) at the CrateDB Academy.  You can also [watch this video](https://www.youtube.com/watch?v=8_rirCsCqac) from the [Notts IoT Meetup](https://www.meetup.com/nottingham-iot-meetup/) where [Simon Prickett](https://simonprickett.dev), CrateDB's Developer Advocate, demonstrates how to use an early version of this driver with various sensors attached to Raspberry Pi Pico W devices.

## Installation

There are two ways to install this driver.

### Install with `mpremote`

Install the driver with [`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html) like this:

```bash
mpremote mip install github:crate/micropython-cratedb
```

This will install the driver into `/lib` on the device, along with the [base64](https://github.com/micropython/micropython-lib/tree/master/python-stdlib/base64) module from `micropython-lib`.

### Install with `mip`

You can also install the driver into `/lib` on the device by running the following commands at the MicroPython REPL on the device:

```python
import network
import mip
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("<your wifi SSID>", "<your wifi password>")
wlan.isconnected() # Run this until it returns True
mip.install("github:crate/micropython-cratedb")
```

## Using the Driver in a MicroPython Script

Import the driver like this:

```python
import cratedb
```

### Connecting to CrateDB

Connect to a CrateDB Cloud cluster using SSL, by providing hostname, username, and password:

```python
crate = cratedb.CrateDB(
    host="host", 
    user="user", 
    password="password"
)
```

The driver uses SSL by default.

If you're running CrateDB on your workstation (with Docker for example,
by using `docker run --rm -it --publish=4200:4200 crate`), connect like
this:

```python
crate = cratedb.CrateDB(
    host="hostname", 
    use_ssl=False
)
```

The driver will connect to port 4200 unless you provide an alternative value:

```python
crate = cratedb.CrateDB(
    host="host", 
    user="user", 
    port=4201,
    password="password"
)
```

### Interacting with CrateDB

CrateDB is a SQL database: you'll store, update and retieve data using SQL statements.  The examples that follow assume a table schema that looks like this:

```sql
CREATE TABLE temp_humidity (
  sensor_id TEXT, 
  ts TIMESTAMP WITH TIME ZONE GENERATED ALWAYS AS current_timestamp,
  temp DOUBLE PRECISION, 
  humidity DOUBLE PRECISION
);
```

Assume that the table contains a few sample rows.

#### Retrieving Data

The `execute` method sends a SQL statement to the database for execution, and returns the result:

```python
response = crate.execute(
    "SELECT sensor_id, ts, temp, humidity FROM temp_humidity ORDER BY ts DESC"
)
```

You can also use parameterized queries:

```python
response = crate.execute(
    """
        SELECT sensor_id, ts, temp, humidity
        FROM temp_humidity WHERE sensor_id = ?
        ORDER BY ts DESC
    """,
    [
        "a01"
    ]
)
```

Data is returned as a dictionary that looks like this:

```python
{
    'rows': [
        ['a01', 1728473302619, 22.8, 59.1], 
        ['a02', 1728473260880, 3.3, 12.9], 
        ['a02', 1728473251188, 3.2, 12.7], 
        ['a03', 1728473237365, 28.4, 65.7], 
        ['a01', 1728473223332, 22.3, 58.6]
    ], 
    'rowcount': 5, 
    'cols': [
        'sensor_id', 
        'ts', 
        'temp', 
        'humidity'
    ], 
    'duration': 18.11329
}
```

Use the `with_types` parameter to have CrateDB return information about the data type of each column in the resultset. This feature is off by defaault to minimize network bandwidth.

```python
response = crate.execute(
    "SELECT sensor_id, ts, temp FROM temp_humidity WHERE sensor_id = ? ORDER BY ts DESC",
    [
        "a01"
    ],
    with_types=True
)
```

The resultset then contains an extra key, `col_types`:

```python
{
    'col_types': [
        4, 
        11, 
        6
    ], 
    'cols': [
        'sensor_id', 
        'ts', 
        'temp'
    ], 
    'rowcount': 2, 
    'rows': [
        ['a01', 1728473302619, 22.8], 
        ['a01', 1728473223332, 22.3]
    ], 
    'duration': 7.936583
}
```

Constants are provided for each type.  For example type `11` is `CRATEDB_TYPE_TIMESTAMP_WITH_TIME_ZONE`.

#### Inserting / Updating Data

Here's an example insert statement:

```python
response = crate.execute(
    "INSERT INTO temp_humidity (sensor_id, temp, humidity) VALUES (?, ?, ?)",
    [
        "a01",
        22.8,
        60.1
    ]
)
```

The response from CrateDB looks like this:

```python
{
    'rows': [
        []
    ], 
    'rowcount': 1, 
    'cols': [], 
    'duration': 38.615707
}
```

If you don't need a response, set the `return_response` parameter to `False` (default is `True`). This will save a small amount of time that the driver normally spends on processing the response.

```python
response = crate.execute(
    "INSERT INTO temp_humidity (sensor_id, temp, humidity) VALUES (?, ?, ?)",
    [
        "a01",
        22.9,
        60.3
    ],
    return_response=False
)
```

`response` will be `None`.

You can add multiple records in a single network round trip using a bulk insert:

```python
response = crate.execute(
    "INSERT INTO temp_humidity (sensor_id, temp, humidity) VALUES (?, ?, ?)",
    [
        [
            "a01",
            22.7,
            60.1
        ],
        [
            "a02",
            3.3,
            12.9
        ]
    ]
)
```

The response looks like this, note that you can expect to receive multiple results each containing their own `rowcount`:

```python
{
    'results': [
        {
            'rowcount': 1
        }, 
        {
            'rowcount': 1
        }
    ], 
    'cols': [], 
    'duration': 32.546875
}
```

Existing rows can also be updated:

```python
response = crate.execute(
    "UPDATE temp_humidity SET sensor_id = ? WHERE sensor_id = ?",
    [
        "a04",
        "a01"
    ]
)
```

The response includes the number of rows affected by the update:

```python
{
    'rows': [
        []
    ], 
    'rowcount': 5, 
    'cols': [], 
    'duration': 696.36975
}
```

#### Working with Objects and Arrays

CrateDB supports flexible storage and indexing of objects / JSON data.  To learn more about this, check out our [blog post](https://cratedb.com/blog/handling-dynamic-objects-in-cratedb) that explains the different ways objects can be stored.

Here are some basic examples showing how to store objects with micropython-cratedb and retrieve desired fields from them.

Assume a table with the following definition having a [dynamic object](https://cratedb.com/blog/handling-dynamic-objects-in-cratedb) column:

```sql
CREATE TABLE driver_object_test (
    id TEXT PRIMARY KEY, 
    data OBJECT(DYNAMIC)
)
```

Objects of arbitrary structure are inserted like this:

```python
response = crate.execute(
    "INSERT INTO driver_object_test (id, data) VALUES (?, ?)",
    [
        "2cae54",
        {
            "sensor_readings": {
                "temp": 23.3,
                "humidity": 61.2
            },
            "metadata": {
                "software_version": "1.19",
                "battery_percentage": 57,
                "uptime": 2851200
            }
        }
    ]
)
```

And values contained in objects can be retrieved selectively like this:

```python
response = crate.execute(
    """SELECT 
            id,
            data['metadata']['uptime'] AS uptime, 
            data['sensor_readings'] AS sensor_readings 
        FROM driver_object_test 
        WHERE id = ?""",
    [
        "2cae54"
    ]
)
```

`response` contains the matching records like this:

```python
{
    'rows': [
        [2851200, {'humidity': 61.2, 'temp': 23.3}]  
    ], 
    'rowcount': 1, 
    'cols': [
        'uptime', 'sensor_readings'
    ], 
    'duration': 4.047666
}
```

For more examples, see the [`object_examples.py`](examples/object_examples.py) script in the `examples` folder.

#### Deleting Data

Delete queries work like any other SQL statement:

```python
response = crate.execute(
    "DELETE FROM temp_humidity WHERE sensor_id = ?",
    [
        "a02"
    ]
)
```

And the response from the above looks like this, again including the number of rows affected:

```python
{
    'rows': [
        []
    ], 
    'rowcount': 3, 
    'cols': [], 
    'duration': 66.81604
}
```

#### Errors / Exceptions

The driver can throw the following types of exception:

* `NetworkError`: when there is a network level issue, for example the hostname cannot be resolved.
* `CrateDBError`: errors returned by the CrateDB cluster, for example when invalid SQL is submitted.

Here's an example showing how to catch a network error:

```python
crate = cratedb.CrateDB("nonexist", use_ssl=False)

try:
    response = crate.execute(
        "SELECT sensor_id, ts, temp FROM temp_humidity WHERE sensor_id = ? ORDER BY ts DESC",
        [
            "a01"
        ],
        with_types=True
    )
except cratedb.NetworkError as e:
    print("Network error:")
    print(e)
```

Output:

```python
Network error:
[addrinfo error 8]
```

This example shows a `CrateDBError`:

```python
try:
    response = crate.execute(
        "SELECT nonexist FROM temp_humidity"
    )
except cratedb.CrateDBError as e:
    print("CrateDB error:")
    print(e)
```

Output:

```python
CrateDB error:
{
    'error': {
        'message': 'ColumnUnknownException[Column nonexist unknown]', 
        'code': 4043
    }
}
```

Constants for each value of `code` are provided.  For example `4043` is `CRATEDB_ERROR_UNKNOWN_COLUMN `.

## Examples

The [`examples`](examples/) folder contains example MicroPython scripts, some of which are for specific microcontroller boards, including the popular Raspberry Pi Pico W.
Hardware-independent example programs also work well on CPython, and the
MicroPython UNIX and Windows port, see [Running on CPython](./docs/cpython.md)
and [Running on MicroPython](./docs/micropython.md).

## Testing

This driver library has been tested using the following MicroPython versions:

* **1.24.0** 
  * macOS/darwin ([install with Homebrew package manager](https://formulae.brew.sh/formula/micropython))
  * Raspberry Pi Pico W ([download](https://micropython.org/download/RPI_PICO_W/))
* **1.23.0** 
  * macOS/darwin ([install with Homebrew package manager](https://formulae.brew.sh/formula/micropython))
  * Raspberry Pi Pico W ([download](https://micropython.org/download/RPI_PICO_W/))
* **1.23.0 (Pimoroni build)**
  * Raspberry Pi Pico W ([download](https://github.com/pimoroni/pimoroni-pico/releases))

If you have other microcontroller boards that you can test the driver with or provide examples for, we'd love to receive a [pull request](/pulls)!

## Need Help?

If you need help, have a bug report or feature request, or just want to show us your project that uses this driver then we'd love to hear from you!

For bugs or feature requests, please raise an [issue](/issues) on GitHub.  We also welcome [pull requests](/pulls)!

If you have a project to share with us, or a more general question about this driver or CrateDB, please post in our [community forum](https://community.cratedb.com/).
