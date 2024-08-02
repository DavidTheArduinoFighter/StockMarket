import requests


def get_symbols():
    url = "http://localhost:4000/symbols"
    return requests.get(url).json()


def stocks():
    url = "http://localhost:4000/symbols"
    return requests.get(url).json()['logInCredentials']['twelveApiKey']