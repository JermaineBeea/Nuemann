import numpy as np
import random as random

def sinerange(n, period, min_y, max_y):
    x = np.linspace(0, period, 1000)
    raw_y = np.sin(2*np.pi*n * (x / period))
    y = min_y + (max_y - min_y) * (raw_y + 1) / 2
    return x, y

def sinepoint(n, period, point, increment):
    x = np.linspace(0, period, 1000)
    y = point + increment * np.sin(n * 2 * np.pi * x / period)
    return x, y

def random_func(prob, posval, negval):
  return posval if random.random() <= prob else negval

if __name__ == '__main__':
    
    data = [(1,0), (4,3), (3,5), (6,5)]

