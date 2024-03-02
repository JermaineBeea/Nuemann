import numpy as np
import random as random
import matplotlib.pyplot as plt

def sinerange(n, period, min_y, max_y):
    x = np.linspace(0, period, 1000)
    raw_y = np.sin(2*np.pi*n * (x / period))
    y = min_y + (max_y - min_y) * (raw_y + 1) / 2
    return x, y

def sinepoint(n, period, point, increment):
    x = np.linspace(0, period, 1000)
    y = point + increment * np.sin(n * 2 * np.pi * x / period)
    return x, y

if __name__ == '__main__':

    number = 6; period = 2; min_y = 0; max_y = 1
    x, y = sinerange(number, period, min_y, max_y)
    
    plt.plot(x, y)
    plt.show()
