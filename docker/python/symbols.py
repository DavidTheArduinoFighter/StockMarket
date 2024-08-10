import requests


def get_symbols():
    url = "http://localhost:4000/symbols"
    return requests.get(url).json()


def post_symbols(value):
    json_value = value  # TODO: transform to json value -- add value to json
    url = "http://localhost:4000/symbols"
    return requests.post(url, json_value)
