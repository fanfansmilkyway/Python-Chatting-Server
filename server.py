import socket
import time
import threading
import duckdb
import time

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
PORT = 8080
SERVER = "0.0.0.0"
#SERVER = "127.0.0.1"
# Another way to get the local IP address automatically
#SERVER = socket.gethostbyname(socket.gethostname())
#print(SERVER)
#print(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISC"

# This dictionary stores every message the user receives
MESSAGES = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
'''
def detect_client_connection(conn):
    try:
        conn.send(b"Verify is the client still connected")
    except BrokenPipeError:
        return False
    else:
        return True
'''

def handle_client(conn, addr, client_username):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while True:
        '''
        if detect_client_connection(conn) == False:
            return
        '''
        action = str(conn.recv(4).decode(FORMAT))
        print("Action:" + action)
        if action == "SEND":
            print("SEND")
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
            print("RECV")
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