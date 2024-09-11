import sys
from datetime import timedelta, datetime, date
import time
import hashlib
import symbols
import helper
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
import StockMarketUI


class StockData:
    def __init__(self):
        self.symbol = None
        self.cur = helper.connect_to_db()
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

        if self.last_write_date and self.last_write_date.date() == helper.get_last_working_day(self.start_date):
            msg = f'Data for table {table_name} (symbol: {symbol}) already up to date.'
            print(msg)
            return msg

        for i in range(years * 2):
            start_date, end_date = self.get_interval_data(183)
            is_error, msg = self.add_to_db_price_interval(end_date, start_date, symbol)
            if is_error or self.last_date_reached:
                return msg
            time.sleep(9)  # to not exceed max api calls per minute

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

    def add_to_db_price_interval(self, start_date, end_date, symbol, num_of_data=5000):
        result = helper.twelve_api(num_of_data, start_date, end_date, symbol)
        if result['data'][0]['status'] == 'error':
            message = result['data'][0]['message']
            print(f'Error: {message}')
            return True, f'Error: {message}'
        self.write_table(result)
        return False, ''

    def write_table(self, result):
        values = result['data'][0]['values']

        print('Started writing data to DB')
        start = time.time()
        for value in values:

            hkey = hashlib.md5(bytes(value['datetime'] + self.table_name, 'utf-8')).hexdigest()

            if self.last_write_date and self.last_write_date.date() == datetime.fromisoformat(value['datetime']).date():
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
        self.cur = helper.connect_to_db()

    def test_symbol(self, symbol, symbol_type, table_name, ui_output=False):
        if not (symbol and symbol_type and table_name and ui_output):
            msg = 'All data need to be inserted!'
            return msg

        allowed_symbol_type = ['stocks', 'etf', 'benchmark']
        if symbol_type not in allowed_symbol_type:
            msg = 'Allowed types are: benchmark, etf or stocks!'
            print(msg)
            if ui_output:
                return msg
            return

        res = symbols.get_symbols()
        existed_symbols = helper.get_symbol_list(res)
        if any(d['table'] == table_name for d in existed_symbols) and not symbol_type == 'benchmark':
            msg = 'Table already in use!'
            print(msg)
            if ui_output:
                return msg
            return

        result = helper.twelve_api(20, '2024-07-04', '2024-07-06', symbol)

        if 'code' in result['data'][0]:
            msg = 'Error in test!'
            print(msg)
            err_code = result['data'][0]['code']
            print(f'Code: {err_code}')
            err_msg = result['data'][0]['message']
            print(f'Message: {err_msg}')

            msg = msg + f'Message: {err_msg}'
            if ui_output:
                return msg

        msg = 'Symbol is valid!'
        print(msg)

        if symbol_type != 'benchmark':
            if symbol not in existed_symbols:
                symbols.post_symbols(symbol_type, symbol, table_name)
                print('Symbol added!')
                if ui_output:
                    return msg + ' Symbol added!'
            else:
                print('Already existed!')
                if ui_output:
                    return msg + ' Already existed!'

        elif not res['benchmark'] or res['benchmark'][0] != symbol:
            symbols.post_symbols(symbol_type, symbol, table_name)
            print('Symbol added!')
            if ui_output:
                return msg + ' Symbol added!'
        else:
            print('Already existed!')
            if ui_output:
                return msg + ' Already existed!'

        # TODO: check if we don't have benchmark of we want to update benchmark


class UIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = StockMarketUI.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.testSymbolPushButton.clicked.connect(self.test_symbol)
        self.ui.updateDBpushButton.clicked.connect(self.update_database)

    def test_symbol(self):
        symbol_type = self.ui.testSymoblTypeInput.text()
        symbol_name = self.ui.testSymbolSymbolInput.text()
        table_name = self.ui.testSymbolTableNameInput.text()

        print(f'{symbol_type} {symbol_name} {table_name}')

        testSym = TestSymbol()
        msg = testSym.test_symbol(symbol_name.upper(), symbol_type, table_name, True)
        self.ui.resultOutputTestSymbol.setPlainText(msg)

    def update_database(self):
        print('Updating database')
        self.ui.resultUpdate.setPlainText('Date base will be updated, please wait, it could take a while!')
        QTimer.singleShot(100, self.perform_update)

    def perform_update(self):
        update_tables()
        self.ui.resultUpdate.setPlainText('Date base will be updated, please wait, it could take a while!\n'
                                          'Date base updated, now you can use library!')


def update_tables():
    all_symbols_data = helper.get_symbol_list(symbols.get_symbols())
    for symbol_data in all_symbols_data:
        if not symbol_data['symbol'] or not symbol_data['table']:
            continue
        print(f'Updating {symbol_data["symbol"]}, table {symbol_data["table"]}.')
        save_data = StockData()
        save_data.fill_db(symbol_data['symbol'], symbol_data['table'])
        print("----------------------------------------------------------")


if __name__ == '__main__':
    # while True:
    #     time.sleep(10)
    #     print(time.time())
    """
    first_time = True
    while True:
        if first_time:
            print("Welcome to Get data console app!")
            print("You have following possibilities, type (just) number to select what to do:")
            first_time = False
        else:
            print("You can choose again:")
        print("\t 1 - Test symbol")
        print("\t 2 - Update all database with new data")
        print("\t 3 - Debug program (use just if you know what are you doing!)")
        print("\t 4 - Exit")

        user_select = input("Enter number that you chose: ")

        match user_select:
            case '1':
                while True:
                    print("You selected to test symbol. If symbol is valid, it will be added in json.")
                    print("When you run update all database (number 2) the symbol will be used from json.")
                    print("You need to insert symbol, in what type do you want to save it (stocks/etf/benchmark), "
                          " and what will be table name.")
                    print("Benchmark involve only one symbol.")
                    print("Be aware, if table already exist with inserted name, than you need to change it to be uniq. Choose names"
                          " wisely!")
                    inserted_symbol_name = input("Enter symbol name: ")
                    inserted_symbol_type = input("Enter type of symbol(stocks/etf/benchmark): ")
                    inserted_table_name = input("Enter table name: ")
                    testSym = TestSymbol()
                    testSym.test_symbol(inserted_symbol_name.upper(), inserted_symbol_type, inserted_table_name)

                    print("Do you want to test another symbol?")
                    test_symbol_answer = input("Enter y/n: ")

                    if test_symbol_answer == 'n':
                        prog_exit = input("Do you want to exit program? (y/n): ")
                        if prog_exit == 'y':
                            sys.exit(0)
                        break
            case '2':
                print("You selected to update database, just sit down and relax, we will notify you when process will be"
                      " finished.")
                print("P. S.: Just make sure that you have already tested some symbols (and so filled the json,"
                      " which will provide data for update). You need at least one symbol for stocks \n or etf and benchmark"
                      " symbol.")
                update_tables()
                print("All up to date.")
                prog_exit = input("Do you want to exit program? (y/n): ")
                if prog_exit == 'y':
                    sys.exit(0)
            case '3':
                print("This section is more for debugging or \"hacking\" constructed program, be aware of this!")
                print("You will update chosen symbol, but symbol will not be tested first. Do you want to continue?")
                debug_answer = input("Type y/n ")
                if debug_answer == 'y':
                    while True:
                        debug_symbol_name = input("Enter symbol name: ")
                        debug_table_name = input("Enter table name: ")
                        debug_save_data = StockData()
                        debug_save_data.fill_db(debug_symbol_name, debug_table_name)

                        print("Do you want to insert another symbol?")
                        debug_symbol_answer = input("Enter y/n: ")

                        if debug_symbol_answer == 'n':
                            prog_exit = input("Do you want to exit program? (y/n): ")
                            if prog_exit == 'y':
                                sys.exit(0)
                            break
            case '4':
                sys.exit(0)
"""
    # TODO: library for use of database

    app = QApplication(sys.argv)
    run_app = UIApp()
    run_app.show()  # Show the main window
    sys.exit(app.exec())
