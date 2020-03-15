from typing import List
from requests import get


def download(*urls: List[str]):
    def fetch(url):
        result = get(url)
        if 'application/json' in result.headers['content-type']:
            return result.json()
        else:
            return result.content

    return [fetch(url) for url in urls]
