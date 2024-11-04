# Running on CPython

The module is designed for [MicroPython], but also works on [CPython].

While CPython does not provide hardware support usually available when
running MicroPython on embedded devices, this is mostly not a concern
when running a database driver.


## Setup

Install Python package and project manager [uv].
```shell
{apt,brew,pip,zypper} install uv
```

Create virtualenv, and install requirements.
```shell
uv venv
uv pip install requests
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
source .venv/bin/activate
export PYTHONPATH=$(pwd)
python examples/example_usage.py
python examples/object_examples.py
```


[CPython]: https://en.wikipedia.org/wiki/Cpython 
[MicroPython]: https://en.wikipedia.org/wiki/Micropython
[uv]: https://docs.astral.sh/uv/
