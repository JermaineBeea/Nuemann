import numpy as np 
import pandas as pd
import cProfile
from Modules import DataMod
import matplotlib.pyplot as plt

path = r'EURAUD.ifx_M1_202402190000_202402191016.csv'

data = pd.read_csv(path, sep = '\t')['<CLOSE>'].dropna()
initial_val = data.iloc[-1] if isinstance(data, pd.Series) else data[-1]
print(f'Initial value: {initial_val}')

split_data = True
bounding = False
if bounding:
  recursive_bounding = False

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

region_size = (1/3)*np.ptp(data)
num_forecasts = 1000
Forecast_iterations = 1000
Forecast = np.zeros((num_forecasts, Forecast_iterations))

for index1 in np.arange(num_forecasts):
  current_val = initial_val
  for index2 in np.arange(Forecast_iterations):
    if index2 == 0: 
      Forecast[index1, index2] = current_val
      continue
    
    if current_val > data.max(): 
      current_data = DataMod.boundData(data, data.max(), region_size)
      method_result = method_called(current_data)
    elif current_val < data.min(): 
      current_data = DataMod.boundData(data, data.min(), region_size)
      method_result = method_called(current_data)
    elif bounding and index2 == 1:
      current_data = DataMod.boundData(data, current_val,region_size)
      method_result = method_called(current_data)
    elif bounding and recursive_bounding:
        if not (current_val>= current_data.min() and current_val <= current_data.max()):
          current_data = DataMod.boundData(data, current_val,region_size)
          method_result = method_called(current_data)
   
    elif split_data and index2 == 1:
      data_regions, region_values = DataMod.splitData(data, current_val, region_size)
      region_index = np.digitize(current_val, region_values)
      if region_index == len(region_values): region_index -= 1
      if region_index == 0: region_index += 1
      net_process = [method_called(region) for region in data_regions]
      method_result = net_process[region_index - 1]
    elif split_data:
      current_regionIndex = np.digitize(current_val, region_values)
      if current_regionIndex == len(region_values): current_regionIndex -= 1
      if current_regionIndex == 0: current_regionIndex += 1
      if current_regionIndex != region_index:
        region_index = current_regionIndex
        method_result = net_process[region_index - 1]

    elif index2 == 1:
      current_data = data
      method_result = method_called(current_data)  

    current_val += DataMod.genChange(method_result)
    Forecast[index1, index2] = current_val
    
plt.plot(Forecast.T)
plt.show()

