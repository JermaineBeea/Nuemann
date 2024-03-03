import numpy as np 
import pandas as pd
import cProfile
from Modules import DataMod
import matplotlib.pyplot as plt

class ForecastClass():
  def __init__(self, data, initial_val):
    self.data = data
    self.initial_val = initial_val
    self.boundSplit_called = False
    self.regionSplit_called = False
    self.method_used = DataMod.method_1  
    self.method_args = {
    'tend_evaluation' : True,
    'dynamic_change' : True,
    'use_prob' : True,
    'set_prob' : 0.5,
    'dev_type' : 1
    }

  def methodCalled (self, method_used = None, **kwargs):
    if method_used is not None:
        self.method_used = method_used  
    self.method_args.update(kwargs)
    return self.method_used
  
  def boundSplit (self, region_size, recursive_split = True):
    self.boundSplit_called = True
    data = self.data
    initial_val = self.initial_val
    self.region_size = region_size
    self.recursive_split = recursive_split
    if initial_val < data.min() or initial_val > data.max():      
      initial_val = data.max() if initial_val > data.max() else data.min() 
    self.current_data = DataMod.boundData(data, initial_val, region_size)
    self.method_return = self.method_used(self.current_data, **self.method_args)  

  def regionSplit (self, region_size, recursive_split = True):
    self.regionSplit_called = True
    data = self.data
    initial_val = self.initial_val
    self.region_size = region_size
    self.recursive_split = recursive_split
    data_regions, region_values = DataMod.splitData(data, initial_val, region_size)
    self.region_values = region_values
    self.net_process = [self.method_used(data_regions[i], **self.method_args) for i in range(len(data_regions))]
    region_index = np.digitize(initial_val, region_values)
    self.region_index = region_index
    if region_index == len(region_values): region_index -= 1
    if region_index == 0: region_index += 1
    self.method_return = self.net_process[region_index - 1]
  
  def generateChange (self, current_val):
    if self.boundSplit_called and self.recursive_split:
      data = self.data
      current_data = self.current_data
      region_size = self.region_size
      if current_val < data.min() or current_val > data.max():      
        current_val = data.max() if current_val > data.max() else data.min() 
        current_data = DataMod.boundData(data, current_val, region_size)
      elif current_val < current_data.min() or current_val > current_data.max():
        current_data = DataMod.boundData(data, current_val,region_size)
        self.current_data = current_data
      self.method_return = self.method_used(self.current_data, **self.method_args)
    
    elif self.regionSplit_called and self.recursive_split:
      region_values = self.region_values
      region_index = self.region_index
      current_regionIndex = np.digitize(current_val, region_values)
      if current_regionIndex != region_index:
        if current_regionIndex == len(region_values): current_regionIndex -= 1
        if current_regionIndex == 0: current_regionIndex += 1
        self.region_index = current_regionIndex
      self.method_return = self.net_process[self.region_index - 1]
    
    else:
      self.method_return = self.method_used(self.data, **self.method_args)
    change = DataMod.genChange(self.method_return)
    return change

path = r'EURAUD.ifx_M1_202402190000_202402191016.csv'

data = pd.read_csv(path, sep = '\t')['<CLOSE>'].dropna()
initial_val = data.iloc[-1] if isinstance(data, pd.Series) else data[-1]
region_size = (1/3)*np.ptp(data)
num_forecasts = 600
Forecast_iterations = 100

instance = ForecastClass(data, initial_val)
instance.methodCalled(DataMod.method_2, tend_evaluation = False)
instance.boundSplit(region_size, recursive_split = True)

Forecast = np.zeros((num_forecasts, Forecast_iterations))
for index1 in np.arange(num_forecasts):
  Forecast[index1, 0] = initial_val
  current_val = initial_val
  current_data = data
  for index2 in np.arange(1, Forecast_iterations):
    current_val += instance.generateChange(current_val)
    Forecast[index1, index2] = current_val

frame = pd.DataFrame(Forecast)
plt.plot(Forecast.T, color = 'grey')
plt.show()

