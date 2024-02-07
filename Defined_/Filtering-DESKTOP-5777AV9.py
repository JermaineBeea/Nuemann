import numpy as np

# Filter data by index_increment, greater_than, and less_than

def filterfunc(data, index_increment, greater_than, less_than):
  counter = 0
  array_ = []
  for val in data:
    if (val >= greater_than and val <= less_than) and (counter + index_increment < len(data)):
      array_.append((val, data[counter + index_increment]))
    counter += 1
  return array_

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
