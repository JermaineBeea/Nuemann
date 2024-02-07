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

def Array_diffFunc(data,*arguments):
    pos = []; neg = []
    for val in data:
      diff = np.diff(val, n=1)[0]
      pos.append(diff) if diff > 0 else neg.append(diff) if diff < 0 else None
    
    differences = lambda: pos + neg
    posprob = lambda: len(pos)/len(differences())
    negprob = lambda: (1- posprob())

    try:
      return [{0:differences(), 1:pos, -1:neg, 'pos':posprob(), 'neg':negprob()}[arg] for arg in [*arguments]]
    except KeyError:
      return 'Error: output argument must be an integer or between -1 and 1'

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

def random_func(prob, posval, negval):
  return posval if random.random() <= prob else negval


if __name__ == '__main__':
    
    data = [(1,0), (4,3), (3,5), (6,5)]

    result = Array_diffFunc(data, -1, 1, 0)
    print(result)