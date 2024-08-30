__version__ = "DEV1.0"
print(f"Version: {__version__}")
print()

import socket
import time
import threading
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('-ip', '--server_ip', default=socket.gethostbyname(socket.gethostname()), type=str, help="Server IP Address")
parser.add_argument('-port', '--server_port', default=8080, type=int, help="The port where service running on")
arguments = parser.parse_args()

# Colors
NORMAL = '\033[0m'
RED = '\033[31m'
GREEN = '\033[32m'
ORANGE = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
YELLOW = '\033[93m'
PINK = '\033[95m'

HEADER = 64
PORT = arguments.server_port
SERVER = arguments.server_ip
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISC"

# This dictionary stores every message the user receives
MESSAGES = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(ADDR)
except Exception as e:
    print(e)
    print(RED, f"Server failed to bind at {ADDR}")
    exit()

def handle_client(conn, addr, client_username):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while True:
        action = str(conn.recv(4).decode(FORMAT))
        print("Action:" + action)
        if action == "SEND":
            msg = str(conn.recv(2048).decode(FORMAT))
            time.sleep(0.1)
            target = str(conn.recv(1024).decode(FORMAT))
            try:
                MESSAGES[target].append([msg, client_username]) # Send message
            except KeyError: # Target Username Not Found
                conn.send(b"-1") # -1 means Error
            else:
                conn.send(b"0") # 0 means Normal
            print(MESSAGES)

        if action == "RECV":
            messages = MESSAGES[client_username]
            NumberOfMessage = len(messages)
            conn.send(str(NumberOfMessage).encode(FORMAT)) # Send the number of messages
            if NumberOfMessage != 0:
                for i in range(NumberOfMessage):
                    time.sleep(0.05)
                    conn.send(messages[i][0].encode(FORMAT))
                    time.sleep(0.05)
                    conn.send(messages[i][1].encode(FORMAT))
            MESSAGES[client_username].clear()
        
        if action == DISCONNECT_MESSAGE:
            break

    conn.close()
    print(f"Connection with {addr} closed")

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        conn.send(b"HereIsPythonChattingService") # Send Verify Code
        username = str(conn.recv(1024).decode(FORMAT))
        if username == DISCONNECT_MESSAGE:
            conn.close()
            print(f"Connection with {addr} closed")
            continue
        MESSAGES.update({username:[]})
        thread = threading.Thread(target=handle_client, args=(conn, addr, username), name=username)
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()