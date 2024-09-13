import unittest
from lib.StockLib import get_table_name, data_for_symbol


class TestStockLib(unittest.TestCase):

    def test_get_table_name(self):
        symbol = "AAPL"
        table_name = get_table_name(symbol)
        self.assertIsNotNone(table_name, "Table name should not be None for a valid symbol.")

    def test_query_db_for_symbol(self):
        symbol = "AAPL"
        result = data_for_symbol(symbol)
        self.assertGreater(len(result), 0, "Query should return data for valid symbol.")


if __name__ == "__main__":
    unittest.main()
