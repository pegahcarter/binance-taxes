import ccxt

binance = ccxt.binance()
ticks = binance.fetchTickers().keys()
tickers = {tick.replace('/', ''): tick for tick in ticks}

def fetch_price(ticker, date):
    # NOTE: we are using the "close" OHLCV parameter
    return binance.fetch_ohlcv(symbol=ticker, since=int(date*1000), limit=1)[0][2]
