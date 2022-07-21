import os


def parse_float(value: str) -> float | str:
    try:
        _value = float(value)
        return _value
    except ValueError:
        return value


def image_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0, os.SEEK_SET)
    return size
