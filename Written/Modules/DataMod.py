import numpy as np
import cProfile
import pandas as pd
import random

def DistrFunc (data, **kwargs):
  
  dev_type = kwargs.get('dev_type', 1)
  tend_evaluation = kwargs.get('tend_evaluation', True)
  return_type = kwargs.get('return_type', 'conc distr')

  if tend_evaluation:
    deviation = np.power(np.mean(np.abs(data[:, None] - data) ** dev_type, axis=1), 1/dev_type).min()
    min_indices = np.where(np.isclose(np.power(np.mean(np.abs(data[:, None] - data) ** dev_type, axis=1), 1/dev_type), deviation))
    tendency = np.unique(data[min_indices])
  else:
    tendency = np.mean(data)
    if dev_type == 1 : deviation = np.std(data)
    else:deviation = np.power(np.mean(np.abs(data - tendency) ** dev_type), 1/dev_type)

  distribution = [tendency - deviation, tendency, tendency + deviation]
  distr_range = [tendency - deviation, tendency + deviation]
  concatenated_distribution = distribution
  conc_range = distr_range

  return_libr = {
    'dev': deviation, 
    'tend': tendency,
    'distr': distribution,
    'conc distr': concatenated_distribution,
    'conc tend': concatenated_distribution[1],
    'distr range': distr_range,
    'conc range': conc_range
  }
  if isinstance(return_type, tuple): 
    return [return_libr[key] for key in return_type]
  else: 
    return [return_libr[key] for key in [return_type]][0]

def blitzDistr (data, **kwargs):
  dev_type = kwargs.get('dev_type', 1)
  tend_evaluation = kwargs.get('tend_evaluation', True)
  return_type = kwargs.get('return_type', 'conc distr')

  if isinstance(data, list): data = np.array(data)
  if data.size == 0: 
    if isinstance(return_type, tuple):return [None for _ in return_type]
    else: return None
  if len(data.shape) > 1: data = np.concatenate(data)
  data_array = np.array(data)[:, np.newaxis] 

  if tend_evaluation:
    deviations = np.abs(data_array - data_array.T)**dev_type
    yield_deviation = np.mean(deviations, axis = 1)**(1/dev_type)
    min_deviation = np.min(yield_deviation)
    min_indices = np.where(yield_deviation == min_deviation)
    tendency = list(np.unique(data[min_indices[0]]))
    meanTend = np.mean(tendency) 
    distribution = [[tend - min_deviation, tend, tend + min_deviation] for tend in tendency]
    distr_range = [[tend - min_deviation, tend + min_deviation] for tend in tendency]
    concatenated_distribution = [meanTend - min_deviation, meanTend, meanTend + min_deviation]
    conc_range = [meanTend - min_deviation, meanTend + min_deviation]
    deviation = min_deviation
  else:
    tendency = np.mean(data)
    if dev_type == 1 : deviation = np.std(data)
    else:deviation = np.power(np.mean(np.abs(data - tendency) ** dev_type), 1/dev_type)

    distribution = [tendency - deviation, tendency, tendency + deviation]
    distr_range = [tendency - deviation, tendency + deviation]
    concatenated_distribution = distribution
    conc_range = distr_range

  return_libr = {
  'dev': deviation, 
  'tend': tendency,
  'distr': distribution,
  'conc distr': concatenated_distribution,
  'conc tend': concatenated_distribution[1],
  'distr range': distr_range,
  'conc range': conc_range
  }
  
  if isinstance(return_type, tuple): 
    return [return_libr[key] for key in return_type]
  else: 
    return [return_libr[key] for key in [return_type]][0]

def regionMap_pair (original_data, region_values = None, **kwargs):
  if isinstance(original_data, list): original_data = np.array(original_data)
  pair_data = kwargs.get('pair_data', False)
  pair_increment = kwargs.get('pair_increment', 1) if pair_data else 0
  return_type = kwargs.get('return_type', 1)

  if isinstance(region_values, str):
    if region_values.lower() == 'map distr': 
      kwargs_copy = kwargs.copy()
      kwargs_copy.pop('return_type', None)
      distr_return = kwargs_copy.get('distr_return', 'conc distr')
      region_values = blitzDistr(original_data, return_type = distr_return, **kwargs_copy)

  if isinstance(region_values, list): original_data = np.array(original_data)
  n = len(region_values) - 1
  mapped_data = [[] for _ in range(n)]

  filtered_data = original_data[(original_data >= min(region_values)) & (original_data <= max(region_values))]

  for val, nextval in zip(filtered_data, filtered_data[pair_increment:]):    
    bin_value = np.digitize(val, region_values)
    if bin_value > n: bin_value = n
    if pair_data:
      mapped_data[bin_value - 1].append((val, nextval))
    else: mapped_data[bin_value - 1].append(val)
  
  Data_size = original_data.size
  net_MapData_size = len(mapped_data[0]) if len(mapped_data) == 1 else len(np.concatenate(mapped_data))
  mappedData_size = [len(sub_data) for sub_data in mapped_data]
  Total_prob = net_MapData_size / Data_size
  abs_prob = [len(sub_data) / Data_size for sub_data in mapped_data]
  relative_prob = [len(sub_data) / net_MapData_size for sub_data in mapped_data]
  
  return_list = [mapped_data, relative_prob, abs_prob, Total_prob, net_MapData_size, mappedData_size, region_values]

  if  isinstance(return_type,tuple): 
    return [return_list[digit - 1] for digit in return_type]
  else:  
    return [return_list[digit - 1] for digit in [return_type]][0]

def filterPair (data, **kwargs):
  order = kwargs.get('order', None)
  filter_flag = kwargs.get('filter_flag', False)
  pair_flag = kwargs.get('pair', False)
  filterFunc = kwargs.get('filterFunc', None)
  pair_index = kwargs.get('pair_index', 1)
  axis_index = kwargs.get('axis_index', 0)

  if isinstance(data, list): data = np.array(data)

  if order is not None: 
    filter_flag = True 
    pair_flag = True

  if pair_flag:
    PairedData = np.transpose([data[:-pair_index],data[pair_index:]])
    if order == 0 and filterFunc is not None:
      Filtered_PairedData = PairedData[filterFunc(PairedData[:,axis_index])]
      return Filtered_PairedData
    else: 
      return PairedData

  if filter_flag and filterFunc is not None:
    FilteredData = data[filterFunc(data)]
    if order == 1:
      Paired_FilteredData = np.transpose([FilteredData[:-pair_index], FilteredData[pair_index:]])
      return  Paired_FilteredData
    else: 
      return FilteredData

  return print('No filter or pair operation performed') 

def diffFunction (data, **kwargs):
  n_order = kwargs.get('n_order', 1)
  axis = kwargs.get('axis', 1)
  return_type = kwargs.get('return_type', 0)
  
  data_shape = np.shape(data)
  if len(data) == 0: return print('Data is empty')
  elif len(data_shape) == 1: 
    differences =  np.diff(data, n_order)
  elif len(data_shape) == 2:
    differences =  np.diff(data, n_order, axis = axis)
  elif len(data) > 2: return print('Data shape not supported: must be less than 3D')

  diffsize = differences.size
  Posvalues, Negvalues = differences[differences > 0], differences[differences < 0]
  Posprob, NegProb = Posvalues.size/diffsize, Negvalues.size/diffsize
  return_libr = {0:differences, 1:Posvalues, 2:Negvalues, 'pos prob':Posprob, 'neg prob':NegProb}

  if isinstance(return_type, tuple): 
    return [return_libr[key] for key in return_type]
  else: 
    return [return_libr[key] for key in [return_type]][0]

def boundSplitFunc (data, value, region_size):
  if isinstance(data, list): data = np.array(data)
  upper_bound = value + (abs(data.max() - value)/np.ptp(data))*region_size
  lower_bound = value - (abs(data.min() - value)/np.ptp(data))*region_size
  current_data = data[(data >= lower_bound) & (data <= upper_bound)]
  return current_data

def uniformSplitFunc (data, val, region_size):
  if isinstance(data, list): data = np.array(data)
  steps = np.floor(np.ptp(data)/region_size) + 1
  region_values = np.linspace(data.min(), data.max(), int(steps))
  split_data = regionMap_pair(data, region_values, pair_data =  True)
  region_index = np.digitize(val, region_values)
  if region_index == len(region_values): region_index -= 1
  if region_index == 0: region_index += 1
  return split_data, region_values

def regionChange (data, **kwargs):
  dynamic_change = kwargs.get('dynamic_change', True)
  use_prob = kwargs.get('use_prob', True)
  set_prob = kwargs.get('set_prob', 0.5)
  dev_type = kwargs.get('dev_type', 1)
  tend_evaluation = kwargs.get('tend_evaluation', True)

  differences = diffFunction(data, return_type = 0)
  diff_distr = blitzDistr(differences, dev_type = dev_type, tend_evaluation = tend_evaluation,  return_type = 'conc distr')
  region_mapped, probability = regionMap_pair(differences , diff_distr, return_type = (1,2))
  lower_region = region_mapped[0]
  upper_region = region_mapped[-1]
  prob_upperRegion = probability[-1] if use_prob else set_prob
  distr_lowerRegion, tend_lowerRegion = blitzDistr(lower_region, dev_type = dev_type, tend_evaluation = tend_evaluation, return_type = ('conc range', 'conc tend'))
  distr_upperRegion, tend_upperRegion = blitzDistr(upper_region, dev_type = dev_type, tend_evaluation = tend_evaluation, return_type = ('conc range', 'conc tend'))
  
  if dynamic_change:
    return distr_lowerRegion, distr_upperRegion, prob_upperRegion
  else:
    return tend_lowerRegion, tend_upperRegion, prob_upperRegion

def posNegChange (data, **kwargs):
  dynamic_change = kwargs.get('dynamic_change', True)
  use_prob = kwargs.get('use_prob', True)
  set_prob = kwargs.get('set_prob', 0.5)
  dev_type = kwargs.get('dev_type', 1)
  tend_evaluation = kwargs.get('tend_evaluation', True)

  pos_val, neg_val, prob_pos = diffFunction(data, return_type = (1, 2, 'pos prob'))
  distr_pos, tend_pos = blitzDistr(pos_val, dev_type = dev_type, tend_evaluation = tend_evaluation, return_type = ('conc range', 'conc tend'))
  distr_neg, tend_neg = blitzDistr(neg_val, dev_type = dev_type, tend_evaluation = tend_evaluation, return_type = ('conc range', 'conc tend'))
  prob_pos = prob_pos if use_prob else set_prob

  if dynamic_change:
    return distr_neg, distr_pos, prob_pos
  else:
    return tend_neg, tend_pos, prob_pos

def genChange (method_data):
  if method_data[0] is None: return method_data[1] if len(method_data[1]) == 1 else random.uniform(*method_data[1])
  if method_data[1] is None: return method_data[0] if len(method_data[0]) == 1 else random.uniform(*method_data[0])
  lower_change = method_data[0] if len(method_data[0]) == 1 else random.uniform(*method_data[0])
  upper_change = method_data[1] if len(method_data[1]) == 1 else random.uniform(*method_data[1])
  return upper_change if random.random() > method_data[2] else lower_change

if __name__== '__main__':
  path = r'/workspaces/Nuemann/Written/EURAUD.ifx_M1_202402190000_202402191016.csv'
  data = pd.read_csv(path, sep = '\t')['<CLOSE>'].dropna()

  data = np.arange(21).reshape(7,3)
  data_frame = pd.DataFrame(data)
  # result1, result2 = regionMap_pair(data, region_values = [0, 5, 10, 20], return_type = (1,2))
  # print(f'result1: {result1} and result2: {result2} \n')
  result = data_frame.apply(regionMap_pair, axis = 0, dev_type = 2, region_values = 'map distr', return_type = (1,5))
  print(f'result {result[:1]} \n')
  # mapped_data = regionMap_pair(data, region_values = 'map distr', return_type = (5,6,7))
  # print(f'mapped_data: {mapped_data} \n')
  

  
