import sys
sys.path.append("..")
sys.path.insert(0, 'C:/Users/tebne/OneDrive/Programming/Written/')

import numpy as np
import pandas as pd
import IPython.display as ds
import random as random
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

from Defined_.Forecast import forecast
from Defined_.Forecast import rangeincrement
from Defined_.Distribution import distribution
from Test_.Data import*


arrays = [data1, data2, data3, data4, data5]
dataAnalysed = []
choices = 1,2,3
for choice in [*choices]:
  dataAnalysed += arrays[choice -1]

data = dataAnalysed
comparison = arrays[choices[-1]]

from_ = len(data)
evaluate = data[-1]
print(f'Evaulauted from {evaluate}')

deviationtype = 2
index_increment = 1 
increment_type = 'max'
range_increment = rangeincrement(data, increment_type, deviationtype)
iterations = len(comparison)

Forecasts = []
numForecasts = 20
for index in range(numForecasts):
  forecastvalues = forecast(data, evaluate, iterations, index_increment, deviationtype, range_increment)
  Forecasts.append(forecastvalues)

Frame = pd.DataFrame(Forecasts)
tend_distr = Frame.apply(distribution, args=(1,'conc distr'), axis= 0)
tendency = tend_distr.T[1]
maxtend_distr = tend_distr[2]
mintend_distr = tend_distr[0]
maxtend = max(tendency)
mintend = min(tendency)
# tend_distr = [array[0] for array in tend_distr]
ds.display(tend_distr)

print(f'R increment is {increment_type}, with value {range_increment}')
print(f'Forecast iterations are {iterations*numForecasts}, with {iterations} iterations per forecast')

plot = 1
if plot:
  plt.title(f'Forecast Graph \nR increment is {increment_type}, with value {range_increment}')

  # X ranges
  datarange = range(len(data))
  comparisonrange = range(len(data) + 1, len(data) + len(comparison) + 1)
  x_range_forecast = range(from_, from_ + len(forecastvalues))

  #Plot comparison, Forecast and data
  plt.plot(comparisonrange, comparison, label = 'Comparison', color = 'blue')
  
  plot_forecast = False
  if plot_forecast:
    for index in range(numForecasts):
      plt.plot(x_range_forecast, Forecasts[index],color='grey', linewidth=0.5)

  plt.plot(datarange, data, label= 'Data', color = 'orange')
  plt.plot(x_range_forecast,tendency, color = 'green', linewidth = 0.3)

  plt.axhline(y= maxtend, color='black', linestyle='--', label = f'max {maxtend}')
  plt.axhline(y = mintend, color = 'black', linestyle = '--', label = f'min {mintend}')
  # plt.axhline(from_, y = evaluate ,color = 'red', linestyle = '--', label = f'Evaluate from: {evaluate}')
  plt.legend()
  plt.show()
 