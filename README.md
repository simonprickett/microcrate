# MicroCrate - A CrateDB Driver for MicroPython

## Introduction

MicroCrate is a [CrateDB](https://cratedb.com) driver for the [MicroPython](https://micropython.org) language.  It connects to CrateDB using the [HTTP Endpoint](https://cratedb.com/docs/crate/reference/en/latest/interfaces/http.html).

To use this, you'll need a CrateDB database cluster.  Sign up for our cloud free tier [here](https://console.cratedb.cloud/) or get started with Docker [here](https://hub.docker.com/_/crate).

Want to learn more about CrateDB?  Take our free [Fundamentals course](https://learn.cratedb.com/course-overview) at the CrateDB Academy.

## Installation

### Installing Dependencies

This driver uses the base64 implementation from [`micropython-lib`](https://github.com/micropython/micropython-lib/).  Install it on your device by first establishing a network connection, then entering the following commands:

```python
import mip
mip.install('base64')
```

Alternatively, copy [this file](https://github.com/micropython/micropython-lib/blob/master/python-stdlib/base64/base64.py) to your device manually using [`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html), [Thonny](https://thonny.org/) or whichever IDE you normally use for MicroPython projects.

### Installing MicroCrate

TODO

## Using the Driver in a MicroPython Script

Import the driver like this:

```python
import microcrate
```

### Connecting to CrateDB

Connect to a CrateDB cluster in the cloud by providing hostname, user name and password:

```python
crate = microcrate.CrateDB(
    host="host", 
    user="user", 
    password="password"
)
```

The driver uses SSL by default.

If you're running CrateDB locally (with Docker for example), connect like this:

```python
crate = microcrate.CrateDB(
    host="hostname", 
    use_ssl=False
)
```

The driver will connect to port 4200 unless you provide an alternative value:

```python
crate = microcrate.CrateDB(
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
    "SELECT sensor_id, ts, temp, humidity FROM temp_humidity WHERE sensor_id = ? ORDER BY ts DESC",
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

TODO

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
crate = microcrate.CrateDB("nonexist", use_ssl = False)

try:
    response = crate.execute(
        "SELECT sensor_id, ts, temp FROM temp_humidity WHERE sensor_id = ? ORDER BY ts DESC",
        [
            "a01"
        ],
        with_types=True
    )
except microcrate.NetworkError as e:
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
except microcrate.CrateDBError as e:
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

## Testing

This driver library was tested using the following MicroPython versions:

* **1.23.0** ([download](https://micropython.org/download/))
  * macOS/darwin
  * Raspberry Pi Pico W
* **1.23.0 (Pimoroni build)** ([download](https://github.com/pimoroni/pimoroni-pico/releases))
  * Raspberry Pi Pico W

If you have other microcontroller boards that you can test the driver with or provide examples for, we'd love to receive a pull request!
