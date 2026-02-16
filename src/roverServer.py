import socket
from control.command import Command
from control import movement
import traceback

HOST = '0.0.0.0'
PORT = 65432
BUFFER_SIZE = 2**20

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        print(f"Listening on {HOST}:{PORT}")
        while True:
            s.listen()
            conn, addr = s.accept()
            rover_setup()
            with conn:
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    try: 
                        command = Command(data.decode())
                        print(command.commandType)
                        print(command.commandArgs)
                        conn.send(bytes(handle_command(command), encoding="utf-8"))
                        if command.commandType == "Disconnect":
                            conn.close()
                            break
                    except ValueError as err:
                        conn.send(bytes("400: Unable to Parse Command", encoding="utf-8"))
                    except Exception as err:
                        conn.send(bytes("500: Internal Error", encoding="utf-8"))
                        error_message = traceback.format_exc()
                        conn.send(error_message.encode())

def rover_setup():
    movement.setup()

def handle_command(command: Command) -> str:
    match command.commandType:
        case "Forward" | "F":
            speed_float = 75
            if len(command) > 0:
                speed_float = float(command.get_command_arg(0))

            movement.forward(speed_float)
        case "Backward" | "B":
            speed_float = 75
            if len(command) > 0:
                speed_float = float(command.get_command_arg(0))

            movement.backward(speed_float)
            pass
        case "Left" | "L":
            speed_float = 75
            if len(command) > 0:
                speed_float = float(command.get_command_arg(0))

            movement.left(speed_float)
            pass
        case "Right" | "R":
            speed_float = 75
            if len(command) > 0:
                speed_float = float(command.get_command_arg(0))

            movement.right(speed_float)
            pass
        case "Stop" | "S":
            movement.stop()
            pass
        case "Disconnect":
            rover_cleanup()
        case "TestConnect":
            return "200: OK"
        case _:
            return "400: Unknown Command"
        
    return "200 OK"

def rover_cleanup():
    movement.cleanup()

if __name__ == "__main__":
    start_server()