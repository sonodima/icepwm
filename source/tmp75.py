import busio


class TMP75:
    _i2c: busio.I2C
    _address: int

    def __init__(self, *, i2c: busio.I2C, address: int = 0x48):
        self._i2c = i2c
        self._address = address

    def read_temp(self) -> float:
        if not self._i2c.try_lock():
            raise RuntimeError("Failed to lock I2C interface")

        buffer = bytearray(2)
        try:
            self._i2c.readfrom_into(self._address, buffer)
        except Exception as e:
            self._i2c.unlock()
            raise e

        temp = buffer[0] << 8 | buffer[1]
        temp >>= 4
        if temp & 0x800:
            temp -= 0x1000

        self._i2c.unlock()
        return temp * 0.0625
