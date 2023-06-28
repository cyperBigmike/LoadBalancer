from MusicServerHandler import MusicServerHandler
from VideoServerHandler import VideoServerHandler
from ServerHandler import ServerHandler
from Request import Request
from queue import Queue
import socket
from threading import Thread

class LoadBalancer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('10.0.0.1', 80))
        self.socket.listen(15)
        self.ResponseQueue = Queue()
        self.servers = [VideoServerHandler("192.168.0.101",80,self.ResponseQueue),
                        VideoServerHandler("192.168.0.102",80,self.ResponseQueue),
                        MusicServerHandler("192.168.0.103",80,self.ResponseQueue)]
        self.Logic()
        
    def FindBestServer(self,request) -> ServerHandler:
        
        minIdx =  min([(serverHandler.ComputeTimeToExecute(request),i) for i,serverHandler in enumerate(self.servers)])[1]
        return self.servers[minIdx]
    
    def HandleConncetion(self,conn :socket.socket):
        print("Handling Connection")
        with conn:
            requestString = conn.recv(4096).decode().strip()
            print("Got Request", requestString)
            request = Request(requestString)
            serverHandler = self.FindBestServer(request)
            print("Chose handler", serverHandler._socket.getpeername())
            response = serverHandler.HandleRequest(request)
            print("Got Response", response)
            conn.sendall(response)
            print("Sent Response")
    
    def Logic(self):
        while True:
            print("Waiting For connection... ")
            conn, addr = self.socket.accept()
            print("Connecton Accepted!")
            func = lambda : self.HandleConncetion(conn)
            Thread(target=func).start()
            
            
if __name__ == "__main__":
    LoadBalancer()