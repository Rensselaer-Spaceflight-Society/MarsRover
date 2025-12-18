import socket

HOST = 'localhost'
PORT = 65432
BUFFER_SIZE = 1024

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                print(f"Received: {data.decode()}")
                conn.sendall(data)

if __name__ == "__main__":
    start_server()