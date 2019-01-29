import os
import sys
import pandas as pd
import numpy as np
import ccxt
import pprint

with open('../../../administrative/ethereum/api.txt', 'r') as f:
    api = f.readlines()
    apiKey = api[0][:-1]
    secret = api[1][:-1]

binance = ccxt.binance({'apiKey': apiKey, 'secret': secret})

deposits = binance.fetch_deposits()
withdrawals = binance.fetch_withdrawals()

df = pd.DataFrame(columns=['date', 'ratio', 'type', 'price', 'amount', 'total', 'address', 'txId'])

for deposit in deposits:

    date = deposit['timestamp']
    ratio = deposit['currency'] + '/BTC' #TODO: BTC deposits will not work
    actionType = 'DEPOSIT'
    price = binance.fetch_ohlcv(symbol=ratio, since=date, limit=1)[0][2]
    amount = deposit['amount']
    address = deposit['address']
    txId = deposit['txid']

    # TODO: this will not work BTC deposits
    df.append([date, ratio, actionType, price, amount, price * amount, address, txId])

test = deposits[0]




deposits

'''
- Enough data to count it as a "buy"
- Merge deposits into transactions as buys
    > Only difference from a trade is there is no "sell" side
'''
