from ServerHandler import ServerHandler

class VideoServerHandler(ServerHandler):
    def __init__(self, ip, port, responseQueue) -> None:
        super().__init__(ip, port, 2, 1, 1, responseQueue)