# IcePWM

## Hardware

Out of the box, IcePWM is configured to work with the **waveshare-rp2040-tiny** board and
a **TMP75** temperature sensor connected to the I2C bus.

You can change the pins used by the various peripherals to get it working with other boards.

## Usage

- Copy the contents of the `source` folder to **CircuitPython** volume mounted by the board.
- Edit the `code.py` file to change the configuration.
- Use `circup` to install the `neopixel` library.
