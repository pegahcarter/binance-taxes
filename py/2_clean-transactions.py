from operator import itemgetter
import pandas as pd
from datetime import datetime
import ccxt

binance = ccxt.binance()
df = pd.read_excel('../data/transactions.xlsx')

df.rename(columns={'Date(UTC)':'date', 'Fee Coin':'fee_coin', 'Market':'ratio'}, inplace=True)
df.columns = [col.lower() for col in df.columns]

df['date'] = [int(datetime.timestamp(datetime.strptime(day, '%Y-%m-%d %H:%M:%S')) * 1000)
              for day in df['date']]

new_ratio = []
for ratio in df['ratio']:
    if len(ratio) == 6:
        new_ratio.append(ratio[:3] + '/' + ratio[3:])
    else:
        new_ratio.append('/'.join(ratio.partition('NANO')[1:]))

df['ratio'] = new_ratio

# For now, we'll assume fetch_ohlcv perfectly pulls the price information at that timestamp.
# Add a btc_price to every transaction for conversion

# First of all- make sure our transactions are in the correct order (I know this from experience)
df = df.sort_values(by='date').reset_index(drop=True)


bitfinex = ccxt.bitfinex()
df['btc_price'] = None

bitfinex.fetch_ohlcv(symbol='BTC/USDT', since=df['date'][0], limit=1)[0][2]

df.head()

for i, date in enumerate(df['date']):
    # pull price data for btc, numerator, and denominator
    [btc_data] = bitfinex.fetch_ohlcv(symbol='BTC/USDT', since=date, limit=1)
    numerator, denominator = df['ratio'][i].split('/')
    df.loc[df['date'] == date, 'btc_price'] = btc_data[2] # NOTE: we are using the "close" OHLCV parameter





# date = df['date'][0]
# date1 = df['date'][1]
# date2 = df['date'][2]

# trade = binance.fetch_ohlcv(symbol="BTC/USDT", limit=1, since=date)
# trade1 = binance.fetch_ohlcv(symbol="BTC/USDT", limit=1, since=date1)
# trade2 = binance.fetch_ohlcv(symbol="BTC/USDT", limit=1, since=date2)

# order = binance.fetch_ohlcv(symbol="BTC/USDT", limit=1, since=date)[0][0]
# order1 = binance.fetch_ohlcv(symbol="BTC/USDT", limit=1, since=date1)[0][0]
# order2 = binance.fetch_ohlcv(symbol="BTC/USDT", limit=1, since=date2)[0][0]

# NOTE: the values below are in milliseconds.
# date - order
# date1 - order1
# date2 - order2
