from functools import lru_cache


@lru_cache(None)
def __raw_data():
    pass


def json():
    return {}


def csv():
    return {}
