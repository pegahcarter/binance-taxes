from operator import itemgetter
import pandas as pd
import datetime
import time
import ccxt

binance = ccxt.binance()
df = pd.read_excel('/home/carl/Documents/main/legal/taxes/crypto/2018/binance/transactions.xlsx')

df.rename(columns={'Date(UTC)':'date', 'Fee Coin':'fee_coin', 'Market':'ticker'}, inplace=True)
df.columns = [col.lower() for col in df.columns]

df['date'] = map(lambda x: time.mktime(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').timetuple()), df['date'])
df['date'] *= 1000


new_ratio = []
for ratio in df['ticker']:
    if len(ratio) == 6:
        new_ratio.append(ratio[:3] + '/' + ratio[3:])
    else:
        new_ratio.append('/'.join(ratio.partition('NANO')[1:]))

df['ticker'] = new_ratio

# For now, we'll assume fetch_ohlcv perfectly pulls the price information at that timestamp.
# Add a btc_price to every transaction for conversion

# First of all- make sure our transactions are in the correct order (I know this from experience)
df = df.sort_values(by='date').reset_index(drop=True)

for i, date in enumerate(df['date'].unique()):
    # pull price data for btc, numerator, and denominator
    [btc_data] = binance.fetch_ohlcv(symbol='BTC/USDT', since=int(date), limit=1)
    numerator, denominator = df['ticker'][i].split('/')
    df.loc[df['date'] == date, 'btc_price'] = btc_data[2] # NOTE: we are using the "close" OHLCV parameter

df.to_csv('../data/transactions.csv')


'''
To-do
- get price of fee coin
- get price of numerator
- get price of denominator
    > if it's BTC, we can use btc_price for both sides
        > numerator price = price * btc_price
        > denominator price = btc_price
    > if it's not BTC
        > denominator price = denominator/BTC * btc_price
        > numerator price = denominator * price

'''

#
# df['numerator'] = None
# df['denominator'] = None
# df.loc[:, ['numerator', 'denominator']] = map(lambda x: x.split('/'), df['ticker'])
# df.head()
