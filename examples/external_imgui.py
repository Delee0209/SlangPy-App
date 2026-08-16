import slangpy as spy
from imgui_bundle import imgui
import os
import sys

app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.abspath(app_path))

from App import *

app = App(title = "external imgui", resizable = True, gui = True, use_imgui = True, debug = True)

# Hooking the imgui_layout function for extern imgui configuration
# how to use imgui... please see doc in imgui_bundle
def imgui_layout(app: App):
    imgui.show_demo_window()
app.imgui_layout = imgui_layout

app.run()