import numpy as np
import pandas as pd
import Forecast_Instance as fi
from Modules import DataMod
import matplotlib.pyplot as plt

path = r'EURAUD.ifx_M1_202402190000_202402191016.csv'
data = pd.read_csv(path, sep = '\t')['<CLOSE>'].dropna()
initial_val = data.iloc[-1] if isinstance(data, pd.Series) else data[-1]
region_size = (1/3)*np.ptp(data)
num_forecasts = 50
Forecast_iterations = 50

instance = fi.ForecastFunc(data, initial_val)
instance.MethodCalled(DataMod.posNegChange, tend_evaluation = False)
instance.BoundSplit(region_size, recursive_split = False)

Forecast = np.zeros((num_forecasts, Forecast_iterations))
for index1 in np.arange(num_forecasts):
  Forecast[index1, 0] = initial_val
  current_val = initial_val
  current_data = data
  for index2 in np.arange(1, Forecast_iterations):
    current_val += instance.GenerateChange(current_val)
    Forecast[index1, index2] = current_val

data_frame = pd.DataFrame(Forecast)

move_frame = data_frame.iloc[:, 1:]
moving_distr, movingDistr_count = move_frame.apply(DataMod.regionMap_pair, axis = 0, dev_type = 2, region_values = 'map distr', distr_return = 'conc range', return_type = (7,5)).values
moving_prob = movingDistr_count/move_frame.shape[0]
net_movingDistr = np.sum(movingDistr_count)/move_frame.size
moving_distr =  pd.DataFrame(moving_distr)
print(f'Moving distribution: {moving_distr}')
print(f'Count of moving distribution: {movingDistr_count}')
print(f'moving Probabilities is {(movingDistr_count/move_frame.shape[0])}')
print(f'Net moving prob distr is  {np.sum(movingDistr_count)/move_frame.size}')

# plt.plot(moving_distr, color = 'red')
# plt.plot(Forecast.T, color = 'grey')
# plt.show()
