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

## Connecting to CrateDB

TODO

## Interacting with CrateDB

TODO



## Examples

The [`examples`](examples/) folder contains example MicroPython scripts, some of which are for specific microcontroller boards, including the popular Raspberry Pi Pico W.

## Testing

This driver library was tested using the following MicroPython versions:

* **1.23.0**
  * macOS/darwin
  * Raspberry Pi Pico W

If you have other microcontroller boards that you can test the driver with or provide examples for, we'd love to receive a pull request!