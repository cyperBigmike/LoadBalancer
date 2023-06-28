from MusicServerHandler import MusicServerHandler
from VideoServerHandler import VideoServerHandler
from ServerHandler import ServerHandler
from Request import Request
from queue import Queue
import socket
from threading import Thread

class LoadBalancer:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('10.0.0.1', 80))
        self.socket.listen()
        self.ResponseQueue = Queue()
        self.servers = [VideoServerHandler("192.168.0.101",80,self.ResponseQueue),
                        VideoServerHandler("192.168.0.102",80,self.ResponseQueue),
                        MusicServerHandler("192.168.0.103",80,self.ResponseQueue)]
        self.Logic()
        
    def FindBestServer(self,request) -> ServerHandler:
        return min([(serverHandler, serverHandler.ComputeTimeToExecute(request)) for serverHandler in self.servers])[0]
    
    def HandleConncetion(self,conn :socket.socket):
        requestString = conn.recv(4096)
        request = Request(requestString)
        serverHandler = self.FindBestServer(request)
        response = serverHandler.HandleRequest(request)
        conn.sendall(response)
        
    
    def Logic(self):
        while True:
            conn, addr = self.socket.accept()
            func = lambda : self.HandleConncetion(conn)
            Thread(target=func).start
            
            
            