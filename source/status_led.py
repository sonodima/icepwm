import time
import neopixel
import board


class StatusLED:
    _np: neopixel.NeoPixel
    _swap_rg: bool

    def __init__(self, *, pin: board.Pin, swap_rg: bool = False):
        self._np = neopixel.NeoPixel(pin, n=1, brightness=0.1, auto_write=True)
        self._swap_rg = swap_rg

    def on(self, *, color):
        if self._swap_rg:
            color = (color[1], color[0], color[2])
        self._np.fill(color)

    def off(self):
        self._np.fill((0, 0, 0))

    def blink(self, *, color, times: int = 1, dt: float = 0.1):
        for i in range(times):
            self.on(color=color)
            time.sleep(dt / 2)
            self.off()
            time.sleep(dt / 2)
