import numpy as np 
import pandas as pd
import DataModification
import matplotlib.pyplot as plt

class ForecastFunc():
  def __init__(self, data, initial_val):
    self.data = data
    self.initial_val = initial_val
    self.bound_split_called = False
    self.region_split_called = False
    self.method_used = DataModification.method_1  

  def method_called (self, arg, method_used = None, **kwargs):
    if method_used is not None:
        self.method_used = method_used  
    key_args = {
    'tend_evaluation' : True,
    'dynamic_change' : True,
    'use_prob' : True,
    'set_prob' : 0.5,
    'dev_type' : 1
    }
    key_args.update(kwargs)
    return self.method_used(arg, **key_args)  
  
  def bound_split (self, region_size, recursive_split = True):
    self.bound_split_called = True
    data = self.data
    initial_val = self.initial_val
    self.region_size = region_size
    self.recursive_split = recursive_split
    if initial_val < data.min() or initial_val > data.max():      
      initial_val = data.max() if initial_val > data.max() else data.min() 
    self.current_data = DataModification.boundData(data, initial_val, region_size)
    self.method_return = self.method_called(self.current_data)  

  def region_split (self, region_size, recursive_split = True):
    self.region_split_called = True
    data = self.data
    initial_val = self.initial_val
    self.region_size = region_size
    self.recursive_split = recursive_split
    data_regions, region_values = DataModification.splitData(data, initial_val, region_size)
    self.region_values = region_values
    self.net_process = [self.method_called(data_regions[i]) for i in range(len(data_regions))]
    region_index = np.digitize(initial_val, region_values)
    self.region_index = region_index
    if region_index == len(region_values): region_index -= 1
    if region_index == 0: region_index += 1
    self.method_return = self.net_process[region_index - 1]
  
  def generateChange (self, current_val):
    if self.bound_split_called and self.recursive_split:
      data = self.data
      current_data = self.current_data
      region_size = self.region_size
      if current_val < data.min() or current_val > data.max():      
        current_val = data.max() if current_val > data.max() else data.min() 
        current_data = DataModification.boundData(data, current_val, region_size)
      elif current_val < current_data.min() or current_val > current_data.max():
        current_data = DataModification.boundData(data, current_val,region_size)
        self.current_data = current_data
      self.method_return = self.method_called(self.current_data)
    
    elif self.region_split_called and self.recursive_split:
      region_values = self.region_values
      region_index = self.region_index
      current_regionIndex = np.digitize(current_val, region_values)
      if current_regionIndex != region_index:
        if current_regionIndex == len(region_values): current_regionIndex -= 1
        if current_regionIndex == 0: current_regionIndex += 1
        self.region_index = current_regionIndex
      self.method_return = self.net_process[self.region_index - 1]
    
    else:
      self.method_return = self.method_called(self.data)
    change = DataModification.genChange(self.method_return)
    return change

