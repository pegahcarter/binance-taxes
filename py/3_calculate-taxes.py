import pandas as pd
import ccxt

# Order
# 1. loop through the df by rows
# 2. For each row:
#       - pull BTC price of that time
#       - Find the price of the numerator & denominator using BTC (make exception if one is BTC)
#       - Use `fee_coin` to determine which coin to reduce quantity of (trading fee)
#       - Also multiply trade fee by BTC price to get $ price of trade fee

Transactions = pd.DataFrame(columns=[
                    'date', 'coin', 'side', 'units', 'pricePerUnit', 'fees',
                    'previousUnits', 'cumulativeUnits', 'transactedValue',
                    'previousCost', 'costOfTransaction', 'costOfTransactionPerUnit',
                    'cumulativeCost', 'gainLoss', 'realisedPct'])

binance = ccxt.binance()
for date, ratio, type, price, amount, total, btc_fee, fee_coin in df.values:
    btc_data = binance.fetch_ohlcv(symbol='BTC/USDT', since=date, limit=1)
    btc_price = next(iter(btc_data)) [0]

    for coin in ratio.split('/'):
        if coin = 'BTC':
            coin_price = btc_price
        else:
            coin_price = btc_price * binance.fetch_ohlcv(symbol=coin, since=date, limit=1)

        if coin in Transactions['coin']:
            transactions.update()
        else:
            transactions.addCoin(coin=coin, coinUnits=???, date=date, currentPrice=coin_price)


transactions.update(ratio.split('/'))
