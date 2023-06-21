import socket
import multiprocessing

# Define the server inforamtions [ IP , PORT ]
server_mapping = {
    'server1': ('192.168.0.101', 80),
    'server2': ('192.168.0.102', 80),
    'server3': ('192.168.0.103', 80)
}



#Create a socket between the LB and every server
server1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server1_socket.connect((server_mapping['sever1'][0], server_mapping['sever1'][1]))

server2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2_socket.connect((server_mapping['sever2'][0], server_mapping['sever2'][1]))

server3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server3_socket.connect((server_mapping['sever3'][0], server_mapping['sever3'][1]))

# Create a socket for the load balancer and the clients
lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lb_socket.bind(('10.0.0.1', 80))
lb_socket.listen(10)

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

while True:
    # Accept incoming client connections
    client_socket, address = lb_socket.accept()
    print('Received connection from:', address)
     # Start a new process to handle the request
    process = multiprocessing.Process(target=route_request, args=(client_socket,))
    process.start()

    
