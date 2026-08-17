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
    window = spy.ui.Window(app.screen, "Slangpy Native GUI", size=spy.float2(700, 700))
    spy.ui.Text(parent = window, text = "demo window")
    last_input = spy.ui.Text(parent = window, text = "Last input --- None")

    def callback(input):
        global output
        last_input.text = "Last input --- " + str(input)
        
    # drag ui widgets
    drag_group = spy.ui.Group(parent = window, label = "drag widgets")
    drag_int_group = spy.ui.Group(parent = drag_group, label = "int")
    drag_int = spy.ui.DragInt(parent = drag_int_group, label = "drag int", callback = callback, min = 0, max = 1024)
    drag_int2 = spy.ui.DragInt2(parent = drag_int_group, label = "drag int2", callback = callback, min = 0, max = 1024)
    drag_int3 = spy.ui.DragInt3(parent = drag_int_group, label = "drag int3", callback = callback, min = 0, max = 1024)
    drag_int4 = spy.ui.DragInt4(parent = drag_int_group, label = "drag int4", callback = callback, min = 0, max = 1024)
    drag_float_group = spy.ui.Group(parent = drag_group, label = "float")
    drag_float = spy.ui.DragFloat(parent = drag_float_group, label = "drag float", callback = callback, speed = 0.05, min = 0, max = 1024)
    drag_float2 = spy.ui.DragFloat2(parent = drag_float_group, label = "drag float2", callback = callback, speed = 0.05, min = 0, max = 1024)
    drag_float3 = spy.ui.DragFloat3(parent = drag_float_group, label = "drag float3", callback = callback, speed = 0.05, min = 0, max = 1024)
    drag_float4 = spy.ui.DragFloat4(parent = drag_float_group, label = "drag float4", callback = callback, speed = 0.05, min = 0, max = 1024)
    # slider ui widgets
    slider_group = spy.ui.Group(parent = window, label = "slider widgets")
    slider_int_group = spy.ui.Group(parent = slider_group, label = "int")
    slider_int = spy.ui.SliderInt(parent = slider_int_group, label = "slider int", callback = callback, min = 0, max = 4)
    slider_int2 = spy.ui.SliderInt2(parent = slider_int_group, label = "slider int2", callback = callback, min = 0, max = 4)
    slider_int3 = spy.ui.SliderInt3(parent = slider_int_group, label = "slider int3", callback = callback, min = 0, max = 4)
    slider_int4 = spy.ui.SliderInt4(parent = slider_int_group, label = "slider int4", callback = callback, min = 0, max = 4)
    slider_float_group = spy.ui.Group(parent = slider_group, label = "float")
    slider_float = spy.ui.SliderFloat(parent = slider_float_group, label = "slider float", callback = callback, min = 0, max = 4)
    slider_float2 = spy.ui.SliderFloat2(parent = slider_float_group, label = "slider float2", callback = callback, min = 0, max = 4)
    slider_float3 = spy.ui.SliderFloat3(parent = slider_float_group, label = "slider float3", callback = callback, min = 0, max = 4)
    slider_float4 = spy.ui.SliderFloat4(parent = slider_float_group, label = "slider float4", callback = callback, min = 0, max = 4)
    # input widgets
    input_group = spy.ui.Group(parent = window, label = "input widgets")
    input_int_group = spy.ui.Group(parent = input_group, label = "int")
    input_int = spy.ui.InputInt(parent = input_int_group, label = "input int", callback = callback)
    input_int2 = spy.ui.InputInt2(parent = input_int_group, label = "input int2", callback = callback)
    input_int3 = spy.ui.InputInt3(parent = input_int_group, label = "input int3", callback = callback)
    input_int4 = spy.ui.InputInt4(parent = input_int_group, label = "input int4", callback = callback)
    input_float_group = spy.ui.Group(parent = input_group, label = "float")
    input_float = spy.ui.InputFloat(parent = input_float_group, label = "input float", callback = callback)
    input_float2 = spy.ui.InputFloat2(parent = input_float_group, label = "input float2", callback = callback)
    input_float3 = spy.ui.InputFloat3(parent = input_float_group, label = "input float3", callback = callback)
    input_float4 = spy.ui.InputFloat4(parent = input_float_group, label = "input float4", callback = callback)
    input_text_group = spy.ui.Group(parent = input_group, label = "text")
    input_text = spy.ui.InputText(parent = input_text_group, label = "input text", value = '', callback = callback)
    # Others widgets
    other_group = spy.ui.Group(parent = window, label = "other widgets")
    check_box = spy.ui.CheckBox(parent = other_group, label = "check box", callback = callback)
    combo_box = spy.ui.ComboBox(parent = other_group, label = "combo box", items = ["combo item 1", "combo item 2", "combo item 3"], callback = callback)
    list_box = spy.ui.ListBox(parent = other_group, label = "list box", items = ["list item 1", "list item 2", "list item 3"], callback = callback)
app.ui_layout = ui_layout

app.run()
