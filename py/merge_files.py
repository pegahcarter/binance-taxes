import os
import sys
import pandas as pd
import numpy as np
import ccxt
import pprint

DEPOSITS_FILE = '../data/deposits.csv'
TRANSACTIONS_FILE = '../data/transactions.csv'
WITHDRAWALS_FILE = '../data/withdrawals.csv'


with open('../../../administrative/ethereum/api.txt', 'r') as f:
    api = f.readlines()
    apiKey = api[0][:-1]
    secret = api[1][:-1]

exchange = ccxt.binance({'options': {'adjustForTimeDifference': True},
                         'apiKey': apiKey,
                         'secret': secret})


# Deposits and their respective information
deposits = exchange.fetch_deposits()

amount = ['info']['amount']
addressTo = ['info']['address']
coin = ['info']['asset']
txId = ['txid']
date = ['timestamp']

'''
- Enough data to count it as a "buy"
- Merge deposits into transactions as buys
    > Only difference from a trade is there is no "sell" side
'''
