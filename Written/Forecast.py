import numpy as np 
import pandas as pd
import cProfile
from Modules import DataMod
import matplotlib.pyplot as plt
import IPython.display as display

def ForecastFunc(data, initial_val, **kwargs):
  region_split = kwargs.get('region_split', False)
  bound_split = kwargs.get('bound_split', False)
  recursive_split = kwargs.get('recursive_split', False)
  split_size = kwargs.get('split_size', (1/3)*np.ptp(data))
  method_used = kwargs.get('method_used', DataMod.method_1)
  initial_val = kwargs.get('inital_val', data.iloc[-1] if isinstance(data, pd.Series) else data[-1])
  num_forcast = kwargs.get('num_forcast', 100)
  forecast_iterations = kwargs.get('Forecast_iterations', len(data))

  def method_called (data_passed, method_used = method_used, **kwargs):
    default_args = {
    'tend_evaluation' : True,
    'dynamic_change' : True,
    'use_prob' : True,
    'set_prob' : 0.5,
    'dev_type' : 1
    }
    default_args.update(kwargs)
    return method_used(data_passed, **default_args)

  Forecast = np.zeros((num_forcast, forecast_iterations))
  for index1 in np.arange(num_forcast):
    current_val = initial_val
    for index2 in np.arange(forecast_iterations):
      if index2 == 0: 
        Forecast[index1, index2] = current_val
        continue
      
      if current_val > data.max(): 
        current_data = DataMod.boundData(data, data.max(), split_size)
        change_behaviour = method_called(current_data)
      elif current_val < data.min(): 
        current_data = DataMod.boundData(data, data.min(), split_size)
        change_behaviour = method_called(current_data)
      elif bound_split and index2 == 1:
        current_data = DataMod.boundData(data, current_val,split_size)
        change_behaviour = method_called(current_data)
      elif bound_split and recursive_split:
          if not (current_val>= current_data.min() and current_val <= current_data.max()):
            current_data = DataMod.boundData(data, current_val,split_size)
            change_behaviour = method_called(current_data)
    
      elif region_split and index2 == 1:
        data_regions, region_values = DataMod.splitData(data, current_val, split_size)
        region_index = np.digitize(current_val, region_values)
        if region_index == len(region_values): region_index -= 1
        if region_index == 0: region_index += 1
        net_process = [method_called(region) for region in data_regions]
        change_behaviour = net_process[region_index - 1]
      elif region_split and recursive_split:
        current_regionIndex = np.digitize(current_val, region_values)
        if current_regionIndex == len(region_values): current_regionIndex -= 1
        if current_regionIndex == 0: current_regionIndex += 1
        if current_regionIndex != region_index:
          region_index = current_regionIndex
          change_behaviour = net_process[region_index - 1]

      elif index2 == 1:
        current_data = data
        change_behaviour = method_called(current_data)  

      current_val += DataMod.genChange(change_behaviour)
      Forecast[index1, index2] = current_val
  return Forecast

path = r'/workspaces/Nuemann/Written/EURAUD.ifx_M1_202402190000_202402191016.csv'

data = pd.read_csv(path, sep = '\t')['<CLOSE>'].dropna()
initial_val = data.iloc[-1] if isinstance(data, pd.Series) else data[-1]
print(f'Initial value: {initial_val}')

kwargs = {
'split_size' : (1/3)*np.ptp(data),
'region_split' : 0,
'bound_split' : True,
'recursive_split' : True,
'method_used' : DataMod.method_1,
'num_forcast' : 100,
'forecast_iterations' : 100,

'tend_evaluation' : True,
'dynamic_change' : True,
'use_prob' : True,
'set_prob' : 0.5,
'dev_type' : 1
}

Forecast_list = ForecastFunc(data, initial_val, **kwargs)
Forecast_list = pd.DataFrame(Forecast_list)
moving_avg = Forecast_list.rolling(window=10).mean()
moving_distr = Forecast_list.apply(DataMod.blitzDistr, axis = 0, return_type = 'conc range')
max_mvDistri = moving_distr.max().max()
min_mvDistri = moving_distr.min().min()

from_ = data.size
x_range = np.arange(from_, from_ + Forecast_list.shape[1])

plt.plot(data, color = 'orange')
plt.plot(x_range, Forecast_list.T, color = 'grey', alpha = 0.2)
plt.plot(x_range, moving_distr.T, color = 'blue')
plt.axhline(y = max_mvDistri, color = 'red', linestyle = '--')
plt.axhline(y = min_mvDistri, color = 'red', linestyle = '--')
plt.show()

