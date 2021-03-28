from config import *
import sqlite3, tulipy, numpy
import pandas as pd
import alpaca_trade_api as tradeapi
from datetime import date

connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

#Pulls list of stocks in database
cursor.execute("""
    SELECT id, symbol FROM stock
""")
rows = cursor.fetchall()

#generates a list of symbols sotred in the stock database for use in the price database
symbols = []
idnumbers = []
stock_dict ={}

for row in rows:
    symbol = row['symbol']
    id = row['id']
    print(f"Processing symbol {symbol}, stock-id = {id}")
    query ="""
    SELECT * FROM stock_price WHERE stock_id = ? ORDER BY date
    """
    cursor.execute(query,(id, ))
    stocks = cursor.fetchall()
    
    recent_closes = []
    recent_highs = []
    recent_lows = []
    recent_volume = []

    for stock in stocks:

