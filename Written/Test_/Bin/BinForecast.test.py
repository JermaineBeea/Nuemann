import sys
sys.path.append("..")
sys.path.insert(0, 'C:/Users/tebne/OneDrive/Programming/Written/')

import numpy as np
import pandas as pd
import IPython.display as ds
import random as random
import time as tm 
import timeit as tim
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

from Defined_.Forecast_Functions import rangeincrement
from Defined_.Distribution import distribution
from Read_csv import readcsv
from Defined_.Math import difference, random_func
from Defined_.Filtering import filterfunc

interval = '1 min: 1 day'
raw_data = readcsv(r'c:\Users\tebne\OneDrive\Documents\C-EURUSD.ifx_M1_0205.csv')
comp_data = readcsv(r'c:\Users\tebne\OneDrive\Documents\C-EURUSD.ifx_M1_0205.csv')
comp_data = []

data = raw_data
comparison = comp_data

from_ = len(data)
initial = data[-1]

set_range = False
static = True
setprob = False
append_ = False
condition = False

setvalue = 0.5
index_increment = 1
spread = 0.00013
profit = 0; 
invest = 10000; 

poscondition = ((profit/(invest)) + 1)*(initial + spread)
negcondition = (initial/((profit/(invest)) + 1)) - spread

evaluate = initial
forecastvalues = [initial]
iterations = int(len(data))
deviationtype = 1
numForecasts = 1000

poscounter = 0; negcounter = 0
Forecasts = []; arr_forecastmax = []; arr_forecastmin = []

min_data = np.min(data)
increment_type = 'mean'; units = 1
range_increment = rangeincrement(data, increment_type, deviationtype, units_input = units) 

counter = 1
start = tm.perf_counter()
for index in range(numForecasts*iterations):
  
  if counter == iterations:
    counter = 1
    arr_forecastmax.append(max(forecastvalues))
    arr_forecastmin.append(min(forecastvalues))
    Forecasts.append(forecastvalues)
    data = readcsv(r'c:\Users\tebne\OneDrive\Documents\C-EURUSD.ifx_M1_0205.csv')
    evaluate = initial
    forecastvalues = [initial]
  else: counter = counter + 1
      
  if index == numForecasts*iterations:
    break
  
  if append_: 
    data.append(evaluate)

  if set_range:
      set_increment = range_increment
      z = set_increment
      n = (evaluate - min_data)/z
      minimum = min_data + z*(n - 1)
      maximum = min_data + z*(n + 1)
  else:
      minimum = evaluate - range_increment
      maximum = evaluate + range_increment

  filterdata = filterfunc(data, index_increment, minimum, maximum)
  if not filterdata:  # if filterdata is empty
      print(f'iter {index} is empty')
      continue  # skip to the next iteration
  poschange, negchange, posprob = difference(filterdata, 1, -1, 'pos')
  if poschange == []: poschange = [0]
  if negchange == []: negchange = [0]

  posprob = setvalue if setprob else posprob

  if static:
      posval =  distribution(poschange, deviationtype, 'tend')[0]
      negval =  distribution(negchange, deviationtype, 'tend')[0]
  else:
      posrange =  distribution(poschange, deviationtype, 'distr range')[0]
      posval = random.uniform(*posrange)
      negrange =  distribution(negchange, deviationtype, 'distr range')[0]
      negval = random.uniform(*negrange)

  if condition:
      poscounter = poscounter + 1 if evaluate > poscondition else poscounter
      negcounter = negcounter + 1 if evaluate < negcondition else negcounter
  
  evaluate += random_func(posprob, posval, negval)
  forecastvalues.append(evaluate)

total = tm.perf_counter() - start
print(f'direct {total}')

for line in Forecasts:
   plt.plot(line, linewidth = 0.6)
plt.show()