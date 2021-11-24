def try_int(text) -> int:
    try:
        return int(text)
    except ValueError:
        return None
