import ccxt

binance = ccxt.binance()

def fetch_price(ticker, date):
    # NOTE: we are using the "close" OHLCV parameter
    return binance.fetch_ohlcv(symbol=ticker, since=int(date), limit=1)[0][2]
