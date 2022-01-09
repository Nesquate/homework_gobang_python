import game, socket, time, json

class Controller:
    def __init__(self):
        self.__IP: str = None
        self.__PORT: str = None
        self.__socket: socket.socket = None
        self.__BUFSIZE: int = 1024
        self.__game: game.Game = None

    def __send(self, command: str):
        time.sleep(0.1)
        self.__socket.send(command.encode("utf-8"))
        # print("DEBUG : command = {}".format(command))
        time.sleep(0.1)
        self.__socket.recv(self.__BUFSIZE)

    def __recv(self) -> str:
        time.sleep(0.1)
        command = self.__socket.recv(self.__BUFSIZE).decode("utf-8")
        # print("DEBUG : recv = {}".format(command))
        time.sleep(0.1)
        msg = "TCP_CLIENT_OK"
        self.__socket.send(msg.encode("utf-8"))

        return command

    #LoginUI
    def login(self, ADDR: str, PORT: int, name: str) -> str:
        try:
            # Get IP again
            self.__IP = socket.gethostbyname(ADDR)

            # Create a socket object as client
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.settimeout(5.0)

            # Connect to server
            
            self.__socket.connect((self.__IP, PORT))

            msg = "LOGIN" + "," + name
            self.__send(msg)

            recv_msg = self.__recv()

            if recv_msg == "FAIL":
                return "FAIL"
            
            return "SUCCESS"

        except socket.error as socketError:
            # print('Occurred Socket error! Information:')
            # print(socketError)
            return "FAIL"

        except Exception as otherError:
            print('Occurred other error! Information:')
            print(otherError)

            return "EXCEPTION"
    #Menu
    def logout(self) -> str:
        try:
            self.__send("LOGOUT")
            recv_msg = self.__recv()

            if recv_msg == "OK":
                print("DEBUG : Socket Closed.")
                self.__socket.close()
                return "SUCCESS"
            return "FAIL"
        
        except socket.error as socketError:
            print('Occurred Socket error! Information:')
            print(socketError)
            print("Force stop...")
            exit(2)

        except Exception as otherError:
            print('Occurred other error! Information:')
            print(otherError)
            print("Force stop...")
            exit(2)

    #Lobby
    def getLobby(self):
        try:
            self.__send("GET_LOBBY")
            recv_msg = self.__recv()

            if recv_msg == "FAIL":
                return "FAIL"
            

            lobby_list = json.loads(recv_msg)

            return lobby_list

        except socket.error as socketError:
            print('Occurred Socket error! Information:')
            print(socketError)
            print("Force stop...")
            exit(2)

        except Exception as otherError:
            print('Occurred other error! Information:')
            print(otherError)
            print("Force stop...")
            exit(2)

    def create(self, size: int, winCondi: int) -> str:
        try:
            msg = "CREATE" + "," + str(size) + "," + str(winCondi)
            self.__send(msg)

            recv_msg = self.__recv()

            if recv_msg == "FAIL":
                return "FAIL"
            
            return recv_msg
        
        except socket.error as socketError:
            print('Occurred Socket error! Information:')
            print(socketError)
            print("Force stop...")
            exit(2)

        except Exception as otherError:
            print('Occurred other error! Information:')
            print(otherError)
            print("Force stop...")
            exit(2)
        
    def joinRoom(self, id: str):
        try:
            msg = "JOIN" + "," + id
            self.__send(msg)

            recv_msg = self.__recv()
            
            if recv_msg == "FAIL":
                return "FAIL"
            
            self.__game = game.Game()
            self.__game.setSize(int(recv_msg))

            return recv_msg

        except socket.error as socketError:
            print('Occurred Socket error! Information:')
            print(socketError)
            print("Force stop...")
            exit(2)

        except Exception as otherError:
            print('Occurred other error! Information:')
            print(otherError)
            print("Force stop...")
            exit(2)


    #Room
    def getPlayerList(self) -> str:
        try:
            self.__send("GET_PLAYER_LIST")

            recv_msg = self.__recv()

            if recv_msg == "FAIL":
                return "FAIL"

            list_dict = json.loads(recv_msg)
            
            return list_dict

        except socket.error as socketError:
            print('Occurred Socket error! Information:')
            print(socketError)
            print("Force stop...")
            exit(2)

        except Exception as otherError:
            print('Occurred other error! Information:')
            print(otherError)
            print("Force stop...")
            exit(2)

    def ready(self) -> str:
        try:
            self.__send("READY")
            recv_msg = self.__recv()

            if recv_msg == "FAIL":
                return "FAIL"
            
            return True
        except socket.error as socketError:
            print('Occurred Socket error! Information:')
            print(socketError)
            print("Force stop...")
            exit(2)

        except Exception as otherError:
            print('Occurred other error! Information:')
            print(otherError)
            print("Force stop...")
            exit(2)

    def start(self) -> str:
        try:
            self.__send("START")
            recv_msg = self.__recv()

            if recv_msg == "FAIL":
                return "FAIL"

            if recv_msg == "NOT_ALL_READY":
                return "NOT_ALL_READY"
            
            self.__game.setTurn(int(recv_msg))

            return "SUCCESS"
        
        except socket.error as socketError:
            print('Occurred Socket error! Information:')
            print(socketError)
            print("Force stop...")
            exit(2)

        except Exception as otherError:
            print('Occurred other error! Information:')
            print(otherError)
            print("Force stop...")
            exit(2)

    def leave(self) -> str:
        try:
            self.__send("LEAVE")

            recv_msg = self.__recv()

            if recv_msg == "FAIL":
                return "FAIL"
            
            return "SUCCESS"

        except socket.error as socketError:
            print('Occurred Socket error! Information:')
            print(socketError)
            print("Force stop...")
            exit(2)

        except Exception as otherError:
            print('Occurred other error! Information:')
            print(otherError)
            print("Force stop...")
            exit(2)

    #Gamming
    def getSize(self) -> int:
        return self.__game.getSize()

    def getBoard(self):
        try:
            self.__send("GET_BOARD")
            recv_msg = self.__recv()

            if recv_msg == "FAIL":
                return "FAIL"
            
            board = json.loads(recv_msg)
            self.__game.setBoard(board)

            return board
        
        except socket.error as socketError:
            print('Occurred Socket error! Information:')
            print(socketError)
            print("Force stop...")
            exit(2)

        except Exception as otherError:
            print('Occurred other error! Information:')
            print(otherError)
            print("Force stop...")
            exit(2)

    def getWho(self) -> str:
        try:
            self.__send("GET_WHO")
            recv_msg = self.__recv()

            if recv_msg == "FAIL":
                return "FAIL"

            turn_now = int(recv_msg)
            turn_your = self.__game.getTurn()

            if turn_now == turn_your:
                return "IS_YOU"
            else:
                return "NO_YOU"

        except socket.error as socketError:
            print('Occurred Socket error! Information:')
            print(socketError)
            print("Force stop...")
            exit(2)

        except Exception as otherError:
            print('Occurred other error! Information:')
            print(otherError)
            print("Force stop...")
            exit(2)

    def setPos(self, x: int, y: int) -> str:
        try:
            msg = "SET_POS" + "," + str(x) + "," + str(y)
            self.__send(msg)
            recv_msg = self.__recv()

            if recv_msg == "FAIL":
                return "FAIL"
            
            if recv_msg == "ALREADY_SET":
                return "EXIST"
            
            return "SUCCESS"

        except socket.error as socketError:
            print('Occurred Socket error! Information:')
            print(socketError)
            print("Force stop...")
            exit(2)

        except Exception as otherError:
            print('Occurred other error! Information:')
            print(otherError)
            print("Force stop...")
            exit(2)
            

    def getWinner(self) -> str:
        try:
            self.__send("GET_WINNER")
            recv_msg = self.__recv()

            if recv_msg == "FAIL":
                return "FAIL"
            
            return recv_msg
        
        except socket.error as socketError:
            print('Occurred Socket error! Information:')
            print(socketError)
            print("Force stop...")
            exit(2)

        except Exception as otherError:
            print('Occurred other error! Information:')
            print(otherError)
            print("Force stop...")
            exit(2)

    def gameOver(self) -> str:
        try:
            self.__send("GAMEOVER")
            recv_msg = self.__recv()

            if recv_msg == "FAIL":
                return "FAIL"
            
            return "SUCCESS"

        except socket.error as socketError:
            print('Occurred Socket error! Information:')
            print(socketError)
            print("Force stop...")
            exit(2)

        except Exception as otherError:
            print('Occurred other error! Information:')
            print(otherError)
            print("Force stop...")
            exit(2)
    
    def getLocalTurn(self):
        return self.__game.getTurn()