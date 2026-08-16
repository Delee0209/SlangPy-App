import slangpy as spy
import numpy as np
import os
import sys

app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.abspath(app_path))

from App import *

n = 250

app = App(title = "numpy display", width = n, height = n, resizable = False, vsync = True)

# initialize grid
grid0 = np.zeros((n, n, 4), dtype = np.float32)
grid0[:, :, 3] = 1.0
grid1 = np.zeros((n, n, 4), dtype = np.float32)
grid1[:, :, 3] = 1.0

# initialize random number generator
rng = np.random.default_rng(seed=42)

def set(storage, x, y, val):
    storage[x][y][0] = val
    storage[x][y][1] = val
    storage[x][y][2] = val

# randomly set initial population
initial_population = int(n * n / 5)
for i in range(initial_population):
    x = int(rng.uniform(0.0, n) % n)
    y = int(rng.uniform(0.0, n) % n)
    set(grid0, x, y, 1)

def game_of_life(in_grid, out_grid):
    for i in range(n):
        for j in range(n):
            set(out_grid, i, j, in_grid[i, j, 0])
            total = int(in_grid[i, (j - 1) % n, 0] +
                        in_grid[i, (j + 1) % n, 0] +
                        in_grid[(i - 1) % n, j, 0] + 
                        in_grid[(i + 1) % n, j, 0] + 
                        in_grid[(i - 1) % n, (j - 1) % n, 0] + 
                        in_grid[(i - 1) % n, (j + 1) % n, 0] + 
                        in_grid[(i + 1) % n, (j - 1) % n, 0] + 
                        in_grid[(i + 1) % n, (j + 1) % n, 0])
            if in_grid[i, j, 0] == 1:
                if total < 2 or total > 3:
                    set(out_grid, i, j, 0)
            else:
                if total == 3:
                    set(out_grid, i, j, 1)

iteration = 0
while(app.process_event()):
    # game of life update
    in_grid = grid0 if iteration % 2 == 0 else grid1
    out_grid = grid1 if iteration % 2 == 0 else grid0
    # display current iteration
    app.numpy_display(in_grid)
    # game of life update
    game_of_life(in_grid, out_grid)
    iteration += 1
