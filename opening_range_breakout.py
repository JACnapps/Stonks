from config import *
import alpaca_trade_api as tradeapi
from datetime import datetime
import pandas as pd
import smtplib, ssl
import sqlite3

context = ssl.create_default_context()

strategy_id = 1

connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, name FROM stock JOIN stock_strategy ON stock_strategy.stock_id = stock.id WHERE stock_strategy.strategy_id = ?
   """, (strategy_id,))

stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks]

#symbols = ['MSF
#T', 'NIO', 'GD', 'WPC', 'LMT', 'C', 'BAC', 'INTC', 'ACB', 'UBER', 'STT', 'BIDU', 'ALB', 'WMT', 'BABA', 'AAL', 'CVS', 'TEVA', 'XOM', 'GM', 'T', 'GE', 'GME', 'AMC', 'EZGO']
print (symbols)

#calulcate first 15 minute bar and make trade based on movement
#current_date = date.date.today()
current_date = '2021-03-05'
start_bar = f"{current_date} 09:30:00-05:00"
end_bar = f"{current_date} 09:45:00-05:00"


api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)
orders = api.list_orders(status = 'all', after=f"{current_date}T13:30:00Z")
existing_order_symbols = [order.symbol for order in orders]

messages = []

for symbol in symbols:
    
   #minute_bars = api.get_barset(symbol, '5Min', start = '2021-03-05T09:30:00-05:00', end = '2021-03-05T16:30:00-05:00')
    minute_bars = api.get_barset(symbol, '5Min', start=start_bar).df
    minute_bars.columns = minute_bars.columns.droplevel(0)
    #print(minute_bars)
    print(symbol)
        
    opening_range_mask = (minute_bars.index >= start_bar) & (minute_bars.index < end_bar)
    opening_range_bars = minute_bars.loc[opening_range_mask]
    print(opening_range_bars)

    opening_range_low = opening_range_bars['low'].min()
    opening_range_high = opening_range_bars['high'].max()
    opening_range = opening_range_high - opening_range_low 
    print(opening_range_low)
    print(opening_range_high)
    print(opening_range)

    after_opening_range_mask = minute_bars.index >= end_bar
    after_opening_range_bars = minute_bars.loc[after_opening_range_mask]

    after_opening_range_breakout = after_opening_range_bars[after_opening_range_bars['close'] > opening_range_high]

    if not after_opening_range_breakout.empty:
        if symbol not in existing_order_symbols:
            limit_price = after_opening_range_breakout.iloc[0]['close']
 
            messages.append(f"placing order for {symbol} at {limit_price}, closed above {opening_range_high}\n\n{after_opening_range_breakout.iloc[0]}\n\n")
        
            api.submit_order(
                symbol = symbol,
                qty = 10,
                side = 'buy',
                type = 'limit',
                time_in_force = 'day',
                order_class = 'bracket',
                limit_price = limit_price,
                take_profit = dict(
                    limit_price = limit_price + opening_range, 
                ),
                stop_loss = dict(
                    stop_price = limit_price - opening_range,
                )
            )
        else:
            print(f"Alreay an order for {symbol}, skipping")

print(messages)
with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    email_message = "\n\n".join(messages)
    server.sendmail(EMAIL_ADDRESS, 'jamesandrew7860@gmail.com', email_message)