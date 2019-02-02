# Cleaning
import pandas as pd
from datetime import datetime

for file in ['withdrawals', 'deposits']:
    df = pd.read_csv('../data/' + file + '.csv')
    df.dropna(inplace=True)

    # Re-order dataframe from oldest to newest
    df = df[::-1]

    # Convert to datetime
    df['Date'] = [datetime.strptime(day, '%Y-%m-%d %H:%M:%S') for day in df['Date']]

    df.to_csv('../data/' + file + '.csv')
