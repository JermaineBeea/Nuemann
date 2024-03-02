import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np
import random

def sinerange(n, period, min_y, max_y):
    x = np.linspace(0, period, 1000)
    raw_y = np.sin(2*np.pi*n * (x / period))
    y = min_y + (max_y - min_y) * (raw_y + 1) / 2
    return x, y

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')

red_pos = 0.5
blue_pos = 0
red_ball_initial_position = (red_pos, red_pos)
blue_ball_initial_position = (blue_pos, blue_pos) 

red_ball = patches.Circle(red_ball_initial_position, 0.02, fill=True, color = 'red') 
ax.add_patch(red_ball)

blue_ball = patches.Circle(blue_ball_initial_position, 0.02, fill=True, color = 'blue')
ax.add_patch(blue_ball)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
jiggle_rate = 0.01
frames = 1000
interval = 200

def update(num):
  number = 6; period = 100; min_y = 4; max_y = 7
  current_jiggle_rate = jiggle_rate * sinerange(number, period, min_y, max_y)[1][num]

  red_ball_x, red_ball_y = red_ball.center
  increment = np.random.uniform(-current_jiggle_rate, current_jiggle_rate)
  new_red_ball_x, new_red_ball_y = sinerange(number, period, red_ball_x, increment)
  # new_red_ball_x, new_red_ball_y = np.random.uniform(0, 0.1, 10), np.random.uniform(0, 0.1, 10)
  new_red_ball_x = np.clip(new_red_ball_x[num % len(new_red_ball_x)], 0, 1)
  new_red_ball_y = np.clip(new_red_ball_y[num % len(new_red_ball_y)], 0, 1)
  red_ball.center = (new_red_ball_x, new_red_ball_y)

  blue_ball_x, blue_ball_y = blue_ball.center
  direction_x = new_red_ball_x - blue_ball_x
  direction_y = new_red_ball_y - blue_ball_y
  new_blue_ball_x = np.clip(blue_ball_x + direction_x * current_jiggle_rate, 0, 1)
  new_blue_ball_y = np.clip(blue_ball_y + direction_y * current_jiggle_rate, 0, 1)
  blue_ball.center = (new_blue_ball_x, new_blue_ball_y)

  return red_ball, blue_ball,

ani = animation.FuncAnimation(fig, update, frames = frames, interval = interval, repeat=True)

plt.show()