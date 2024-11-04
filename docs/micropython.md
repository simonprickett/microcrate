# Running on MicroPython

The module is designed for [MicroPython]. You can run it on embedded systems,
and, thanks to the [MicroPython UNIX and Windows port], also on Linux, macOS,
and Windows.

While MicroPython on a workstation does not provide hardware support usually
available when running MicroPython on embedded devices, this is mostly not
a concern when running a database driver.


## Embedded

Todo.


## Workstation

### Setup

Install MicroPython.
```shell
{apt,brew,pip,zypper} install micropython
```

Install requirements.
```shell
micropython -m mip install base64 requests
```

## Usage

Start CrateDB.
```shell
docker run --rm -it --name=cratedb \
  --publish=4200:4200 --publish=5432:5432 \
  --env=CRATE_HEAP_SIZE=2g crate:latest -Cdiscovery.type=single-node
```

Invoke example programs.
```shell
export MICROPYPATH=".frozen:${HOME}/.micropython/lib:/usr/lib/micropython:$(pwd)"
micropython examples/example_usage.py
micropython examples/object_examples.py
```


[MicroPython]: https://en.wikipedia.org/wiki/Micropython
[MicroPython UNIX and Windows port]: https://docs.micropython.org/en/latest/unix/quickref.html
