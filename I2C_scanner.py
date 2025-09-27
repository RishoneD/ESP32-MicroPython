import machine
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))

print('Scanning I2C bus...')
devices = i2c.scan()

if len(devices) == 0:
    print("No I2C device !")
else:
    print('I2C devices found:',len(devices))

    for device in devices:  
        print("Decimal address: ",device," | Hexa address: ",hex(device))