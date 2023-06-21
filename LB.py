import socket
import threading
import random

# Define the server inforamtions [ IP , PORT ]
server_mapping = {
    '1': ('192.168.0.101', 80),
    '2': ('192.168.0.102', 80),
    '3': ('192.168.0.103', 80)
}



#Create a socket between the LB and every server
servers_sockets = []
for i in range(3):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_mapping[str(i)][0], server_mapping[str(i)][1]))
    servers_sockets.append(server_socket)


#how servers are chosen 
def choose_server(request):
    random_number = random.randint(0, 2)
    return servers_sockets[random_number]



def route_request(client_socket):
    
    # Receive data from the client
    request_data = client_socket.recv(4096).decode().strip()

    # Get the server based on the request content
    server_socket = choose_server(request_data)

    if server_socket:

        # Forward the request to the chosen server
        server_socket.sendall(request_data.encode())

        # Receive the response from the server
        response_data = server_socket.recv(4096)

        # Send the response back to the client
        client_socket.sendall(response_data)

    # Close the client connection
    client_socket.close()


# Create a socket for the load balancer that the clients connect to.
lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lb_socket.bind(('10.0.0.1', 80))
lb_socket.listen(10)

while True:
    # Accept incoming client connections
    client_socket, address = lb_socket.accept()
    print('Received connection from:', address)
     # Start a new process to handle the request
    thread = threading.Thread(target=route_request, args=(client_socket))
    thread.start()

    
