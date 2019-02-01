import pandas as pd
import numpy as np
from datetime import datetime
import ccxt

# -------------------------------------------------------------------------
# Testing
market = exchange.load_markets()
tickers = list(market.keys())

coins = set()
[[coins.add(coin) for coin in ticker.split('/') if coin != 'BTC'] for ticker in tickers]
coins = list(coins)

# Since we can't pull BTC/BTC, use BTC/USDT ticker.  Otherwise, use coin/BTC as ticker
tickers = [coin + '/BTC' for coin in coins]

# -------------------------------------------------------------------------
exchange = ccxt.binance()
def btc_price(coin, date):
    if coin == 'BTC':
        return 1.0/exchange.fetch_ohlcv(symbol=coin + '/BTC', since=date, limit=1)[0][2]
    else:
        return exchange.fetch_ohlcv(symbol=coin + '/BTC', since=date, limit=1)[0][2]


def addCoin(coin, coinUnits, date=None, currentPrice=None):
    ''' Add initial purchase of coin to transactions table '''

    if date is None:
        date = datetime.now()
        currentPrice = exchange.fetch_price(coin)


    df = pd.read_csv(TRANSACTIONS_FILE)
    df = df.append({'date': date,
                    'coin': coin,
                    'side': 'buy',
                    'units': coinUnits,
                    'pricePerUnit': currentPrice,
                    'fees': currentPrice * coinUnits * 0.00075,
                    'previousUnits': 0,
                    'cumulativeUnits': coinUnits,
                    'transactedValue': currentPrice * coinUnits,
                    'previousCost': 0,
                    'cumulativeCost': currentPrice * coinUnits,
                    'gainLoss': 0}, ignore_index=True)

    return df.to_csv(TRANSACTIONS_FILE, index=False)


def update(coins, sides, coinUnits, d_amt, date=None, currentPrice=None):
    '''
    Document transaction data to CSV
    coin            - coin we're documenting for the trade
    side            - side we're executing the trade on (buy or sell)
    coinUnits       - units of coin to be traded
    d_amt           - value of our trade in dollars
    df              - transactions dataframe
    '''
    df = pd.read_csv(TRANSACTIONS_FILE)
    for coin, tradeSide, tradeUnits in zip(coins, sides, coinUnits):

        previousUnits = df[df['coin'] == coin]['cumulativeUnits'].iloc[-1]
        previousCost = df[df['coin'] == coin]['cumulativeCost'].iloc[-1]
        # previousUnits, previousCost = df[df['coin'] == coin][['cumulativeUnits','cumulativeCost']].iloc[-1]

        if date is None:
            date = datetime.now()
            currentPrice = exchange.fetch_price(coin)

        if tradeSide == 'buy':
            fees = d_amt * 0.00075
            cumulativeUnits = previousUnits + tradeUnits
            costOfTransactionPerUnit = None
            costOfTransaction = None
            cumulativeCost = previousCost + d_amt
            gainLoss = None
            realisedPct = None
        else:
            fees = None
            cumulativeUnits = previousUnits - tradeUnits
            costOfTransactionPerUnit = previousCost / previousUnits
            costOfTransaction = tradeUnits / previousUnits * previousCost
            cumulativeCost = previousCost - d_amt
            gainLoss = d_amt - costOfTransaction
            realisedPct = gainLoss / costOfTransaction

        df = df.append({'date': date,
                        'coin': coin,
                        'side': tradeSide,
                        'units': tradeUnits,
                        'pricePerUnit': currentPrice,
                        'fees': fees,
                        'previousUnits': previousUnits,
                        'cumulativeUnits': cumulativeUnits,
                        'transactedValue': currentPrice * tradeUnits,
                        'previousCost': previousCost,
                        'costOfTransaction':  costOfTransaction,
                        'costOfTransactionPerUnit': costOfTransactionPerUnit,
                        'cumulativeCost': cumulativeCost,
                        'gainLoss': gainLoss,
                        'realisedPct': realisedPct}, ignore_index=True)

    return df.to_csv(TRANSACTIONS_FILE, index=False)
