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





# date = df['date'][0]
# trade = binance.fetch_ohlcv(symbol="BTC/USDT", limit=1, since=date)
# order = binance.fetch_ohlcv(symbol="BTC/USDT", limit=1, since=date)[0][0]
#
# date1 = df['date'][1]
# trade1 = binance.fetch_ohlcv(symbol="BTC/USDT", limit=1, since=date1)
# order1 = binance.fetch_ohlcv(symbol="BTC/USDT", limit=1, since=date1)[0][0]
#
# date2 = df['date'][2]
# trade2 = binance.fetch_ohlcv(symbol="BTC/USDT", limit=1, since=date2)
# order2 = binance.fetch_ohlcv(symbol="BTC/USDT", limit=1, since=date2)[0][0]
#
#
# df['date'][0] - order
# df['date'][1] - order1
# df['date'][2] - order2
