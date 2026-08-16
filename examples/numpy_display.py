import slangpy as spy
import numpy as np
import os
import sys

app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.abspath(app_path))

from App import *

n = 800

app = App(title = "numpy display", width = n, height = n, resizable = False, vsync = True)

# initialize grid
grid = np.zeros((n, n), dtype = np.int8)
# display color setting
palette = np.array([[0, 0, 0, 1], [1, 1, 1, 1]], dtype=np.float32)

# initialize random number generator
rng = np.random.default_rng(seed=42)

# randomly set initial population
initial_population = int(n * n / 5)
for i in range(initial_population):
    x = int(rng.uniform(0.0, n) % n)
    y = int(rng.uniform(0.0, n) % n)
    grid[x, y] = 1

# game of life update function
def game_of_life(grid):
    neighbors = (
        np.roll(grid,  1, axis=0) + np.roll(grid, -1, axis=0) +
        np.roll(grid,  1, axis=1) + np.roll(grid, -1, axis=1) +
        np.roll(np.roll(grid,  1, axis=0),  1, axis=1) +
        np.roll(np.roll(grid,  1, axis=0), -1, axis=1) +
        np.roll(np.roll(grid, -1, axis=0),  1, axis=1) +
        np.roll(np.roll(grid, -1, axis=0), -1, axis=1)
    )
    return ((neighbors == 3) | ((grid == 1) & (neighbors == 2))).astype(int)

# main loop
while(app.process_event()):
    # display current iteration
    app.numpy_display(palette[grid])
    # game of life update
    grid = game_of_life(grid)
