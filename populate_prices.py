#These are required
from config import *
import sqlite3, tulipy, numpy
import alpaca_trade_api as tradeapi

connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

#Pulls list of stocks in database
cursor.execute("""
    SELECT id, symbol, name FROM stock
""")
rows = cursor.fetchall()

#generates a list of symbols sotred in the stock database for use in the price database
symbols = []
stock_dict ={}

for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

print(stock_dict)
#print(stock_dict["AAPL"])
    #print(symbols)
#TEMP MEANS OF TESTING TO REPLACE LIST OF SYMBOLS FROM ABOVE
#symbols = ['MSFT','NIO','GD','WPC','LMT','C','BAC','INTC','ACB','UBER','STT','BIDU','ALB','WMT','BABA','AAL','CVS','TEVA','XOM','GM','T','GE','GME','AMC','EZGO']

#alpaca asset call and set limit to 200
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)
chunk_size = 200

#pulls a X years of trading data for each stock in symbols. 
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size]
    #print(symbol_chunk)
    #barsets = api.get_barset(symbol_chunk, 'day', after=date.today().isoformat())
    barsets = api.get_barset(symbol_chunk, 'day')
    
    for symbol in barsets:
        #print(symbol)
        #print(symbol[0])
        #print(barsets)
        print(f"Processing symbol {symbol}")
        recent_closes = []
        recent_highs = []
        recent_lows = []
        recent_volume = []
        

        #inserts barset information into sql
        for bar in barsets[symbol]:
            
            #print(stock_dict[symbol])
            stock_id = stock_dict[symbol]
            recent_closes.append(bar.c)
            recent_highs.append(bar.h)
            recent_lows.append(bar.l)
            recent_volume.append(bar.v)
            
            if len(recent_closes) >= 50: 
                #MACD 26/12
                (macd_a, macd_a_signal, macd_a_histogram) = tulipy.macd(numpy.array(recent_closes), short_period=12,  long_period=26, signal_period=9)
                macd_a = macd_a[-1]
                macd_a_signal = macd_a_signal[-1]
                macd_a_histogram = macd_a_histogram[-1]

                #MACD 50/20
                (macd_b, macd_b_signal, macd_b_histogram) = tulipy.macd(numpy.array(recent_closes), short_period=20,  long_period=50, signal_period=9)
                macd_b = macd_b[-1]
                macd_b_signal = macd_b_signal[-1]
                macd_b_histogram = macd_b_histogram[-1]
                
                #Parabolic SAR
                psar = tulipy.psar(numpy.array(recent_highs), numpy.array(recent_lows), .2, 2)[-1]
                
                #RSI
                rsi_14 = tulipy.rsi(numpy.array(recent_closes), period=14)[-1]

                #ADX
                adx = tulipy.adx(numpy.array(recent_highs),numpy.array(recent_lows), numpy.array(recent_closes), 5)[-1] 
                #adxr = tulipy.adxr(numpy.array(recent_highs),numpy.array(recent_lows), numpy.array(recent_closes), 5)[-1] 
                (plus_di, minus_di) = tulipy.di(numpy.array(recent_highs), numpy.array(recent_lows), numpy.array(recent_closes), 5)
                plus_di = plus_di[-1]
                minus_di = minus_di[-1]

                #CMO
                cmo_s = tulipy.cmo(numpy.array(recent_closes), period=9)[-1]
                cmo_p = tulipy.cmo(numpy.array(recent_closes), period=20)[-1] 
                
                #OBV
                #obv = tulipy.obv(numpy.array(recent_closes), numpy.array(recent_volume))[-1]
            else:
                macd_a, macd_a_signal, macd_a_histogram, macd_b, macd_b_signal, macd_b_histogram, psar, rsi_14, adx, plus_di, minus_di, cmo_s, cmo_p = None, None, None, None, None, None, None, None, None, None, None, None, None

            cursor.execute("""
                INSERT INTO stock_price (stock_id, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))
            cursor.execute("""
                INSERT INTO stock_review (stock_id, date, macd_a, macd_a_signal, macd_a_histogram, macd_b, macd_b_signal, macd_b_histogram, psar, rsi_14, adx, plus_di, minus_di, cmo_s, cmo_p)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (stock_id, bar.t.date(), macd_a, macd_a_signal, macd_a_histogram, macd_b, macd_b_signal, macd_b_histogram, psar, rsi_14, adx, plus_di, minus_di, cmo_s, cmo_p))
connection.commit()