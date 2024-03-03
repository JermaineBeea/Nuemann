import numpy as np
import pandas as pd
import ForecastModule as fm
import DataModification as DataMod
import matplotlib.pyplot as plt

path = r'EURAUD.ifx_M1_202402190000_202402191016.csv'
data = pd.read_csv(path, sep = '\t')['<CLOSE>'].dropna()
initial_val = data.iloc[-1] if isinstance(data, pd.Series) else data[-1]
region_size = (1/3)*np.ptp(data)
num_forecasts = 10
Forecast_iterations = 10

instance = fm.ForecastFunc(data, initial_val)
instance.MethodCalled(DataMod.regionChange, tend_evaluation = False)
instance.UniformSplit(region_size, recursive_split = True)
instance.BoundSplit(region_size, recursive_split = False)

Forecast = np.zeros((num_forecasts, Forecast_iterations))
for index1 in np.arange(num_forecasts):
  Forecast[index1, 0] = initial_val
  current_val = initial_val
  current_data = data
  for index2 in np.arange(1, Forecast_iterations):
    current_val += instance.GenerateChange(current_val)
    Forecast[index1, index2] = current_val

frame = pd.DataFrame(Forecast)
plt.plot(Forecast.T, color = 'grey')
plt.show()
