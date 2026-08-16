import slangpy as spy
import numpy as np
import os
import sys

app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.abspath(app_path))

from App import *

app = App(title = "compute display", resizable = True, vsync = True)

# load and compile the slang shader
device = app.device
program = device.load_program("examples/compute_display.slang", ["main"])
kernel = device.create_compute_kernel(program = program)

timer = spy.Timer()

# Hooking the render function
def render(app: App):
    time = timer.elapsed_s()
    frame = app.frame
    kernel.dispatch(thread_count = [frame.width, frame.height, 1], time = time, frame = frame)
app.render = render

app.run()