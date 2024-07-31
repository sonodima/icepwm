import board
import pwmio


class PWMFan:
    _out: pwmio.PWMOut

    def __init__(self, *, pin: board.Pin):
        self._out = pwmio.PWMOut(pin, frequency=25_000)

    def set_speed(self, value: float):
        value = max(0.0, min(1.0, value))
        self._out.duty_cycle = int(65_535 * value)

    def get_speed(self) -> float:
        return self._out.duty_cycle / 65_535
