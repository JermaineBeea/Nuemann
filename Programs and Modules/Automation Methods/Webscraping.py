import sys
import os
import numpy as np 

# Import the DataMod module from the Modules package
from Modules import  DataMod

data = np.arange(10)
initial_value = data[-1]

# Calculate the size of the absolute boundary as a third of the peak-to-peak distance in the data
boundAbs_size = (1/3)*np.ptp(data)

# Calculate the upper and lower bounds
upper_bound = initial_value + ((np.max(data) - initial_value)/np.ptp(data))*boundAbs_size
lower_bound = initial_value + ((np.min(data) - initial_value)/np.ptp(data))*boundAbs_size

# Define a function to check if a value is within the bounds
arg_func = lambda x: (x >= lower_bound) & (x <= upper_bound)

# Filter the data using the arg_func function
filterdData = DataMod.filterPair(data, order = 0, filterFunc = arg_func)

# Calculate the differences between consecutive elements in the filtered data
differences = DataMod.diffFunction(filterdData)

# Define the deviation type and output type for the blitzDistr function
devType = 2
output = 'distr'

# Define whether to evaluate the trend in the blitzDistr function
evaluate_tend = False

# Calculate the blitz distribution of the differences
distr = DataMod.blitzDistr(differences, devType, output, evaluate_tend)

# Calculate the probability distribution of the blitz distribution
prob = DataMod.probDistr(distr, differences)