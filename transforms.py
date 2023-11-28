from datetime import datetime


def quant_or_qual(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return -1


def is_datetime(val):
    if type(val) == datetime:
        return val

    return None


def read_scalar(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 1
