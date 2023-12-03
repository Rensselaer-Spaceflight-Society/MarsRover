import bluetooth

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

while True:
    try:
        data = input()
        if len(data) == 0:
            break
        
        try:
            client_socket.send(data)
        except bluetooth.btcommon.BluetoothError as err:
            print("Bluetooth Error: {}".format(err))
            break

    except(KeyboardInterrupt, SystemExit):
        print("Closing socket")
        client_socket.close()
        break
