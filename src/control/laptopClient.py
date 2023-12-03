import bluetooth

client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
bluetooth_address = input("Enter the bluetooth address of the rover: ").strip()
port = 1

client_socket.connect((bluetooth_address, port))

while True:
    try:
        data = input()
        if len(data) == 0:
            break

        client_socket.send(data)

    except(KeyboardInterrupt, SystemExit):
        print("Closing socket")
        client_socket.close()
        break
