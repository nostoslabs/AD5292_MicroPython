from ad5292 import AD5292
# Example usage:
pot = AD5292(1, 5)  # SPI bus 1, CS pin 5
pot.set_wiper_position(512)  # Set wiper position to mid-range
control_reg_value = pot.read_control_register()
print("Control Register:", control_reg_value)
pot.write_control_register(3)  # Write a new value to the control register
pot.close()
