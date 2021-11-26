def try_int(text) -> int:
    try:
        return int(text)
    except ValueError:
        return None


def try_float(text) -> float:
    try:
        return float(text)
    except ValueError:
        return None
