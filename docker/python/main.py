import requests
import mariadb
import sys
from datetime import timedelta, datetime, date
import time
import hashlib
import credentials


def connect_to_db():
    try:
        conn = mariadb.connect(
            user='stock_data_user',
            password='stock_data_pass',
            host='localhost',
            port=3306,
            database='StockDB',
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


class StockData:
    def __init__(self, table_name):
        self.cur = connect_to_db()
        self.table_name = table_name
        self.hkey = []
        self.last_date_reached = False
        self.last_write_date = None
        self.start_date = date.today()  # today won't be inserted in db (to avoid potential errors) datetime(2024, 7, 20)

    def fill_db(self, years=None):
        if years is None:
            years = 25
        self.make_new_stock_table()
        self.last_write_date = self.get_last_db_date()

        for i in range(years * 2):
            start_date, end_date = self.get_interval_data(183)
            is_error = self.add_to_db_price_interval(end_date, start_date)
            if is_error or self.last_date_reached:
                return
            time.sleep(9)   # to not exceed max api calls per minute

        print(f'Size of hkey list is: {sys.getsizeof(self.hkey)}')

    def make_new_stock_table(self):
        self.cur.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                hkey varchar(32),
                price_date DATETIME,
                open_price FLOAT(24),
                close_price FLOAT(24),
                high_price FLOAT(24),
                low_price FLOAT(24),
                volume BIGINT
                );"""
        )

    def add_to_db_price_interval(self, start_date, end_date, num_of_data=5000):
        result = twelve_api(num_of_data, start_date, end_date)
        if result['data'][0]['status'] == 'error':
            message = result['data'][0]['message']
            print(f'Error: {message}')
            return True
        self.write_table(result)

    def write_table(self, result):
        values = result['data'][0]['values']

        print('Started writing data to DB')
        start = time.time()
        for value in values:

            hkey = hashlib.md5(bytes(value['datetime'] + self.table_name, 'utf-8')).hexdigest()

            if self.last_write_date and self.last_write_date.strftime('%Y-%m-%d') == datetime.fromisoformat(value['datetime']).strftime('%Y-%m-%d'):
                self.last_date_reached = True
                print('All new data populated')
                return

            # Avoiding same data input
            if self.check_last_data_hkey(hkey):
                prevented_date = value['datetime']
                print(f'Warning population of was prevented for date: {prevented_date}')
                continue

            self.add_db_api_data(value['datetime'], value['open'], value['close'], value['high'], value['low'],
                                 value['volume'])
        print(f'Finished writing data to DB. Time elapsed: {time.time() - start}')

    def add_db_api_data(self, price_date, open_price, close_price, high_price, low_price, volume):
        self.cur.execute(
            f'INSERT INTO {self.table_name}(hkey, price_date, open_price, close_price, high_price, low_price, volume) VALUES (MD5(?), ?, ?, ?, ?, ?, ?)',
            (price_date + self.table_name, price_date, open_price, close_price, high_price, low_price, volume))

    def get_interval_data(self, num_of_days):
        start_date = (self.start_date - timedelta(days=num_of_days))
        end_date = self.start_date
        self.start_date = start_date

        return end_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d')

    def get_last_db_date(self):
        self.cur.execute(
            f'SELECT price_date FROM {self.table_name} n ORDER BY price_date DESC LIMIT 1'
        )

        price_date = self.cur.fetchone()

        return price_date[0] if price_date else None

    def check_last_data_hkey(self, hkey):
        if hkey not in self.hkey:
            self.hkey.append(hkey)
            return False
        return True


class TestSymbol:
    def __init__(self):
        self.cur = connect_to_db()

    def test_symbol(self, symbol):
        try:
            self.delete_stock_table(symbol)
            self.make_new_stock_table(symbol)
            result = twelve_api(20, '2024-07-04', '2024-07-06', symbol)
            self.write_table(symbol, result)
            self.delete_stock_table(symbol)
            print('Symbol is valid!')
        except Exception as e:
            print(f'Symbol is invalid! Error: {e}')

    def delete_stock_table(self, table_name):
        self.cur.execute(f'DROP TABLE IF EXISTS {table_name}')

    def make_new_stock_table(self, table_name):
        self.cur.execute(
            f"""CREATE TABLE {table_name} (
                hkey varchar(32),
                price_date DATETIME,
                open_price FLOAT(24),
                close_price FLOAT(24),
                high_price FLOAT(24),
                low_price FLOAT(24),
                volume BIGINT
                );"""
        )

    def write_table(self, table_name, result):
        values = result['data'][0]['values']

        print('Started writing data to DB')
        start = time.time()
        for value in values:
            self.add_db_api_data(value['datetime'], value['open'], value['close'], value['high'], value['low'],
                                 value['volume'], table_name)
        print(f'Finished writing data to DB. Time elapsed: {time.time() - start}')

    def add_db_api_data(self, price_date, open_price, close_price, high_price, low_price, volume,
                        table_name='AppleNasdaq'):
        self.cur.execute(
            f'INSERT INTO {table_name}(hkey, price_date, open_price, close_price, high_price, low_price, volume) VALUES (MD5(?), ?, ?, ?, ?, ?, ?)',
            (price_date + table_name, price_date, open_price, close_price, high_price, low_price, volume))


if __name__ == '__main__':
    # testSym = TestSymbol()
    # testSym.test_symbol('NDX')
    saveData = StockData('Nasdaq100Nasdaq')
    saveData.fill_db()
