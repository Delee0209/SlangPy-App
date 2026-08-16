from pathlib import Path
from typing import Callable, Optional, Union
import slangpy as spy
import slangpy.ui.imgui_bundle as imgui_helper
from imgui_bundle import imgui

class App:
    def __init__(self,
                 title: str = "App",
                 width: int = 800, height: int = 800,
                 resizable: bool = False, vsync: bool = True,
                 gui: bool = False, use_imgui: bool = False,
                 frame_format: spy.Format = spy.Format.rgba32_float, display_format: spy.Format = spy.Format.undefined,
                 include: list[Union[str, Path]] = [], debug: bool = True,
                 backend: spy.DeviceType = spy.DeviceType.automatic):
        super().__init__()
        # create device
        self.debug = debug
        self.device = spy.create_device(type = backend, include_paths = include, enable_debug_layers = debug)
        self.command_encoder: spy.CommandEncoder = None
        # create window
        self.width = width
        self.height = height
        self.window = spy.Window(width = width, height = height, title = title, resizable = resizable)
        # create surface
        self.vsync = vsync
        self.display_format = display_format
        self.surface = self.device.create_surface(self.window)
        self.surface.configure(width = width, height = height, vsync = vsync, format = self.display_format)
        # output frame image
        self.frame_format = frame_format
        self.frame: spy.Texture = None
        # viewport
        self.viewport = None
        # parameters
        self.mouse_pos = spy.float2()
        # events
        self.window.on_keyboard_event = self.on_keyboard_event
        self.window.on_mouse_event = self.on_mouse_event
        self.window.on_resize = self.on_resize
        # hookable external inputs
        self.external_keyboard_event: Optional[Callable[['App', spy.KeyboardEvent], None]] = None
        self.external_mouse_event: Optional[Callable[['App', spy.MouseEvent], None]] = None
        self.external_resize: Optional[Callable[['App'], None]] = None
        # hookable functions
        self.precompute: Optional[Callable[['App'], None]] = None
        self.preprocess: Optional[Callable[['App'], None]] = None
        self.render: Optional[Callable[['App'], None]] = None
        self.postprocess: Optional[Callable[['App'], None]] = None
        # hookable gui - using slangpy native gui interface
        self.gui = gui
        self.use_imgui = use_imgui
        self.ui: spy.ui.Context = None
        self.screen: spy.ui.Screen = None
        self.imgui = None
        if gui:
            self.ui = spy.ui.Context(self.device)
            self.screen = self.ui.screen
            # setup external imgui context if enable
            if use_imgui:
                self.imgui = imgui_helper.create_imgui_context(self.width, self.height)
                imgui.set_current_context(self.imgui)
                imgui.get_io().config_flags |= imgui.ConfigFlags_.docking_enable
        self.ui_layout: Optional[Callable[['App'], None]] = None
        self.ui_update: Optional[Callable[['App'], None]] = None
        self.imgui_layout: Optional[Callable[['App'], None]] = None

    def on_keyboard_event(self, event: spy.KeyboardEvent):
        # gui keyboard inputs
        if self.gui:
            if not self.use_imgui and self.ui.handle_keyboard_event(event):
                return
            elif self.use_imgui and imgui_helper.handle_keyboard_event(event):
                return
        # default keyboard inputs
        if event.is_key_press():
            if event.key == spy.KeyCode.escape:
                self.window.close()
                return
            elif event.key == spy.KeyCode.key1:
                if self.frame:
                    spy.tev.show_async(self.frame)
            elif event.key == spy.KeyCode.key2:
                if self.frame:
                    bitmap = self.frame.to_bitmap()
                    bitmap.convert(spy.Bitmap.PixelFormat.rgb,
                                   spy.Bitmap.ComponentType.uint8,
                                   srgb_gamma = True,).write_async("captured/screenshot.png")
        # external keyboard inputs
        if self.external_keyboard_event:
            self.external_keyboard_event(self, event)

    def on_mouse_event(self, event: spy.MouseEvent):
        # gui mouse inputs
        if self.gui:
            if not self.use_imgui and self.ui.handle_mouse_event(event):
                return
            elif self.use_imgui and imgui_helper.handle_mouse_event(event):
                return
        # default mouse inputs
        if event.type == spy.MouseEventType.move:
            self.mouse_pos = event.pos
        # external mouse inputs
        if self.external_mouse_event:
            self.external_mouse_event(self, event)

    def on_resize(self, width: int, height: int):
        self.device.wait()
        if width > 0 and height > 0:
            self.width = width
            self.height = height
            self.surface.configure(width = width, height = height, vsync = self.vsync)
        else:
            self.surface.unconfigure()
        # external resize operation
        if self.external_resize:
            self.external_resize(self)

    def process_event(self):
        if self.window.should_close():
            return False
        self.window.process_events()
        return True

    def configure_frame(self, width, height):
        # initialize or resize frame texture
        if (self.frame == None 
            or self.frame.width != width 
            or self.frame.height != height):
            self.frame = self.device.create_texture(format = self.frame_format,
                                                    width = width,
                                                    height = height,
                                                    mip_count = 1,
                                                    usage = spy.TextureUsage.shader_resource | spy.TextureUsage.unordered_access | spy.TextureUsage.render_target,
                                                    label = "frame",)
            self.command_encoder.clear_texture_float(self.frame, clear_value = spy.float4(0.0))
            self.viewport = spy.Viewport.from_size(self.frame.width, self.frame.height)

    def configure_gui(self, display):
        if self.gui:
            # current work around for the imgui viewport dimension problem...
            self.ui.begin_frame(display.width, display.height)
            if not self.use_imgui: # using native slangpy imgui wrapper
                self.ui.end_frame(display, self.command_encoder)
            elif self.use_imgui: # using external imgui for draw_data
                imgui_helper.begin_frame(display.width, display.height)
                if self.imgui_layout:
                    self.imgui_layout(self)
                imgui.render()
                imgui_draw_data = imgui.get_draw_data()
                imgui_helper.sync_draw_data_textures(self.device, self.ui, imgui_draw_data)
                imgui_helper.render_imgui_draw_data(self.ui, imgui_draw_data, display, self.command_encoder)
    
    def present(self):
        if not self.surface.config:
            return
        display = self.surface.acquire_next_image()
        if not display:
            return
        self.command_encoder.blit(display, self.frame)
        # self.command_encoder.set_texture_state(display, spy.ResourceState.present)
        self.configure_gui(display)
        self.device.submit_command_buffer(self.command_encoder.finish())
        del display
        self.surface.present()

    def run(self): # a skeleton main loop can be filled via hookable functions
        if self.gui and self.ui_layout:
            self.ui_layout(self)
        if self.precompute:
            self.precompute(self)
        while self.process_event():
            self.command_encoder = self.device.create_command_encoder()
            self.configure_frame(self.width, self.height)
            if self.gui and self.ui_update:
                self.ui_update(self)
            if self.preprocess:
                self.preprocess(self)
            if self.render:
                self.render(self)
            if self.postprocess:
                self.postprocess(self)
            self.present()

    def numpy_display(self, framebuffer): # directly display the framebuffer -> ndarray with shape(width, height, 4)
        self.command_encoder = self.device.create_command_encoder()
        self.configure_frame(framebuffer.shape[1], framebuffer.shape[0])
        self.frame.copy_from_numpy(framebuffer)
        self.present()

    def device(self):
        return self.device

    def frame_size(self):
        return spy.float2(self.width, self.height)
