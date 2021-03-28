from config import *
import sqlite3
import pandas as pd

#create new database for stock and stock price
connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

#Pulls list of stocks in database
cursor.execute("""
    SELECT id, symbol FROM stock
""")
rows = cursor.fetchall()
symbols = []
stock_dict ={}

for row in rows:
    print(row)
    symbol = row[1]
    symbols.append(symbol)
    stock_dict[symbol] = row[0]

current_date = '2021-03-08'
#Find Stocks where trend is POSITIVE per MACD = stocks_bullish
query1 = """
    SELECT * FROM stock_review WHERE macd_a < 0 AND macd_a > macd_a_signal and date = ? ORDER BY rsi_14 DESC
    """
stocks_bullish = pd.read_sql_query(query1, connection, params=(current_date,))
q = len(stocks_bullish)
print(f"Total of {q} bullish stocks. They are as follows:")
print(stocks_bullish)

#Find Stocks where trend NEGATIVE per MACD = stocks_bearish
#select * from stock_review where macd_a < macd_a_signal and date = '2021-03-19'
query2 = """
    SELECT * FROM stock_review WHERE macd_a > 0 AND macd_a < macd_a_signal and date = ? ORDER BY rsi_14 ASC
    """
stocks_bearish = pd.read_sql_query(query2, connection, params=(current_date,))
q = len(stocks_bearish)
print(f"Total of {q} bearish stocks. They are as follows:")
print(stocks_bearish)

#Price Increasing and MACD recording lower highs = bearish divergence (stock_01)
#Price Decreasing and MACD recording higher lows = bullish divergence (stock_02)

#Find stocks where oversold and positive trend - Buy
rsi_limit = 40
adx_limit = 25
query3 ="""
    SELECT stock_id FROM stock_review WHERE rsi_14 < ? AND date = ? and adx > ? AND plus_di > minus_di ORDER BY rsi_14 ASC LIMIT 15
    """ 
stocks_03 = pd.read_sql_query(query3, connection, params=(rsi_limit, current_date, adx_limit,))
print(stocks_03)

#stocks_03 = stocks_03.set_index('stock_id')
#print(stocks_03)

for row in stocks_03['stock_id']:
    print(row)
    cursor.execute("""
    INSERT INTO stock_strategies(stock_id, strategy_id) VALUES(?,?)
    """, (row,3))
connection.commit()



#Find Stocks Trending Down


#cursor.execute("""
    #DELETE FROM stock_strategies
#""")


#for row in stocks-01:
    #cursor.execute("""
    #INSERT INTO stock_strategy(stock_id, strategy_id) VALUES(?,1)
    #""", (row))
#connection.commit()

