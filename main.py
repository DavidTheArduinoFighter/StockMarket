from lib import StockLib

apple = StockLib.get_stock_data('AAPL')
benchmark = StockLib.get_benchmark_data()

for item in benchmark:
    print(item)
    print(item[0])
    print(item[1])
    print(item[2])
    print(item[3])
    print(item[4])
    print(item[5])
    print('-------------------')