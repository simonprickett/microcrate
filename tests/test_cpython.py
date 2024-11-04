# ruff: noqa: S603, S607

import os
import subprocess
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def boot():
    """
    Add current working dir to Python module search path.

    This is needed to make the interpreter pick up `cratedb.py`
    in the top-level directory.
    """
    os.environ["PYTHONPATH"] = str(Path.cwd())


def test_example_usage(capfd):
    """
    Validate `examples/example_usage.py` runs to completion.
    """
    subprocess.check_call(["python", "examples/example_usage.py"])
    out, err = capfd.readouterr()
    assert "Create table" in out
    assert "Drop table" in out


def test_object_examples(capfd):
    """
    Validate `examples/object_examples.py` runs to completion.
    """
    subprocess.check_call(["python", "examples/object_examples.py"])
    out, err = capfd.readouterr()
    assert "Create table" in out
    assert "Drop table" in out


def test_picow_demo(capfd):
    """
    Validate `examples/picow_demo.py` fails, because it needs real hardware.
    """
    returncode = subprocess.call(["python", "examples/picow_demo.py"])
    assert returncode == 1
    out, err = capfd.readouterr()
    assert "ModuleNotFoundError: No module named 'machine'" in err
