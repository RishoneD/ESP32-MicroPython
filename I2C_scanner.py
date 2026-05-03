from machine import I2C, Pin
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

print('Scanning I2C bus...')
devices = i2c.scan()

if len(devices) == 0:
    print("No I2C device detected.")
else:
    print('No. of I2C devices found:',len(devices))
    for device in devices:  
        print("Decimal address: ",device," | Hexa address: ",hex(device))
