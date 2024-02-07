import numpy as np

import cProfile
# Filter data by index_increment, greater_than, and less_than

def filterfunc(data, index_increment, greater_than, less_than):
  counter = 0; array_ = []; data_length = len(data)
  for val in data:
    if (val >= greater_than and val <= less_than) and (counter + index_increment < data_length):
      array_.append((val, data[counter + index_increment]))
    counter += 1
  return array_

def filterfunc2(data, index_increment, greater_than, less_than):
  data_length = len(data)
  return [(val, data[i + index_increment]) for i, val in enumerate(data) if greater_than <= val <= less_than and i + index_increment < data_length]

def filterfunc3(data, index_increment, greater_than, less_than):
    return [(val, data[i + index_increment]) 
            for i, val in enumerate(data[:-index_increment]) 
            if greater_than < val < less_than]

def directindices(data, index_increment, greater_than, less_than):
  results = []
  conditional_indices = list(np.where((data > greater_than) & (data < less_than))[0])
  for index in conditional_indices:
    if index + index_increment < len(data):
      results.append((data[index], data[index + index_increment]))
  return results

def conditionalmethod(data, index_increment, greater_than, less_than):
  results = []
  conditional_indices = list(np.where((data > greater_than) & (data < less_than))[0])
  for index in conditional_indices:
    if index + index_increment < len(data):
      results.append((data[index], data[index + index_increment]))
  return results

def removemethod(data, index_increment, greater_than, less_than):
  results = []
  conditional_indices = list(np.where((data > greater_than) & (data < less_than))[0])
  if len(data) - index_increment in conditional_indices:
    conditional_indices.remove(len(data) - index_increment)
  for i in conditional_indices:
    results.append((data[i], data[i + index_increment]))
  return results

# n = 7
# data = range(10**n)
# index_increment = 1
# greater_than = 3*10**(n - 1)
# less_than = 8*10**(n - 1)

# cProfile.run('filterfunc(data, index_increment, greater_than, less_than)')
# cProfile.run('filterfunc2(data, index_increment, greater_than, less_than)')
# cProfile.run('filterfunc3(data, index_increment, greater_than, less_than)')
