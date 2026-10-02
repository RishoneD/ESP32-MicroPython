from machine import UART, Timer

bluetooth = UART(1, baudrate=9600, tx=17, rx=16)

# פונקציה שנקראת אוטומטית כל 100 מילי-שניות
def check_bluetooth(timer):
    if bluetooth.any():
        data = bluetooth.read()
        try:
            print("\nהתקבל:", data.decode().strip())
        except UnicodeError:
            print("\nהתקבל (גולמי):", data)

# הפעלת הטיימר
timer = Timer(0)
timer.init(period=100, mode=Timer.PERIODIC, callback=check_bluetooth)

# התוכנית הראשית: שליחה מהמקלדת
while True:
    text = input("שלחו ל-Bluetooth: ")
    bluetooth.write(text + '\n')