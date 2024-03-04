import numpy as np
import pandas as pd
import Forecast_Instance as fi
from Modules import DataMod
import matplotlib.pyplot as plt

path = r'EURAUD.ifx_M1_202402190000_202402191016.csv'
data = pd.read_csv(path, sep = '\t')['<CLOSE>'].dropna()
data_size = data.size
initial_val = data.iloc[-1] if isinstance(data, pd.Series) else data[-1]
region_size = (1/3)*np.ptp(data)
num_forecasts = 300
Forecast_iterations = data_size//3

instance = fi.ForecastFunc(data, initial_val)
instance.MethodCalled(tend_evaluation = False, dev_type = 2)
# instance.BoundSplit(region_size, recursive_split = True)
instance.UniformSplit(region_size, recursive_split = True)

Forecast = np.zeros((num_forecasts, Forecast_iterations))
for index1 in np.arange(num_forecasts):
  Forecast[index1, 0] = initial_val
  current_val = initial_val
  current_data = data
  for index2 in np.arange(1, Forecast_iterations):
    current_val += instance.GenerateChange(current_val)
    Forecast[index1, index2] = current_val

data_frame = pd.DataFrame(Forecast)
moving_distr = data_frame.apply(DataMod.blitzDistr, axis = 0, dev_type = 2, return_type = 'conc range')
result = data_frame.apply(DataMod.regionMap_pair, axis = 0, dev_type = 2, region_values = 'map distr', distr_return = 'conc range', return_type = (5))
movingDistr_count = result.to_numpy()[1:]
moving_prob = movingDistr_count/data_frame.shape[0]
net_movingDistr = np.sum(movingDistr_count)/(data_frame.size - data_frame.shape[0])
max_movingDistr = moving_distr.max().max()
min_movingDistr = moving_distr.min().min()

from_ = data_size; to_ = from_ + Forecast_iterations
x_range = np.arange(from_, to_)
color_1 = 'red'
plt.title(f'Moving distrbution probability is  {np.floor(net_movingDistr*100)}%')
plt.axhline(y = max_movingDistr, color = color_1, linestyle = '--', alpha = 0.5, label = f'Max Moving Distribution {max_movingDistr}')
plt.axhline(y = min_movingDistr, color = color_1, linestyle = '--', alpha = 0.5, label = f'Min Moving Distribution {min_movingDistr}')
plt.plot(data, color = 'orange', label = 'Data')
plt.plot(x_range, Forecast.T, linestyle = '--',color = 'grey', linewidth = 0.4, alpha = 0.2)
plt.plot(x_range, moving_distr.T, color = color_1, label = 'Moving Distribution')
# plt.plot(moving_prob, color = 'blue')
plt.legend()
plt.show()
