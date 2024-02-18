import numpy as np
import pandas as pd
import cProfile
import logging as log

def distribution(data, deviation_type, output, tend_evaluation = True):
  data = np.array(data)
  if tend_evaluation:
    deviation = np.power(np.mean(np.abs(data[:, None] - data) ** deviation_type, axis=1), 1/deviation_type).min()
    min_indices = np.where(np.isclose(np.power(np.mean(np.abs(data[:, None] - data) ** deviation_type, axis=1), 1/deviation_type), deviation))
    tendency = np.unique(data[min_indices])
  else:
    tendency = np.mean(data)
    if deviation_type == 1 : deviation = np.std(data)
    else:deviation = np.power(np.mean(np.abs(data - tendency) ** deviation_type), 1/deviation_type)

  distribution = [tendency - deviation, tendency, tendency + deviation]
  distr_range = [tendency - deviation, tendency + deviation]
  concetenated_distribution = distribution
  conc_range = distr_range

  returnlibrary = {
    'dev': deviation, 
    'tend': tendency,
    'distr': distribution,
    'conc distr': concetenated_distribution,
    'distr range': distr_range,
    'conc range': conc_range
  }
  if output not in returnlibrary:
    raise KeyError(f'Error: output must be a string of "all" or {tuple(returnlibrary.keys())}')
  return returnlibrary[output]

def blitzDistr(data, deviation_type, output, tend_evaluation = True):
    data_array = np.array(np.concatenate(data))[:, np.newaxis] 
    if tend_evaluation:
      deviations = np.abs(data_array - data_array.T)**deviation_type
      yield_deviation = np.mean(deviations, axis=1)**(1/deviation_type)
      deviation = np.min(yield_deviation)
      min_indices = np.where(yield_deviation == deviation)
      tendency = list(np.unique(data[min_indices[0]]))
      minTend = np.min(tendency) 
      meanTend = np.mean(tendency) 
      maxTend = np.max(tendency)    
      distribution = [[tend - deviation, tend, tend + deviation] for tend in tendency]
      distr_range = [[tend - deviation, tend + deviation] for tend in tendency]
      concetenated_distribution = [minTend - deviation, meanTend, maxTend + deviation]
      conc_range = [minTend - deviation, maxTend + deviation]
    
    else:
      tendency = np.mean(data)
      if deviation_type == 1 : deviation = np.std(data)
      else:deviation = np.power(np.mean(np.abs(data - tendency) ** deviation_type), 1/deviation_type)

    distribution = [tendency - deviation, tendency, tendency + deviation]
    distr_range = [tendency - deviation, tendency + deviation]
    concetenated_distribution = distribution
    conc_range = distr_range

    returnlibrary = {
      'dev': deviation, 
      'tend': tendency,
      'distr': distribution,
      'conc distr': concetenated_distribution,
      'distr range': distr_range,
      'conc range': conc_range
    }
    if output not in returnlibrary:
      raise KeyError(f'Error: output must be a string of "all" or {tuple(returnlibrary.keys())}')
    return returnlibrary[output]

def probDistr(distr_range, original_data, return_type = (1,2,3,4,5), decimal_convert = True, roundup = None):
  if roundup is None:roundup = 2 if decimal_convert else 0
  if not isinstance(original_data, np.ndarray):
    original_data = np.array(original_data)
  CounterArr = np.array([]); 
  Datasize = original_data.size; count = 0
  for rangeVal, nextRangeVal in zip(distr_range, distr_range[1:]):
    for data in original_data.copy():  # Iterate over a copy of original_data
      if rangeVal <= data <= nextRangeVal:
        original_data = np.delete(original_data, np.where(original_data == data))  # Delete elements from original_data
        count += 1
    CounterArr = np.append(CounterArr, count); count = 0
  SumCount = CounterArr.sum()
  ProbArr = np.round((CounterArr/Datasize)*pow(100, 1 - decimal_convert), roundup) 
  NetProb = np.round((SumCount/Datasize)*pow(100, 1 - decimal_convert), roundup)
  SumCount = CounterArr.sum()
  ProbArr = np.round((CounterArr/Datasize)*pow(100, 1 - decimal_convert), roundup) 
  NetProb = np.round((SumCount/Datasize)*pow(100, 1 - decimal_convert), roundup)

  if SumCount != 0:
    RelativeProb = np.round((CounterArr/SumCount)*pow(100, 1 - decimal_convert), roundup)
  else:
    print("SumCount is zero, cannot calculate RelativeProb")
    RelativeProb = np.zeros_like(CounterArr)  
  
  return [(CounterArr, SumCount, ProbArr, RelativeProb, NetProb)[digit - 1] for digit in return_type]

def blitzProbDistr(distr_range, original_data, return_type = (1,2,3,4,5), decimal_convert = True, roundup = None):
  if roundup is None: roundup = 2 if decimal_convert else 0
  if not isinstance(original_data, np.ndarray):
    original_data = np.array(original_data)
  
  Datasize = original_data.size
  ranges = np.array([distr_range[:-1], distr_range[1:]]).T
  data = original_data[None, :]
  in_range = (ranges[:, 0, None] <= data) & (data <= ranges[:, 1, None])
  CounterArr = np.sum(in_range, axis=1)
  original_data = original_data[~np.any(in_range, axis=0)]
  SumCount = CounterArr.sum()
  ProbArr = np.round((CounterArr/Datasize)*pow(100, 1 - decimal_convert), roundup) 
  NetProb = np.round((SumCount/Datasize)*pow(100, 1 - decimal_convert), roundup)

  if SumCount != 0:
    RelativeProb = np.round((CounterArr/SumCount)*pow(100, 1 - decimal_convert), roundup)
  else:
    print("SumCount is zero, cannot calculate RelativeProb")
    RelativeProb = np.zeros_like(CounterArr)  

  return [(CounterArr, SumCount, ProbArr, RelativeProb, NetProb)[digit - 1] for digit in return_type]

def filterPair(data, **kwargs):
  order = kwargs.get('order', None)
  filter_flag = kwargs.get('filter', False)
  pair_flag = kwargs.get('pair', False)
  filterFunc = kwargs.get('filterFunc', None)
  pair_index = kwargs.get('pair_index', 1)
  axis_index = kwargs.get('axis_index', 0)

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

def diffFunction(data, n_order = 1, return_type = 0):
  data = np.array(data, dtype = object)if isinstance(data, list) else data
  if len(data.shape) < 2:   
    differences =  np.diff(data, n_order, axis = 0)
  elif data.shape[1] < 3:
    differences = np.diff(data, n_order, axis = 1)
  else: raise ValueError('Data must be of shape (a,b) where b < 3')
  
  diffsize = differences.size
  Posvalues, Negvalues = differences[differences > 0], differences[differences < 0]
  Posprob, NegProb = Posvalues.size/diffsize, Negvalues.size/diffsize
  return_libr = {0:differences, 1:Posvalues, 2:Negvalues, 'pos prob':Posprob, 'neg prob':NegProb}
  return [item for key in [return_type] for item in return_libr[key]]

def indexSplice(data,sliceIncr, **kwargs):
  start = kwargs.get('start', 0)
  if isinstance(data, (pd.DataFrame, pd.Series)): Datasize = data.size
  else: Datasize = len(data)
  return np.arange(start, Datasize, sliceIncr)

if __name__ == '__main__':

  iterations = 10**4
  data = np.arange(iterations)
  deviation_type = 1

  # 'dev', 'tend', 'distr', 'conc distr', distr range', 'conc range', 'all'
  output = 'distr'
  return_type = 1,2,3,4 
 
  cProfile.run('blitz_distr(data, deviation_type, output, False)')
  cProfile.run('blitz_distr(data, deviation_type, output)')



