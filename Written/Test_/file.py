import sys
sys.path.append("..")
sys.path.insert(0, 'C:/Users/tebne/OneDrive/Programming/Written/')

import matplotlib.pyplot as plt
import pandas as pd
import cProfile
from Read_csv import readcsv
import numpy as np

raw_data = readcsv(r'C:\Users\tebne\OneDrive\Programming\Python\Written\Data\EURUSD.ifx_M2_0205.csv')

def difference(data,*arguments):
  diff = np.diff(data, n = 1)
  pos, neg = [], []
  for val in diff:
    if val > 0:
      pos.append(val)
    elif val < 0:
      neg.append(val)
  length = len(pos) + len(neg)
  differences = lambda: pos + neg
  posprob = lambda: len(pos)/length
  negprob = lambda: (1- posprob())

  return [{0:differences(), 1:pos, -1:neg, 'pos':posprob(), 'neg':negprob()}[arg] for arg in [*arguments]]


cProfile.run('difference(raw_data, 1, -1, "pos")')



