import requests
import os


def is_docker():
    return os.path.exists('/.dockerenv')


local_or_docker = 'backend_api' if is_docker() else 'localhost'


def get_symbols():
    url = f'http://{local_or_docker}:4000/symbols'
    return requests.get(url).json()


def post_symbols(symbol_type, value, table):
    json_value = {
        "symbolType": symbol_type,
        "table": table,
        "symbol": value
    }

    url = f'http://{local_or_docker}:4000/symbols'
    return requests.post(url, json_value)
