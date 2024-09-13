from docker.python.helper import connect_to_db, disconnect_from_db
from docker.python.symbols import get_symbols


# Dic to store stock symbols and their tables
symbol_table_mapping = dict()
benchmark_table_name = None


def fetch_symbol_data():
    """Fetch JSON data of stock symbols and build the dictionary."""
    global symbol_table_mapping
    global benchmark_table_name

    if not symbol_table_mapping:
        print("Fetching symbol data for the first time...")

        symbol_data = get_symbols()

        symbol_table_mapping = {}
        for category in symbol_data:
            if category == 'benchmark':
                benchmark_table_name = symbol_data[category][0]['table']
            else:
                extract_symbol_data(symbol_data[category], symbol_table_mapping)

    else:
        print("Symbol data already loaded.")


def extract_symbol_data(symbol_data, dict_name):
    for item in symbol_data:
        symbol = item['symbol']
        table_name = item['table']
        dict_name[symbol] = table_name


def get_table_name(symbol):
    """Fetch the table name for the specified stock symbol."""
    if not symbol_table_mapping:
        fetch_symbol_data()  # Load symbol data only once
    return symbol_table_mapping.get(symbol, None)


def data_for_symbol(symbol):
    table_name = get_table_name(symbol)
    if table_name is None:
        raise ValueError(f"No table found for symbol: {symbol}")

    return get_db_data(table_name)


def get_db_data(table_name):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        f'SELECT price_date, open_price, close_price, high_price, low_price, volume FROM {table_name} n ORDER BY price_date ASC'
    )
    stock_data = cur.fetchall()

    disconnect_from_db(conn)

    return stock_data


def get_stock_data(symbol):
    return data_for_symbol(symbol)


def get_benchmark_data():
    return get_db_data(benchmark_table_name)
