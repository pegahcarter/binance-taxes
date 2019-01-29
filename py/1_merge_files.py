import os
import sys
import pandas as pd
import numpy as np
import ccxt
import functions


with open('../../../administrative/ethereum/api.txt', 'r') as f:
    api = f.readlines()
    apiKey = api[0][:-1]
    secret = api[1][:-1]

binance = ccxt.binance({'apiKey': apiKey, 'secret': secret})

deposits = binance.fetch_deposits()
withdrawals = binance.fetch_withdrawals()

df = pd.DataFrame(columns=['date', 'ticker', 'type', 'price', 'amount', 'total', 'address', 'txId'])

df = []
for deposit in deposits:

    date = deposit['timestamp']
    ticker = deposit['currency']
    actionType = 'DEPOSIT'
    price = binance.fetch_ohlcv(symbol=ticker + '/BTC', since=date, limit=1)[0][2] # TODO: this will not work w/ BTC deposits
    amount = deposit['amount']
    address = deposit['address']
    txId = deposit['txid']

    df.append({'date': date,
               'ticker': ticker,
               'type': actionType,
               'price': price,
               'amount': amount,
               'total': price * amount,
               'address': address,
               'txId': txId})


pd.DataFrame(data=df)


'''
- Enough data to count it as a "buy"
- Merge deposits into transactions as buys
    > Only difference from a trade is there is no "sell" side
'''
