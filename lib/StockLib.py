from docker.python.helper import connect_to_db, disconnect_from_db
from docker.python.symbols import get_symbols


# Dic to store stock symbols and their tables
symbol_table_mapping = None


def fetch_symbol_data():
    """Fetch JSON data of stock symbols and build the dictionary."""
    global symbol_table_mapping
    if symbol_table_mapping is None:
        print("Fetching symbol data for the first time...")

        symbol_data = get_symbols()

        symbol_table_mapping = {}
        for category in symbol_data:
            for item in symbol_data[category]:
                symbol = item['symbol']
                table_name = item['table']
                symbol_table_mapping[symbol] = table_name
    else:
        print("Symbol data already loaded.")


def get_table_name(symbol):
    """Fetch the table name for the specified stock symbol."""
    if symbol_table_mapping is None:
        fetch_symbol_data()  # Load symbol data only once
    return symbol_table_mapping.get(symbol, None)


def query_db_for_symbol(symbol):
    """Query the database for the specified stock symbol using the table name."""
    table_name = get_table_name(symbol)
    if table_name is None:
        raise ValueError(f"No table found for symbol: {symbol}")

    # Connect to the database using the credentials module
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(
        f'SELECT price_date, open_price, close_price, high_price, low_price, volume FROM {table_name} n ORDER BY price_date ASC'
    )

    disconnect_from_db(conn)

    stock_data = cur.fetchall()

    return stock_data


def get_stock_data(symbol):
    return query_db_for_symbol(symbol)


def get_benchmark_data():
    # TODO
    pass
