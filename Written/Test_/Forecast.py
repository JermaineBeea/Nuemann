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
import itertools
np.set_printoptions(threshold=np.inf)
pd.set_option('display.max_seq_items', 1000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

from Defined_.Forecast_Functions import rangeincrement
from Defined_.Distribution import blitz_distr, distribution
from Read_csv import readcsv
from Defined_.Math import Array_diffFunc, difference, random_func
from Defined_.Filtering import filterfunc,filterfunc2

start = tm.perf_counter()

interval = 1
raw_data = readcsv(r'C:\Users\User\OneDrive\Programming\Python\Written\Data\Trade\EURGBP.ifx_M2_0205_0207.csv')
comp_data = readcsv(r'C:\Users\User\OneDrive\Programming\Python\Written\Data\Trade\EURGBP.ifx_M3_0205_0207-0208.csv')

data = raw_data
comparison = comp_data

from_ = len(data)
initial = data[-1]

Incremental_Analysis = True
set_range = True
static_change = True
generated_prob = True; setvalue = 0.5
append_ = False
condition = True

deviationtype = 1
spread = 0.00015
poscondition = initial + spread
negcondition = initial - spread

iterations = int(len(data))
numForecasts = 20
Forecasts = []; arr_forecastmax = []; arr_forecastmin = []

if Incremental_Analysis:
  index_increment = 1
  min_data = np.min(data)
  increment_type = 'max'; units = 10**0
  range_increment = rangeincrement(data, increment_type, deviationtype) 

else: # Net Analysis on whole data set
  poschange, negchange, posprob = difference(data, 1, -1, 'pos')
  posprob = posprob if generated_prob else setvalue
  if static_change:
    posval =  blitz_distr(poschange, deviationtype, 'tend')[0]
    negval =  blitz_distr(negchange, deviationtype, 'tend')[0]
  else:
      posrange =  blitz_distr(poschange, deviationtype, 'distr range')[0]
      negrange =  blitz_distr(negchange, deviationtype, 'distr range')[0]

poscounter = 0; negcounter = 0
# region Forecast generation
for index in range(numForecasts + 1):
  if index > 0:
    Forecasts.append(forecastvalues)
    arr_forecastmax.append(max(forecastvalues))
    arr_forecastmin.append(min(forecastvalues))
  
  data = raw_data
  evaluate = data[-1]
  forecastvalues = [data[-1]]
  
  if index == numForecasts:
     break
    
  for iter in range(iterations):

    if Incremental_Analysis:
      if append_ and iter > 0: 
        data.append(evaluate)
      
      if set_range:
          set_increment = range_increment*units
          z = set_increment
          n = np.floor((evaluate - min_data)/z)
          minimum = min_data + z*(n - 1)
          maximum = min_data + z*(n + 1)
      else:
          minimum = evaluate - range_increment*units
          maximum = evaluate + range_increment*units

      filterdata = filterfunc(data, index_increment, minimum, maximum)
      if not filterdata:  # if filterdata is empty
          print(f'iteationr {index} is empty')
          continue  # skip to the next iteration
      poschange, negchange, posprob = Array_diffFunc(filterdata, 1, -1, 'pos')

      if poschange == []: poschange = [0]
      if negchange == []: negchange = [0]

      posprob = posprob if generated_prob else setvalue

      if static_change:
          posval =  blitz_distr(poschange, deviationtype, 'tend')[0]
          negval =  blitz_distr(negchange, deviationtype, 'tend')[0]
      else:
        posrange =  blitz_distr(poschange, deviationtype, 'distr range')[0]
        posval = random.uniform(*posrange)
        negrange =  blitz_distr(negchange, deviationtype, 'distr range')[0]
        negval = random.uniform(*negrange)   

    elif Incremental_Analysis is False and static_change is False:
          posval = random.uniform(*posrange)
          negval = random.uniform(*negrange)

    if condition:
        poscounter = poscounter + 1 if evaluate > poscondition else poscounter
        negcounter = negcounter + 1 if evaluate < negcondition else negcounter

    evaluate += random_func(posprob, posval, negval)
    forecastvalues.append(evaluate)

# endregion Forecast generation

analyse_Forecast_distr = 1
if analyse_Forecast_distr:
  Frame = pd.DataFrame(Forecasts)
  Forecast_distr = distribution(np.concatenate(Frame.values), 1, 'conc range')

  Time_distr = Frame.apply(blitz_distr, args = (1, 'conc range'), axis = 0)
  max = enumerate(Time_distr.max())
  min = enumerate(Time_distr.min())
  indexmax = [(index, maxval) for index,maxval in max if maxval == Time_distr.max().max()]
  indexmin = [(index, minval) for index,minval in min if minval == Time_distr.min().min()]

Buyprofit_prob = np.floor((poscounter/(iterations*numForecasts))*100)
Sellprofit_prob = np.floor((negcounter/(iterations*numForecasts))*100)
Profit_prob = Buyprofit_prob + Sellprofit_prob
Loss_prob= 100 - Profit_prob

Buy_Forecastmax_factor = Forecast_distr[1]/(evaluate + spread) - 1
Buy_Movingmax_factor = indexmax[0][1]/(evaluate + spread) - 1
Sell_Forecastmin_factor = evaluate/(Forecast_distr[0] + spread) - 1
Buy_Movingmin_factor = evaluate/(indexmin[0][1] + spread) - 1

total = tm.perf_counter() - start

Text_libr = {
  2: f'({numForecasts} Forecasts: sub-iterations {iterations}: data size {len(data)} Total time {total})',
  3: f'Spread {spread} Profit ({Profit_prob}%):Loss ({Loss_prob}%), Buy ({Buyprofit_prob}%):Sell ({Sellprofit_prob}%)',
  4: f'Pos profit factors (Moving max: {Buy_Movingmax_factor}, Forecast max: {Buy_Forecastmax_factor})',
  5: f'Neg profit factors (Moving min: {Buy_Movingmin_factor}, Forecast min: {Sell_Forecastmin_factor})'
}
if Incremental_Analysis:
  Text_libr[1] = f'(Forecast with {increment_type} {range_increment*units}({range_increment}:{units}), {len(data)*iterations*numForecasts} iterations'
else:
  Text_libr[1] = f'Forecasts {iterations*numForecasts} iterations'

print('\n'.join([Text_libr[key] for key in Text_libr.keys()]))
print(f'Execution time: {total}')

# region plot
plot = 1
if plot:
  plt.title('\n'.join([Text_libr[key] for key in Text_libr.keys()]))
  from_ = len(data)
  color1 = 'red'; color2 = 'black'; color3 = 'blue'; color4 = 'blue'

  #Forecasts
  plot_forecast = False
  if plot_forecast:
    for line in Forecasts:
      plt.plot(range(from_, from_ + len(line)), line ,color = 'grey', linewidth = 0.6, alpha = 0.4)

  #Forecasts distribution
  style = '-'; width = 0.5; transperency = 0.6

  if analyse_Forecast_distr:
    plt.plot(range(from_, from_ + len(Time_distr.T)), Time_distr.T, color = color4, linestyle = style, linewidth = width, alpha = transperency)
  
  #Original data and comparisom
  plt.plot(data, color = 'orange', linestyle = style, linewidth = 0.8, alpha = 1)
  plt.plot(range(from_, from_ + len(comparison)),comparison, color = 'black', linestyle = style, linewidth = width, alpha = transperency)

  #Plot Horizontal and Verical lines

  #Plot Horizontal lines
  style = '--'
  width = 1; transperency = 1

  plt.plot([from_, from_ + iterations], [evaluate, evaluate], color = 'orange', linestyle = style, linewidth = width, alpha = transperency)

  Hline_libr = {
    poscondition: (color1,'Buy profit Factor'),
    negcondition: (color1,'Sell profit Factor'),
    }
  if analyse_Forecast_distr:
    Hline_libr[Forecast_distr[1]] = (color2,'Forecasts distr Max')
    Hline_libr[Forecast_distr[0]] = (color2,'Forecasts distr Min') 
    Hline_libr[indexmax[0][1]] = (color3,'Moving distr Max')
    Hline_libr[indexmin[0][1]] = (color3,'Moving distr Min')

  for Hline in Hline_libr.keys():
    plt.axhline(y=Hline, color=Hline_libr[Hline][0], linestyle=style, linewidth=width, label = f'{Hline_libr[Hline][1]}: {Hline}', alpha = transperency)

  #Plot Vertical lines
  if analyse_Forecast_distr:
    style = '-'; width = 0.6; transperency = 0.5

    Xline_libr = {
      indexmin[0][0]: ('black','Movng distr Time min'), 
      indexmax[0][0]: ('black','Movng distr Time max')
    }
    for Xline in Xline_libr.keys():
      plt.axvline(x = from_ + Xline, color=Xline_libr[Xline][0], linestyle=style, linewidth=width, label = f'{Xline_libr[Xline][1]}: {Xline}', alpha = transperency)

  plt.legend()
  plt.show()



