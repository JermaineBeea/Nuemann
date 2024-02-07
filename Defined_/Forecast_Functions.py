import sys
sys.path.append("..")
sys.path.insert(0, 'C:/Users/tebne/OneDrive/Programming/Written/')

from Defined_.Filtering import filterfunc
from Defined_.Distribution import distribution
from Defined_.Math import difference, random_func

import random as random
import numpy as np


def rangeincrement(data, increment_type, power_, **kwargs):
   """""
   data: data to be evaluated
   increment_type: type of increment
   power: power of deviation
   'default': default value of increment
   'dev': deviation of data
   'tend': tendency of data
   'min range': minimum range of data
   'mean': mean of data
   'min': minimum of data
   'min dev': minimum of data + deviation of data
   'max': maximum of data
   'min': minimum of data
   'div': range of data / length of data
   default: default value of increment, default = 0.1
   Factor: units of increment, set to 1 for default units
   """""
   default = kwargs.get('default', 0.01)

   data_diff = np.abs(np.diff(data))
   power_ = 1

   increment_list ={
   'default': default,
   'dev': distribution(data_diff, power_, 'dev'),
   'tend': distribution(data_diff, power_, 'tend')[0],
   'min range': distribution(data_diff, power_, 'distr range')[0][0],
   'mean': np.abs(data_diff).mean(),
   'min': (np.abs(data_diff).min()),
   'min dev': np.abs(data_diff).min() + distribution(data_diff, power_, 'dev'),
   'max': np.abs(data_diff).max(),
   'div': np.abs(np.ptp(data))/len(data)
   }
   return increment_list[increment_type]

