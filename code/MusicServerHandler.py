from ServerHandler import ServerHandler

class MusicServerHandler(ServerHandler):
    def __init__(self, ip, port) -> None:
        super().__init__(ip, port, 1, 3, 2)