import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))  # Bind to all interfaces
server_socket.listen(5)  # Listen for connections
print("Server listening on port 8080")

while True:
    client_socket, address = server_socket.accept()
    print(f"Connection from {address}")
    # Handle client connection
