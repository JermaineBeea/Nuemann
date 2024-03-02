
import numpy as np
import pandas as pd
import logging as log
import random
from IPython.display import display

data = np.arange(13)
increment = 3
for index in np.arange(data.size):
  sub_data = data[index: index + increment] 
  print(sub_data)

import numpy as np

data = np.arange(13)
increment = 3

sub_data = np.lib.stride_tricks.sliding_window_view(data, window_shape=increment)

for sub in sub_data:
  print(sub)