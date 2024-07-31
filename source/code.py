import time
import board
import busio

from fan_curve import Point, Curve
from pwm_fan import PWMFan
from status_led import StatusLED
from tmp75 import TMP75


def main_routine():
    print("\n    IcePWM - Simple fan-temperature controller\n")

    curve_points: list[Point] = [
        Point(temp=35.0, speed=0.0),
        Point(temp=40.0, speed=0.1),
        Point(temp=55.0, speed=0.5),
        Point(temp=65.0, speed=1.0),
    ]

    led: StatusLED | None = None
    curve: Curve
    tmp75: TMP75
    fan: PWMFan

    try:
        led = StatusLED(pin=board.NEOPIXEL, swap_rg=True)
        curve = Curve(points=curve_points)
        tmp75 = TMP75(i2c=busio.I2C(board.GP1, board.GP0))
        fan = PWMFan(pin=board.GP6)
    except Exception as e:
        print(f"[x] Fatal: {e}")
        if led is not None:
            led.on(color=(255, 0, 0))
        while True:
            time.sleep(1000.0)

    while True:
        try:
            temp = tmp75.read_temp()
            speed = curve.get_speed(temp=temp)
            fan.set_speed(speed)

            print(f"[>] Iteration: temp={temp}, speed={speed}")
            led.blink(color=(20, 180, 230))
            time.sleep(1.0)

        except Exception as e:
            print(f"[!] Error: {e}")
            led.blink(color=(230, 200, 50), times=8)
            time.sleep(2.0)


if __name__ == "__main__":
    main_routine()
