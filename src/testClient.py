import socket

HOST = "localhost"
PORT = 65432
BUFFER_SIZE = 1024


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        message = input("Enter message to send to server: ")
        message = message.strip()
        message = message[:BUFFER_SIZE]
        print(f"Sending: {message}")
        s.sendall(message.encode())
        data = s.recv(BUFFER_SIZE)
        print(f"Received: {data.decode()}")

if __name__ == "__main__":
    start_client()

    