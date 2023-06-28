import threading
from queue import Queue
from threading import Thread
import socket
from Request import Request

class ServerHandler:
    def __init__(self,ip, port, musicMutiplier, VideoMutiplier, PictureMultiplier, responseQueue) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((ip,port))
        self._musicMutiplier = musicMutiplier
        self._videoMultiplier = VideoMutiplier
        self._pictureMultiplier = PictureMultiplier
        # self.RequestQueue = Queue() # Python queue's are threadsafe
        # self._responseQueue = Queue()
        
        # Thread(target=self.RequestLogic()).start
        # Thread(target=self.RequestLogic()).start
        
        
    def HandleRequest(self, request : Request):
        self._socket.sendall(request.RequestString)
        return self._socket.recv(4096)
        
    def RequestLogic(self):
        while True:
            request = self.RequestQueue.get()
            self._socket.sendall(request)

    def ResponseLogic(self):
        while True:
            response = self._socket.recv(4096)
            self.RequestQueue.put(response)
            
    def ComputeTimeToExecute(self, request : Request):
        requestType = request.RequestString[0]
        requestSize = request.RequestString[1]
        # Match would btter here but assuming older python version
        if requestType == "M":
            return self._musicMutiplier * requestSize
        elif requestType == "V":
            return self._videoMultiplier * requestSize
        elif requestType == "P":
            return self._pictureMultiplier * requestSize

        
        
    