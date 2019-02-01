import os
import sys
import pandas as pd
import numpy as np
import ccxt
from functions import btc_price



with open('../../../Administrative/api.txt', 'r') as f:
    api = f.readlines()
    apiKey = api[0][:-1]
    secret = api[1]

binance = ccxt.binance({'options': {'adjustForTimeDifference': True},
                         'apiKey': apiKey,
                         'secret': secret})

deposits = binance.fetch_deposits()
withdrawals = binance.fetch_withdrawals()
binance.account()


for deposit in deposits:

    date = deposit['timestamp']
    ticker = deposit['currency']
    actionType = 'DEPOSIT'
    price = btc_price(ticker, date)
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
