import sys
import os
sys.path.append("..")
sysPath = os.getcwd()
import numpy as np 
import pandas as pd
import logging as log

from Defined import  DataMod

data = np.arange(10)
initial_value = data[-1]
print(f'Data size is {data.size} ({data.min()},{data.max()})')

boundAbs_size = (1/3)*np.ptp(data)
upper_bound = initial_value + ((np.max(data) - initial_value)/np.ptp(data))*boundAbs_size
lower_bound = initial_value + ((np.min(data) - initial_value)/np.ptp(data))*boundAbs_size
print(f'initial value {initial_value}, lower bound:{lower_bound}, upper bound:{upper_bound}')

arg_func = lambda x: (x >= lower_bound) & (x <= upper_bound)
filterdData = DataMod.filterPair(data, order = 0, filterFunc = arg_func)
print(f'Filterd data size: {filterdData.shape[0]}, proportion {np.round(filterdData.shape[0]/data.size, 2)}')

differences = DataMod.diffFunction(filterdData)

devType = 2
output = 'distr'
evaluate_tend = False

distr = DataMod.blitzDistr(differences, devType, output, evaluate_tend)
prob = DataMod.probDistr(distr, differences)
print(f'distr {distr}')
print(f'Prob {prob}')  
print('\n')

