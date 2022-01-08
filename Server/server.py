import socket

class Server:
    def __init__(self, ADDR: str, PORT: int):
        self.__socket: socket.socket = None
        self.__IP: str = socket.gethostbyname(ADDR)
        self.__PORT: int = PORT
        self.__BUFSIZE: int = 1024
        self.__init(self.__IP, self.__PORT)
        
    def __init(self, ip: str, port: int):
        # Create server socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Enable socket port that can be reused
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind port
        server.bind((ip, port))
        # Set max socket queue to 1
        server.listen(1)

        self.__socket = server

    def accept(self) -> socket.socket:
        client, (rip, rport) = self.__socket.accept()
        print("Log : Create connection from {}, {}".format(rip, rport))
        
        return client

    def closeServer(self):
        self.__socket.close()