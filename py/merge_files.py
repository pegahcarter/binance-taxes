import os
import sys
import pandas as pd
import numpy as np

DEPOSITS_FILE = '../data/deposits.csv'
TRANSACTIONS_FILE = '../data/transactions.csv'
WITHDRAWALS_FILE = '../data/withdrawals.csv'

deposits = pd.read_csv(DEPOSITS_FILE)
transactions = pd.read_csv(TRANSACTIONS_FILE)
withdrawals = pd.read_csv(WITHDRAWALS_FILE)
