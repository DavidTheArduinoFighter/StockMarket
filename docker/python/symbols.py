import requests
import json


def get_symbols():
    url = "http://backend_api:4000/symbols"
    return requests.get(url).json()


def post_symbols(symbol_type, value, table):
    json_value = {
        "symbolType": symbol_type,
        "table": table,
        "symbol": value
    }

    url = "http://backend_api:4000/symbols"
    return requests.post(url, json_value)
