import network
import uasyncio as asyncio
from machine import Pin, reset
from time import ticks_ms, sleep
import wifi_config

def connect2wifi(ssid='', password=''):
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    for net in wifi_config.WIFI_NETWORKS:
        ssid = net["ssid"]
        password = net["password"]

        print("Trying Wi-Fi:", ssid)
        wlan.connect(ssid, password)

        start_time = ticks_ms()
        while not wlan.isconnected(): # wait for Wi-Fi connection
            if ticks_ms() - start_time > 10000:  # 10 seconds timeout for each network
                break
        if wlan.isconnected(): # if connection is successful
            print("Connected to:", ssid)
            return wlan.ifconfig()[0]

    print("No Wi-Fi connection")
    return "NA"


async def process_sensors(): #TODO sensors processes
    global data1, data2 #Define relevent parameters as global
    while True:
#         print("[Sensors] Updating sensors data...")
        await asyncio.sleep(1)


async def process_devices(): #TODO devices processes
    while True:
#         print("[Devices] Controlling devices...")
        await asyncio.sleep(1)


def load_html():
    # Uses global datas updated by sensors tasks
    try:
        with open('webpage.html', 'r') as file:
            html = file.read()
        # Insert parameters into html
        html = html.replace('{{data1}}', str(data1))
        html = html.replace('{{data2}}', str(data2))
        return str(html)
    except Exception as e:
        print("שגיאה בטעינת הקובץ:", e)
        error_page = """<!DOCTYPE html>
<html>
<head><title>שגיאה</title></head>
<body>
  <h1>שגיאה בטעינת הדף</h1>
  <p>לא ניתן לקרוא את קובץ ה-HTML</p>
</body>
</html>
"""
        return str(error_page)


async def handle_client(reader, writer):
    try:
        request = await reader.read(1024)
        request = request.decode()
        print("Request:", request[:30])
        
        parts = request.split()
        print("", parts[1])
        
        if parts[1] == "/test1": #TODO update URL action accordingly
            # Run appropriate actions/functions
            print("received test1 action")
            global data1
            data1 = parts[1]

        response = load_html()

        writer.write("HTTP/1.1 200 OK\r\n")
        writer.write("Content-Type: text/html\r\n")
        writer.write("Connection: close\r\n\r\n")
        writer.write(response)

        await writer.drain()

    except Exception as e:
        print("Client error:", e)

    finally:
        await writer.wait_closed()


async def process_server():
    server = await asyncio.start_server(handle_client,"0.0.0.0",80)

    print("Server running...")

    while True:
        await asyncio.sleep(1)


async def main():
    ip = connect2wifi()
    print('IP address:', ip)
    if ip == "NA":
        print("No Wi-Fi connection, resetting...")
        reset()
        
    await asyncio.gather(
        process_sensors(), # Update sensors data
        process_devices(), # Update devices
        process_server() # Update server tasks
    )
        
    await asyncio.sleep(0.5)

# setup

#TODO Pin assignments
#TODO global parameters/flags assignments
#TODO parameters from sensors, etc.
data1 = "hello"
data2 = 123
# ==========================

#loop
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Ctrl-C pressed.. exiting')
    #TODO reset outputs
    reset()