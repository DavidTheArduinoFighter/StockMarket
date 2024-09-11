import requests
import mariadb
import credentials
from datetime import timedelta, date
import sys
import os

class MonthDay:
    def __init__(self, month, day):
        self.month = month
        self.day = day


stock_holidays_fixed = [
    MonthDay(1, 1),
    MonthDay(6, 19),
    MonthDay(12, 25)
]


def is_docker():
    return os.path.exists('/.dockerenv')


# TODO: move functions that could be moved in new "library python file"
def connect_to_db():
    try:
        conn = mariadb.connect(
            user=credentials.db_username(),
            password=credentials.db_password(),
            host='mariadb' if is_docker() else 'localhost',
            port=3306,
            database=credentials.db_database(),
            autocommit=True
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()

    return cur


def twelve_api(output_size, start_date, end_date, symbol='NDX', intervals='15min'):
    url = f'https://api.twelvedata.com/complex_data?apikey={credentials.twelve_data_key()}'

    data = {
        "symbols": [symbol],
        "intervals": [intervals],
        "start_date": start_date,
        "end_date": end_date,
        "outputsize": output_size,
        "methods": [
            "time_series"
        ]
    }

    print(f'Api post')
    result = post(url, data)
    print(f'Api results received')

    return result


def post(url, json_data):
    api_return = requests.post(url, json=json_data)
    return api_return.json()


def get_symbol_list(json_res):
    all_symbols = []

    for symbol_list in json_res:
        for symbol in json_res[symbol_list]:
            if not symbol:
                continue
            all_symbols.append(symbol)

    return all_symbols


def get_last_working_day(checked_date):
    diff = 1
    # holidays
    today = date.today()

    for holiday in stock_holidays_fixed:
        if today.month == holiday.month and today.day == holiday.day:
            checked_date = checked_date - timedelta(days=diff)

    # weekend
    if checked_date.weekday() == 0:
        diff = 3
    elif checked_date.weekday() == 6:
        diff = 2

    # subtracting diff
    return checked_date - timedelta(days=diff)