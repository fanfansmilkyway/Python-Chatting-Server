import socket
import time
import threading

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
PORT = 8081
SERVER = "127.0.0.1"
# Another way to get the local IP address automatically
#SERVER = socket.gethostbyname(socket.gethostname())
#print(SERVER)
#print(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# This dictionary stores every message the user receives
MESSAGES = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr, client_username):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        action = str(conn.recv(256).decode(FORMAT))
        print("Action:" + action)
        if action == "SEND":
            print("SEND")
            msg = str(conn.recv(2048).decode(FORMAT))
            if msg == DISCONNECT_MESSAGE:
                break
            target = str(conn.recv(1024).decode(FORMAT))
            MESSAGES[target].append([msg, client_username]) # Send message
            print(MESSAGES)

        if action == "RECEIVE":
            messages = MESSAGES[client_username]
            NumberOfMessage = len(messages)
            conn.send(str(NumberOfMessage).encode(FORMAT)) # Send the number of messages
            time.sleep(0.25)
            if NumberOfMessage != 0:
                for i in range(NumberOfMessage):
                    conn.send(messages[i][0].encode(FORMAT))
                    time.sleep(0.15)
                    conn.send(messages[i][1].encode(FORMAT))
                    time.sleep(0.15)
            MESSAGES[client_username].clear()

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        username = str(conn.recv(1024).decode(FORMAT))
        MESSAGES.update({username:[]})
        thread = threading.Thread(target=handle_client, args=(conn, addr, username), name=username)
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()