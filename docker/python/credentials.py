import requests
import os


def is_docker():
    return os.path.exists('/.dockerenv')


local_or_docker = 'backend_api' if is_docker() else 'localhost'


def twelve_data_key():
    url = f'http://{local_or_docker}:4000/credentials'
    return requests.get(url).json()['logInCredentials']['twelveApiKey']


def db_username():
    url = f'http://{local_or_docker}:4000/credentials'
    return requests.get(url).json()['db']['user']


def db_password():
    url = f'http://{local_or_docker}:4000/credentials'
    return requests.get(url).json()['db']['password']


def db_database():
    url = f'http://{local_or_docker}:4000/credentials'
    return requests.get(url).json()['db']['database']
