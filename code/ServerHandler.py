import threading
from queue import Queue
from threading import Thread, Lock
import socket

class ServerHandler:
    def __init__(self,ip, port, musicMutiplier, VideoMutiplier, PictureMultiplier) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((ip,port))
        self._musicMutiplier = musicMutiplier
        self._videoMultiplier = VideoMutiplier
        self._pictureMultiplier = PictureMultiplier
        self._backlog = 0
        self._backlogLock = Lock()
        
    def HandleRequest(self, request):
        time = self.ComputeTimeToExecute(request)
        self._backlogLock.acquire()
        self._backlog += time
        self._backlogLock.release()
        self._socket.sendall(request.encode())
        
        data = self._socket.recv(4096)
        self._backlogLock.acquire()
        self._backlog -= time
        self._backlogLock.release()
        
        return data
            
    def ComputeTimeToExecute(self, request):
        requestType = request[0]
        requestSize = int(request[1])
        # Match would btter here but assuming older python version
        time = float("inf")
        if requestType == "M":
            time = self._musicMutiplier * requestSize
        elif requestType == "V":
            time = self._videoMultiplier * requestSize
        elif requestType == "P":
            time = self._pictureMultiplier * requestSize
        self._backlogLock.acquire()
        time += self._backlog
        self._backlogLock.release()
        
        return time

        
        
    