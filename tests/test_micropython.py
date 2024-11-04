# ruff: noqa: S605, S607
import os


def example_usage():
    """
    Validate `examples/example_usage.py` runs to completion.
    """
    assert os.system("micropython examples/example_usage.py") == 0


def object_examples():
    """
    Validate `examples/object_examples.py` runs to completion.
    """
    assert os.system("micropython examples/object_examples.py") == 0


if __name__ == "__main__":
    example_usage()
    object_examples()
