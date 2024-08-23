import requests


def twelve_data_key():
    url = "http://localhost:4000/credentials"
    return requests.get(url).json()['logInCredentials']['twelveApiKey']


def db_username():
    url = "http://localhost:4000/credentials"
    return requests.get(url).json()['db']['user']


def db_password():
    url = "http://localhost:4000/credentials"
    return requests.get(url).json()['db']['password']


def db_database():
    url = "http://localhost:4000/credentials"
    return requests.get(url).json()['db']['database']
