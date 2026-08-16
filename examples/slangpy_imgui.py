import slangpy as spy
import os
import sys

app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.abspath(app_path))

from App import *

app = App(title = "slangpy native gui", resizable = True, gui = True, debug = True)

# Hooking the ui_layout function for configuring the native slangpy imgui
# for more slangpy imgui please refer to the slangpy API reference
def ui_layout(app: App):
    window = spy.ui.Window(app.screen, "Slangpy Native GUI", size=spy.float2(520, 230))
    drag_int = spy.ui.DragInt(parent = window, label = "drag_int", min = 1, max = 1024)
app.ui_layout = ui_layout

app.run()