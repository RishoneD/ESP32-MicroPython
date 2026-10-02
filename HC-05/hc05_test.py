from machine import UART, Pin
import time

bluetooth = UART(1, baudrate=9600, tx=17, rx=16)

while True:
    # אם התקבלו נתונים מה-HC05
    if bluetooth.any():
        data = bluetooth.read()
        if data:
            try:
                print(data.decode().strip())
            except UnicodeError:
                print("Received (raw):", data)

    # בדיקה אם קלט הגיע מה-REPL (אפשרות למחשב)
    try:
        user_input = input("Send to Bluetooth: ")
        bluetooth.write(user_input + '\n')
    except Exception as e:
        print("Error:", e)

    time.sleep(0.1)
