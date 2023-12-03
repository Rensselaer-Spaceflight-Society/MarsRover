# path: src/control/laptopClient.py

import bluetooth
import tkinter as tk

client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# list bluetooth devices
devices = bluetooth.discover_devices()
for i, device in enumerate(devices):
    print(i+1, bluetooth.lookup_name(device), device)

# connect to device
device = int(input("Select device: "))
bluetooth_address = devices[device-1]
port = 1

client_socket.connect((bluetooth_address, port))

def dataSmartSend(client_socket, data) -> bool:
    try:
        client_socket.send(data)
        return True
    except bluetooth.btcommon.BluetoothError as err:
        print("Bluetooth Error: {}".format(err))
        return False

while True:
    try:
        # tk window to send actions for the rover
        window = tk.Tk()
        window.title("Rover Control")
        window.geometry("200x200")
        window.configure(background="grey")

        # add 4 buttons to the window
        forward = tk.Button(window, text="Forward", command=lambda: dataSmartSend(client_socket, "F"))
        forward.pack(side=tk.TOP)
        left = tk.Button(window, text="Left", command=lambda: dataSmartSend(client_socket, "L"))
        left.pack(side=tk.LEFT)
        right = tk.Button(window, text="Right", command=lambda: dataSmartSend(client_socket, "R"))
        right.pack(side=tk.RIGHT)
        backward = tk.Button(window, text="Backward", command=lambda: dataSmartSend(client_socket, "B"))
        backward.pack(side=tk.BOTTOM)

        window.mainloop()

        # close the socket when the window is closed
        client_socket.close()
        break

    except(KeyboardInterrupt, SystemExit):
        print("Closing socket")
        client_socket.close()
        break



