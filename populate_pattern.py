from config import *
import sqlite3, tulipy, numpy, talib
import pandas as pd
import alpaca_trade_api as tradeapi

connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

def bearish_candle(candle):
    return(candle['close'] <)

#determine if list of items A is diverging or converging with list of items B
def divergence( a, b):
    start = []
    end = []
    flag = []
    for row in a.joinb on date:
        start = row
        end = 
    return(pass)