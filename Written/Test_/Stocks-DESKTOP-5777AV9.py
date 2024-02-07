import yfinance as finance
import pandas as pd
import time as tm
import json
pd.set_option('display.max_rows', None)

asset = "TSLA"

interval = 65
iterations = 3

price = finance.Ticker(asset).info.get('currentPrice')
price02 = finance.Ticker(asset).history()['Close'].iloc[-1]
# pricehist = finance.Ticker(asset).history().loc['2023-12-04':'2023-12-08']['Close']
pricehist = finance.Ticker(asset).history(start = '2024-01-26', end = '2024-01-27', interval= '1m')['Close'].to_list()  

# price = []
# for iter in range(iterations):
#   price.append(finance.Ticker(asset).info.get('currentPrice'))
#   tm.sleep(interval)

dump = 1
if dump:
  with open('Tsla.py', 'a') as file:
    json.dump(pricehist, file)




