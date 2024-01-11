from machine import Pin, SPI
import time

class AD5292:
    def __init__(self, spi_bus, cs_pin, spi_freq=50000):
        self.cs = Pin(cs_pin, Pin.OUT)
        self.cs.value(1)  # Chip select is active low
        self.spi = SPI(spi_bus, baudrate=spi_freq, polarity=0, phase=1)
        self.spi.init(baudrate=spi_freq, polarity=0, phase=1)

    def set_wiper_position(self, position):
        if position > 1023:
            return False  # Invalid position value
        command = (0x01 << 10) | (position & 0x03FF)
        self._send_command(command)
        time.sleep_ms(6)
        return True  # Successful operation

    def _send_command(self, command):
        self.cs.value(0)
        self.spi.write(bytearray([(command >> 8) & 0xFF, command & 0xFF]))
        self.cs.value(1)

    def read_control_register(self):
        command = (0x02 << 10)  # Assuming this is the correct command for reading the control register
        self._send_command(command)
        # Read response from the device
        response = bytearray(2)
        self.cs.value(0)
        self.spi.readinto(response)
        self.cs.value(1)
        return response[1]  # Assuming the control register value is in the LSB

    def write_control_register(self, value):
        if value > 7:
            return False  # Invalid control register value
        command = (0x03 << 10) | (value & 0x07)  # Assuming this is the correct command for writing the control register
        self._send_command(command)
        return True

    def close(self):
        self.spi.deinit()


