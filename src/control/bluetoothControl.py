import bluetooth

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", bluetooth.PORT_ANY))
server_socket.listen(1)

print("Listening on Port 22")

client_socket, address = server_socket.accept()
print("Accepted connection from ", address)

while True:
    try:
        data = client_socket.recieve(1024)
        if len(data) == 0:
            break

        print("Recieved: %s" % data)

    except(KeyboardInterrupt, SystemExit):
        print("Closing socket")
        client_socket.close()
        server_socket.close()
        break
