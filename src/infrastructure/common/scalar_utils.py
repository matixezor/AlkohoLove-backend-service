def parse_float(value: str) -> float | str:
    try:
        _value = float(value)
        return _value
    except ValueError:
        return value
