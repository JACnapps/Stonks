import sqlite3

#create new database for stock and stock price
connection = sqlite3.connect('stonks.db')
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL,
        exchange TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_price (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        date NOT NULL,
        open NOT NULL, 
        high NOT NULL, 
        low NOT NULL, 
        close NOT NULL, 
        volume NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_patterns (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        date NOT NULL,
        hammer NOT NULL, 
        ihammer NOT NULL, 
        three_white_soldiers NOT NULL,
        morning_star NOT NULL, 
        engulfing NOT NULL, 
        hangingman NOT NULL, 
        shooting_star NOT NULL, 
        evening_star NOT NULL, 
        three_black_crows NOT NULL, 
        dark_cloud_cover NOT NULL, 
        doji NOT NULL, 
        spinning_top NOT NULL, 
        three_methods NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
        )
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_review (
        id INTEGER PRIMARY KEY,
        stock_id INTEGER,
        date NOT NULL,
        macd_a, 
        macd_a_signal,
        macd_a_histogram, 
        macd_b, 
        macd_b_signal, 
        macd_b_histogram,
		psar,
		rsi_14,
		adx,
		plus_di,
        minus_di,
		cmo_s,
		cmo_p,		
        FOREIGN KEY (stock_id) REFERENCES stock (id)
        )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS strategies (
        id INTEGER PRIMARY KEY, 
        name TEXT NOT NULL
        )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_strategies (
        stock_id INTEGER PRIMARY KEY, 
        strategy_id TEXT NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id),
        FOREIGN KEY (strategy_id) REFERENCES strategies (id)
        )
""")

cursor.execute("""
    INSERT INTO strategies(name) VALUES('opening_range_breakout')
""")

#cursor.execute("""
 #   INSERT INTO stock_strategy(stock_id, strategy_id) VALUES(1988,1), (7458,1)
  #  """)
connection.commit()