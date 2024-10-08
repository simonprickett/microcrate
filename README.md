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

CrateDB is a SQL database: you'll store, update and retieve data using SQL statements.

#### Retrieving Data

The `execute` method sends a SQL statement to the database for execution, and returns the result:

```python
TODO
```

You can also use parameterized queries:

```python
TODO
```

Data is returned as a dictionary that looks like this:

```python
TODO
```

Use the `with_types` parameter to have CrateDB return information about the data type of each column in the resultset. This feature is off by defaault to minimize network bandwidth.

```python
TODO
```

The resultset then contains an extra key, `col_types`:

```python
TODO
```

Constants are provided for each type.  For example type `12` is `CRATEDB_TYPE_OBJECT`.

#### Inserting / Updating Data

Here's an example insert statement:

```python
TODO
```

The response from CrateDB looks like this:

```python
TODO
```

If you don't need a response, set the `return_response` parameter to `False` (default is `True`). This will save a small amount of time that the driver normally spends on processing the response.

```python
TODO
```

Here's an example of a parameterized insert statement:

```python
TODO
```

You can add multiple records in a single network round trip using a bulk insert:

```python
TODO
```

Existing rows can also be updated:

```python
TODO
```

The response looks like this:

```python
TODO
```

#### Deleting Data

Delete queries work like any other SQL statement:

```python
TODO
```

And the response from the above looks like this:

```python
TODO
```

#### Errors / Exceptions

TODO

## Examples

The [`examples`](examples/) folder contains example MicroPython scripts, some of which are for specific microcontroller boards, including the popular Raspberry Pi Pico W.

## Testing

This driver library was tested using the following MicroPython versions:

* **1.23.0**
  * macOS/darwin
  * Raspberry Pi Pico W

If you have other microcontroller boards that you can test the driver with or provide examples for, we'd love to receive a pull request!