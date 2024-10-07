# MicroCrate - A CrateDB Driver for MicroPython

## Introduction

MicroCrate is a [CrateDB](https://cratedb.com) driver for the [MicroPython](https://micropython.org) language.

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

For more examples, check out [`example_usage.py`](./example_usage.py).

## Testing

This driver library was tested using the following MicroPython versions:

* **1.23.0**
  * macOS/darwin
  * Raspberry Pi Pico W