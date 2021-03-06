from typing import Dict
from typing import List

from OpenGL import GL
from abc import ABC
import glfw

from engine.graphics.sprite import Sprite
from engine.graphics.window import Window
from engine.graphics.skia_surface import SkiaSurface


class EngineInterface(ABC):
    def __init__(self):
        glfw.init()
        self.running = False

    def stop(self) -> None:
        pass

    def start(self) -> None:
        pass

    def update(self) -> bool:
        pass


class Engine(EngineInterface):
    def __init__(self):
        super(Engine, self).__init__()
        self.window = Window()
        self.surface = SkiaSurface(self.window)
        self.batches: Dict[int, List[Sprite]] = {}

    def start(self):
        self.running = True
        self.set_resize_callback(self.framebuffer_size_callback)

    def update(self) -> bool:
        self.running = True
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        self.surface.flush()
        glfw.swap_buffers(self.window.glfw_window)

        for layer in self.batches.keys():
            for sprite in self.batches[layer]:
                self.surface.surface.getCanvas().drawBitmap(sprite.image, sprite.position.x, sprite.position.y)

        self.batches = {}
        glfw.poll_events()

        if glfw.get_key(self.window.glfw_window, glfw.KEY_ESCAPE):
            self.running = False
        elif glfw.window_should_close(self.window.glfw_window):
            self.running = False

        return self.running

    def draw(self, layer: int, sprite: Sprite):
        if layer not in self.batches.keys():
            self.batches[layer] = []
        self.batches[layer].append(sprite)

    def set_resize_callback(self, callback):
        glfw.set_framebuffer_size_callback(self.window.glfw_window, callback)

    def set_key_callback(self, callback):
        glfw.set_key_callback(self.window.glfw_window, callback)

    def framebuffer_size_callback(self, window, width, height):
        GL.glViewport(0, 0, width, height)

    @property
    def window(self) -> Window:
        return self._window

    @window.setter
    def window(self, value: Window):
        self._window = value

    @property
    def surface(self) -> SkiaSurface:
        return self._surface

    @surface.setter
    def surface(self, value: SkiaSurface):
        self._surface = value


