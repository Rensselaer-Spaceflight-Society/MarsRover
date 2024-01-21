import bluetooth
import command 

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", bluetooth.PORT_ANY))
server_socket.listen(1)

print("Listening on Port %d" % server_socket.getsockname()[1])

client_socket, address = server_socket.accept()
print("Accepted connection from ", address)

while True:
    try:
        try:
            data = client_socket.recv(1024)
        except bluetooth.btcommon.BluetoothError as err:
            print("Bluetooth Connection Lost or Terminated {}".format(err))
            # break

        if len(data) == 0:
            break

        roverCommand = command.Command(data.decode("utf-8"))
        print("Received: ", roverCommand)

    except(KeyboardInterrupt, SystemExit):
        print("Closing socket")
        client_socket.close()
        server_socket.close()
        break
