import requests


def twelve_data_key():
    url = "http://localhost:4000/twelvedata"
    return requests.get(url).json()['logInCredentials']['twelveApiKey']
