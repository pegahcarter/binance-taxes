from operator import itemgetter
import pandas as pd
import datetime
import time
from exchange import tickers, fetch_price


df = pd.read_excel('../data/transactions.xlsx')
df.rename(columns={'Date(UTC)':'date', 'Fee Coin':'fee_coin', 'Market':'ticker'}, inplace=True)
df.columns = [col.lower() for col in df.columns]

df['date'].apply(lambda x: time.mktime(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').timetuple()))
df = df.sort_values(by='date').reset_index(drop=True)
df['ticker'] = map(lambda x: tickers[x], df['ticker'])

# For now, we'll assume fetch_ohlcv perfectly pulls the price information at that timestamp.
# Add a btc_price to every transaction for conversion

df['numerator'] = None
df['denominator'] = None
df['numerator_price'] = None
df['denominator_price'] = None
df['fee_coin_price'] = None
df.loc[:, ['numerator', 'denominator']] = map(lambda x: x.split('/'), df['ticker'])

for i, date in enumerate(df['date'].unique()):
    if i % 100 == 0:
        print(i/df['date'].nunique())
    numerator, denominator, fee_coin, price = df.loc[i, ['numerator', 'denominator', 'fee_coin', 'price']]
    # pull btc price
    btc_price = fetch_price('BTC/USDT', date)
    # pull price data for numerator and denominator
    if denominator == 'BTC':
        denominator_price = btc_price
    else:
        denominator_price = btc_price * fetch_price(denominator + '/BTC', date)
    numerator_price = denominator_price * price
    # pull fee coin price
    if fee_coin == 'BTC':
        fee_coin_price = btc_price
    elif fee_coin == numerator:
        fee_coin_price = numerator_price
    elif fee_coin == denominator:
        fee_coin_price = denominator_price
    else:
        fee_coin_price = btc_price * fetch_price(fee_coin + '/BTC', date)

    df.loc[
        df['date'] == date,
        ['btc_price', 'denominator_price', 'numerator_price', 'fee_coin_price'
    ]] = btc_price, denominator_price, numerator_price, fee_coin_price


df.to_excel('../data/transactions_clean.xlsx', drop_index=True)
