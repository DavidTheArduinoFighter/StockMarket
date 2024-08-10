import requests
import mariadb
import sys
from datetime import timedelta, datetime, date
import time
import hashlib
import credentials
import symbols


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


def get_symbol_list(json_res):
    all_symbols = []

    for symbol_list in json_res:
        for symbol in json_res[symbol_list]:
            if not symbol:
                continue
            all_symbols.append(symbol)

    return all_symbols

class StockData:
    def __init__(self):
        self.symbol = None
        self.cur = connect_to_db()
        self.table_name = None
        self.hkey = []
        self.last_date_reached = False
        self.last_write_date = None
        self.start_date = date.today()  # today won't be inserted in db (to avoid potential errors)

    def fill_db(self, symbol, table_name, years=None):
        self.table_name = table_name
        if years is None:
            years = 25
        self.make_new_stock_table()
        self.last_write_date = self.get_last_db_date()

        for i in range(years * 2):
            start_date, end_date = self.get_interval_data(183)
            is_error = self.add_to_db_price_interval(end_date, start_date, symbol)
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

    def add_to_db_price_interval(self, start_date, end_date, symbol,num_of_data=5000):
        result = twelve_api(num_of_data, start_date, end_date, symbol)
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


    def test_symbol(self, symbol, symbol_type, table_name):
        allowed_symbol_type = ['stocks', 'etf', 'benchmark']
        if symbol_type not in allowed_symbol_type:
            print('Allowed types are: benchmark, etf or stocks!')
            return

        res = symbols.get_symbols()
        existed_symbols = get_symbol_list(res)
        if any(d['table'] == table_name for d in existed_symbols) and not symbol_type == 'benchmark':
            print('Table already in use!')
            return

        result = twelve_api(20, '2024-07-04', '2024-07-06', symbol)

        if 'code' in result['data'][0]:
            print('Error in test!')
            err_code = result['data'][0]['code']
            print(f'Code: {err_code}')
            err_msg = result['data'][0]['message']
            print(f'Message: {err_msg}')
            return

        print('Symbol is valid!')

        if symbol_type != 'benchmark':
            if symbol not in existed_symbols:
                symbols.post_symbols(symbol_type, symbol, table_name)
                print('Symbol added!')
            else:
                print('Already existed!')
        elif not res['benchmark'] or res['benchmark'][0] != symbol:
            symbols.post_symbols(symbol_type, symbol, table_name)
            print('Symbol added!')
        else:
            print('Already existed!')


class UpdateAllDb(StockData):
    def __init__(self):
        super().__init__()

    def update_tables(self):
        all_symbols_data = get_symbol_list(symbols.get_symbols())
        for symbol_data in all_symbols_data:
            if not symbol_data['symbol'] or not symbol_data['table']:
                continue
            super().fill_db(symbol_data['symbol'], symbol_data['table'])


if __name__ == '__main__':
    testSym = TestSymbol()
    testSym.test_symbol('AAPL', 'stocks', 'Aple')
    # saveData = StockData('Nasdaq100Nasdaq')
    # saveData.fill_db('NDX')
    # run = UpdateAllDb()
    # run.update_tables()
