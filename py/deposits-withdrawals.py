# Cleaning/merging deposits and withdrawals
import pandas as pd
from datetime import datetime

for file in ['withdrawals', 'deposits']:
    df = pd.read_csv('../data/' + file + '.csv')
    df.dropna(inplace=True)

    # Re-order dataframe from oldest to newest
    df = df[::-1]

    # Convert to datetime
    df['Date'] = [datetime.strptime(day, '%Y-%m-%d %H:%M:%S') for day in df['Date']]

    if file == 'withdrawals':
        df['Type'] = 'WITHDRAWAL'
    else:
        df['Type'] = 'DEPOSIT'

    df.to_csv('../data/' + file + '.csv', index=False)

d = pd.read_csv('../data/deposits.csv')
w = pd.read_csv('../data/withdrawals.csv')
dw = pd.merge(d, w, how='outer')
dw.to_csv('../data/deposits-withdrawals.csv', index=False)
