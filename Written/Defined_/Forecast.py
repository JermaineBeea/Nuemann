import sys
sys.path.append("..")
sys.path.insert(0, 'C:/Users/tebne/OneDrive/Programming/Written/')

from Defined_.Filtering import filterfunc
from Defined_.Distribution import distribution
from Defined_.Math import difference, random_func

import random as random
import numpy as np

def forecast(data, evaluate, iterations, index_increment, deviationtype, 
range_increment, **kwargs):
   
   static = kwargs.get('static', True)
   setprob = kwargs.get('setprob', False)
   setvalue = kwargs.get('setvalue', 0.5)
   
   forecastvalues = [evaluate]
   for iter in range(iterations):
      
      minimum = evaluate - range_increment
      maximum = evaluate + range_increment

      filterdata = filterfunc(data, index_increment, minimum, maximum)
      # print(f'Filter data of iteration {iter}: {filterdata}')
      if not filterdata:  # if filterdata is empty
         continue  # skip to the next iteration
      poschange, negchange, posprob = difference(filterdata, 1, -1, 'pos')
      if poschange == []: poschange = [0]
      if negchange == []: negchange = [0]

      setprob = False
      setvalue = 0.5
      posprob = setvalue if setprob else posprob

      static = True	
      if static:
         posval =  distribution(poschange, deviationtype, 'tend')[0]
         negval =  distribution(negchange, deviationtype, 'tend')[0]
      else:
         posrange =  distribution(poschange, deviationtype, 'distr range')[0]
         posval = random.uniform(*posrange)
         negrange =  distribution(negchange, deviationtype, 'distr range')[0]
         negval = random.uniform(*negrange)

      evaluate += random_func(posprob, posval, negval)
      forecastvalues.append(evaluate)
   return forecastvalues

def rangeincrement(data, increment_type, power_, **kwargs):
   """""
   data: data to be evaluated
   increment_type: type of increment
   power: power of deviation
   'default': default value of increment
   'dev': deviation of data
   'tend': tendency of data
   'min range': minimum range of data
   'mean': mean of data
   'min': minimum of data
   'min dev': minimum of data + deviation of data
   'max': maximum of data
   'min': minimum of data
   'div': range of data / length of data
   default: default value of increment, default = 0.1
   units_input: units of increment, set to 1 for default units
   """""
   default = kwargs.get('default', 0.1)
   units_input = kwargs.get('units_input', 1)

   data_diff = np.abs(np.diff(data))
   power_ = 1

   increment_list ={
   'default': default,
   'dev': distribution(data_diff, power_, 'dev'),
   'tend': distribution(data_diff, power_, 'tend')[0],
   'min range': distribution(data_diff, power_, 'distr range')[0][0],
   'mean': np.abs(data_diff).mean(),
   'min': (np.abs(data_diff).min()),
   'min dev': np.abs(data_diff).min() + distribution(data_diff, power_, 'dev'),
   'max': np.abs(data_diff).max()
   }
   return increment_list[increment_type]*units_input

def divider(data, set = True, units = 3):
   if set:
      return 10^(-units)
   else: 
      return np.ptp(data)//(10^units)
