from config import *
import sqlite3
import alpaca_trade_api as tradeapi

connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

#get a list to limit rewriting of db
cursor.execute("""
    SELECT symbol, name, exchange FROM stock
""")
rows = cursor.fetchall()

symbols = [row['symbol'] for row in rows] #list comprehension

#alpaca asset call
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
active_assets = api.list_assets(status='active')

nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ' and a.tradable]
amex_assets = [a for a in active_assets if a.exchange == 'AMEX']
nyse_assets = [a for a in active_assets if a.exchange == 'NYSE']
assets = nasdaq_assets + nyse_assets
 
#assets inserted that are new and not in symbols
for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"Added a new stock {asset.symbol} {asset.name} {asset.exchange}")
            cursor.execute("INSERT INTO stock (symbol, name, exchange) VALUES (?, ?, ?)", (asset.symbol, asset.name, asset.exchange))
    except Exception as e:
        print(asset.symbol)
        print(e)

#cursor.execute("""
#    DELETE FROM stock WHERE symbol LIKE '%.%' OR symbol LIKE '%-%'
# """)

#Dontwork = ['CAHC', 'GLSPU']
#cursor.execute("DELETE FROM stock WHERE symbol = 'CAHC'")
#cursor.execute("DELETE FROM stock WHERE symbol = 'GLSPU'")

connection.commit()