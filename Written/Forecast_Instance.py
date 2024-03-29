import numpy as np 
import pandas as pd
import cProfile
from Modules import DataMod
import matplotlib.pyplot as plt

class ForecastFunc():
  def __init__(self, data, initial_val):
    # Method called flags
    self.flag = 1
    self.flag2 = 1
    self.run_flag = 1
    # Data and initial value
    self.data = data
    self.initial_val = initial_val
    self.BoundSplit_called = False
    self.UniformSplit_called = False
    # Default method and arguments
    self.method_used = DataMod.regionChange
    self.method_args = {
    'tend_evaluation' : True,
    'dynamic_change' : True,
    'use_prob' : True,
    'set_prob' : 0.5,
    'dev_type' : 1
    }

  def MethodCalled (self, method_used = None, **kwargs):
    if method_used is not None:
        self.method_used = method_used  
    self.method_args.update(kwargs)
    print(f'Change Function used: {self.method_used.__name__}')

  def BoundSplit (self, region_size, recursive_split = True):
    self.BoundSplit_called = True ; print(f'Bound Split Method called')
    if self.UniformSplit_called and self.BoundSplit_called:
      self.UniformSplit_called = False; print(f'BOUND METHOD OVERWRITES UNIFORM METHOD')
    data = self.data
    initial_val = self.initial_val
    self.region_size = region_size
    self.recursive_split = recursive_split
    if initial_val < data.min() or initial_val > data.max():      
      initial_val = data.max() if initial_val > data.max() else data.min() 
    self.current_data = DataMod.boundSplitFunc(data, initial_val, region_size)
    self.method_return = self.method_used(self.current_data, **self.method_args)  

  def UniformSplit (self, region_size, recursive_split = True):
    self.UniformSplit_called = True ; print(f'Uniform Split Method called')
    if self.BoundSplit_called and self.UniformSplit_called: 
      self.BoundSplit_called = False; print(f'UNIFORM NETHOD OVERWRITES BOUND METHOD')
    data = self.data
    initial_val = self.initial_val
    self.region_size = region_size
    self.recursive_split = recursive_split
    data_regions, region_values = DataMod.uniformSplitFunc(data, initial_val, region_size)
    self.region_values = region_values
    self.net_process = [self.method_used(data_regions[i], **self.method_args) for i in range(len(data_regions))]
    region_index = np.digitize(initial_val, region_values)
    self.region_index = region_index
    if region_index == len(region_values): region_index -= 1
    if region_index == 0: region_index += 1
    self.method_return = self.net_process[region_index - 1]
  
  def GenerateChange (self, current_val):
    if self.BoundSplit_called and self.recursive_split:
      # Method called flags
      if self.flag == 1: print(f'Bound Recursion Split') ; self.flag+= 1; 
      data = self.data
      current_data = self.current_data
      region_size = self.region_size
      if current_val < data.min() or current_val > data.max():      
        current_val = data.max() if current_val > data.max() else data.min() 
        current_data = DataMod.boundSplitFunc(data, current_val, region_size)
      elif current_val < current_data.min() or current_val > current_data.max():
        current_data = DataMod.boundSplitFunc(data, current_val,region_size)
        self.current_data = current_data
      self.method_return = self.method_used(self.current_data, **self.method_args)
    
    elif self.UniformSplit_called and self.recursive_split:
      # Method called flags
      if self.flag2 == 1: print(f'Uniform Recursion Split') ; self.flag2 += 1
      region_values = self.region_values
      region_index = self.region_index
      current_regionIndex = np.digitize(current_val, region_values)
      if current_regionIndex != region_index:
        if current_regionIndex == len(region_values): current_regionIndex -= 1
        if current_regionIndex == 0: current_regionIndex += 1
        self.region_index = current_regionIndex
      self.method_return = self.net_process[self.region_index - 1]
    
    else:
      if (not self.BoundSplit_called and not self.UniformSplit_called) and self.run_flag == 1:
          self.method_return = self.method_used(self.data, **self.method_args)
          print(f'No Split Method called')        
      self.run_flag += 1
    change = DataMod.genChange(self.method_return)
    return change

if __name__ == '__main__':
  path = r'EURAUD.ifx_M1_202402190000_202402191016.csv'
  data = pd.read_csv(path, sep = '\t')['<CLOSE>'].dropna()
  initial_val = data.iloc[-1] if isinstance(data, pd.Series) else data[-1]
  region_size = (1/3)*np.ptp(data)
  num_forecasts = 10
  Forecast_iterations = 10
  
  instance = ForecastFunc(data, initial_val)
  instance.MethodCalled( DataMod.posNegChange, tend_evaluation = False)
  instance.UniformSplit(region_size, recursive_split = 0)
  instance.BoundSplit(region_size, recursive_split = 0)
  
  Forecast = np.zeros((num_forecasts, Forecast_iterations))
  for index1 in np.arange(num_forecasts):
    Forecast[index1, 0] = initial_val
    current_val = initial_val
    current_data = data
    for index2 in np.arange(1, Forecast_iterations):
      current_val += instance.GenerateChange(current_val)
      Forecast[index1, index2] = current_val
  
  frame = pd.DataFrame(Forecast)
  plt.plot(Forecast.T, color = 'grey')
  plt.show()
