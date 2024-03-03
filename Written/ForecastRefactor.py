import numpy as np 
import pandas as pd
import cProfile
from Modules import DataMod
import matplotlib.pyplot as plt

path = r'EURAUD.ifx_M1_202402190000_202402191016.csv'

data = pd.read_csv(path, sep = '\t')['<CLOSE>'].dropna()
initial_val = data.iloc[-1] if isinstance(data, pd.Series) else data[-1]
region_size = (1/3)*np.ptp(data)
num_forecasts = 10
Forecast_iterations = 10

bound_split = 1
region_split = 1
if bound_split: region_split = False
recursive_split = 1

def method_called (arg, method_used = DataMod.method_1, **kwargs):
  key_args = {
  'tend_evaluation' : True,
  'dynamic_change' : True,
  'use_prob' : True,
  'set_prob' : 0.5,
  'dev_type' : 1
  }
  key_args.update(kwargs)
  return method_used(arg, **key_args)

def recursiveSplit (current_val, current_data, region_size, region_index ):
  if bound_split:
    if current_val < data.min() or current_val > data.max():      
      current_val = data.max() if current_val > data.max() else data.min() 
      current_data = DataMod.boundData(data, current_val, region_size)
    elif current_val < current_data.min() or current_val > current_data.max():
      current_data = DataMod.boundData(data, current_val,region_size)
    method_return = method_called(current_data)
  elif region_split:
    current_regionIndex = np.digitize(current_val, region_values)
    if current_regionIndex == len(region_values): current_regionIndex -= 1
    if current_regionIndex == 0: current_regionIndex += 1
    if current_regionIndex != region_index:
      region_index = current_regionIndex
    method_return = net_process[region_index - 1]
  return method_return

if bound_split:
  if initial_val < data.min() or initial_val > data.max():      
    initial_val = data.max() if initial_val > data.max() else data.min() 
  current_data = DataMod.boundData(data, initial_val, region_size)
  method_return = method_called(current_data)
elif region_split:
  data_regions, region_values = DataMod.splitData(data, initial_val, region_size)
  net_process = [method_called(data_regions[i]) for i in range(len(data_regions))]
  region_index = np.digitize(initial_val, region_values)
  if region_index == len(region_values): region_index -= 1
  if region_index == 0: region_index += 1
  method_return = net_process[region_index - 1]
else:
  method_return = method_called(data)

Forecast = np.zeros((num_forecasts, Forecast_iterations))
for index1 in np.arange(num_forecasts):
  Forecast[index1, 0] = initial_val
  current_val = initial_val
  current_data = data
  for index2 in np.arange(1, Forecast_iterations):
    if (bound_split or region_split) and recursive_split:
        if not region_split: region_index = None
        method_return = recursiveSplit(current_val, current_data, region_size, region_index)
    current_val += DataMod.genChange(method_return)
    Forecast[index1, index2] = current_val

frame = pd.DataFrame(Forecast)
plt.plot(Forecast.T, color = 'grey')
plt.show()

