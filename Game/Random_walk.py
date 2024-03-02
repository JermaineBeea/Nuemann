import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np

def sinerange(n, period, min_y, max_y):
    x = np.linspace(0, period, 1000)
    raw_y = np.sin(2*np.pi*n * (x / period))
    y = min_y + (max_y - min_y) * (raw_y + 1) / 2
    return x, y

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')

circle = patches.Circle((0.5, 0.5), 0.05, fill=True, color = 'red') 
ax.add_patch(circle)

n = 10
dots = [patches.Circle((np.random.rand(), np.random.rand()), 0.01, fill=True, color = 'red') for _ in range(n)]
for dot in dots:
  ax.add_patch(dot)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
jiggle_rate = 0.01
frames = 1000
interval = 20

def update(num):
  number = 10; period = 500; min_y = -2; max_y = 2
  current_jiggle_rate = jiggle_rate * sinerange(number, period, min_y, max_y)[1][num]

  for dot in dots:
    current_x, current_y = dot.center
    new_x = np.clip(current_x + np.random.uniform(-current_jiggle_rate, current_jiggle_rate), 0, 1)
    new_y = np.clip(current_y + np.random.uniform(-current_jiggle_rate, current_jiggle_rate), 0, 1)
    dot.center = (new_x, new_y)
  
  circle_x, circle_y = circle.center
  new_circle_x = np.clip(circle_x + np.random.uniform(-current_jiggle_rate, current_jiggle_rate), 0, 1)
  new_circle_y = np.clip(circle_y + np.random.uniform(-current_jiggle_rate, current_jiggle_rate), 0, 1)
  circle.center = (new_circle_x, new_circle_y)

  return dots, circle,
ani = animation.FuncAnimation(fig, update, frames = frames, interval = interval, repeat=True)

plt.show()