import socket
import threading
import random

# Define the server inforamtions [ IP , PORT ]
server_mapping = {
    '1': ('192.168.0.101', 80),
    '2': ('192.168.0.102', 80),
    '3': ('192.168.0.103', 80) #music server
}

servers_queues = {
    1: [],
    2: [],
    3: [] 
}

lock = threading.Lock()
#Create a socket between the LB and every server
servers_sockets = []
for i in range(1,4):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_mapping[str(i)][0], server_mapping[str(i)][1]))
    servers_sockets.append(server_socket)


#how servers are chosen 
def choose_server(request):
    ### scheduler method 1 ###
    # if 'M' in request:
    #     #return music server
    #     return servers_sockets[2]
    # else:
    #     random_number = random.randint(0, 1)
    #     return servers_sockets[random_number]

    ### scheduler method 2 ###
    music_request = 'M' in request
    server12_exe = 0 
    server3_exe = 0 
    if not music_request:
        server12_exe = int(request[1])
        server3_exe = 2* int(request[1])
    else: #M requset
        server12_exe = 2*int(request[1])
        server3_exe =  int(request[1])
    
    from time import time
    current_time = time()
    designated_server = 0
    end_time = float('inf')
    for i in range(1,4):
        queue = servers_queues[i]
        if len(queue) != 0 and ( i == 1 or i == 2):
            if queue[-1] + server12_exe < end_time:
                end_time = queue[-1] + server12_exe
                designated_server = i 
        elif len(queue) == 0 and (i == 1 or i == 2):
            if current_time + server12_exe < end_time:
                end_time = current_time + server12_exe
                designated_server = i
        else: # we are in the third server
            if len(queue) != 0 :
                if queue[-1] + server3_exe < end_time:
                    end_time = queue[-1] + server3_exe
                    designated_server = i
            else:
                if current_time + server3_exe < end_time:
                    end_time = current_time + server3_exe
                    designated_server = i

    ##add request to server
    servers_queues[designated_server].append(end_time)
    return  servers_sockets[designated_server-1], designated_server ,end_time








def route_request(client_socket):
    
    # Receive data from the client
    request_data = client_socket.recv(4096).decode().strip()
    lock.acquire()
    # Get the server based on the request content
    server_socket, server_index , end_time  = choose_server(request_data)

    

    # Forward the request to the chosen server
    server_socket.sendall(request_data.encode())
    lock.release()

    # Receive the response from the server
    response_data = server_socket.recv(4096)

    # Send the response back to the client
    client_socket.sendall(response_data)

    # Close the client connection
    client_socket.close()

    #remove from server queue
    lock.acquire()
    servers_queues[server_index].remove(end_time)
    lock.release()





# Create a socket for the load balancer that the clients connect to.
lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lb_socket.bind(('10.0.0.1', 80))
lb_socket.listen(15)

while True:
    # Accept incoming client connections
    client_socket, address = lb_socket.accept()
    print('Received connection from:', address)
     # Start a new process to handle the request
    thread = threading.Thread(target=route_request, args=(client_socket,))
    thread.start()

    
