import numpy as np
import cProfile

# Constructed from tuplefunc: Module CombinationsYield.py

# TODO delete code late 	
def distribution00(data, deviation_type, output):
    yield_deviation = tuple(np.mean(tuple(abs(i-j)**deviation_type for j in data))**(1/deviation_type) for i in data)
    deviation = min(yield_deviation)
    min_indices = np.where(yield_deviation == deviation)
    tendency = list(np.unique([data[index] for index in min_indices[0]]))
    distribution = [[tend - deviation, tend, tend + deviation] for tend in tendency]
    distr_range = [[tendency - deviation, tendency + deviation] for tendency in tendency]
    concetenated_distribution = [min(tendency) - deviation, np.mean(tendency), max(tendency) + deviation]
    conc_range = [min(tendency) - deviation, max(tendency) + deviation]
    
    returnlibrary = {
    'dev':deviation, 'tend':tendency,
    'distr':distribution,'conc distr':concetenated_distribution,
    'distr range':distr_range,'conc range':conc_range
    }
    
    if output not in returnlibrary:
        raise KeyError(f'Error: output must be a string of "all" or {tuple(returnlibrary.keys())}')
    return returnlibrary[output]

def distribution(data, deviation_type, output):
    data_array = np.array(data)
    data_array = data_array[:, np.newaxis]  # reshape data_array to allow broadcasting
    deviations = np.abs(data_array - data_array.T)**deviation_type
    yield_deviation = np.mean(deviations, axis=1)**(1/deviation_type)
    
    deviation = np.min(yield_deviation)
    min_indices = np.where(yield_deviation == deviation)
    tendency = list(np.unique([data[index] for index in min_indices[0]]))
    distribution = [[tend - deviation, tend, tend + deviation] for tend in tendency]
    distr_range = [[tendency - deviation, tendency + deviation] for tendency in tendency]
    concetenated_distribution = [min(tendency) - deviation, np.mean(tendency), max(tendency) + deviation]
    conc_range = [min(tendency) - deviation, max(tendency) + deviation]
    
    returnlibrary = {
    'dev':deviation, 'tend':tendency,
    'distr':distribution,'conc distr':concetenated_distribution,
    'distr range':distr_range,'conc range':conc_range
    }
    
    if output not in returnlibrary:
        raise KeyError(f'Error: output must be a string of "all" or {tuple(returnlibrary.keys())}')
    return returnlibrary[output]

def valuedistr(element, data, deviation_type, output):
    try:
        yield_deviation = tuple(np.mean(tuple(abs(element-j)**deviation_type for j in data))**(1/deviation_type))
        deviation = min(yield_deviation)
        min_indices = np.where(yield_deviation == deviation)
        prox_tend = list(np.unique([data[index] for index in min_indices[0]]))
        distribution = [element - deviation, element, element + deviation]
        distr_range = [element - deviation, element + deviation]
        
        returnlibrary = {
        'dev':deviation, 'tend':prox_tend,
        'distr':distribution,
        'distr range':distr_range,
        }
        return returnlibrary[output]
    except TypeError as e:    
        return f'Error: {e}'
    except ValueError:
        return 'Data is empty'
    except KeyError:   
        return f'Error: output must be a string of "all" or {tuple(returnlibrary.keys())}'

if __name__ == '__main__':

  iterations = 10
  data = range(iterations)
  deviation_type = 2

  # 'dev', 'tend', 'distr', 'conc distr', distr range', 'conc range', 'all'
  output = 'dev'
  result = distribution(data, deviation_type, output)
  print(result)
  # cProfile.run('distribution(data, deviation_type, output)')
  # cProfile.run('distribution_2(data, deviation_type, output)')



