# path: src/control/laptopClient.py

import bluetooth
import tkinter as tk
import command

client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# list bluetooth devices
print("Searching for devices... this may take a while")
devices = bluetooth.discover_devices()
for i, device in enumerate(devices):
    print(i+1, bluetooth.lookup_name(device), device)

# connect to device
device = int(input("Select device: "))
bluetooth_address = devices[device-1]
port = 1

client_socket.connect((bluetooth_address, port))

def dataSmartSend(client_socket, command: command.Command) -> bool:
    try:
        client_socket.send(str(command).encode("utf-8"))
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

        forwardCommand = command.Command("forward", "5")
        backwardCommand = command.Command("backward", "5")
        leftCommand = command.Command("left", "5")
        rightCommand = command.Command("right", "5")

        # add 4 buttons to the window
        forward = tk.Button(window, text="Forward", command=lambda: dataSmartSend(client_socket, forwardCommand))
        forward.pack(side=tk.TOP)
        left = tk.Button(window, text="Left", command=lambda: dataSmartSend(client_socket, leftCommand))
        left.pack(side=tk.LEFT)
        right = tk.Button(window, text="Right", command=lambda: dataSmartSend(client_socket, rightCommand))
        right.pack(side=tk.RIGHT)
        backward = tk.Button(window, text="Backward", command=lambda: dataSmartSend(client_socket, backwardCommand))
        backward.pack(side=tk.BOTTOM)
        commandInput = tk.Text(window, height=1, width=10)
        commandInput.pack(side=tk.BOTTOM)
        commandSend = tk.Button(window, text="Send", command=lambda: dataSmartSend(client_socket, command.Command(commandInput.get(1.0, "end-1c"))))
        commandSend.pack(side=tk.BOTTOM)

        window.mainloop()

        # close the socket when the window is closed
        client_socket.close()
        break

    except(KeyboardInterrupt, SystemExit):
        print("Closing socket")
        client_socket.close()
        break



