import threading, socket, time, json
import lobby, room

class Player(threading.Thread):
    def __init__(self, threadName, client: socket.socket, globalLobby: lobby.Lobby):
        super().__init__(name=threadName)
        self.__socket: socket.socket = client
        self.__name: str = None
        self.globallobby: lobby.Lobby = globalLobby
        self.room: room.Room = None
        self.__turn: int = 0
        self.__ready: bool = False
        self.__BUFSIZE: int = 1024
        self.start()
    
    def run(self):
        if self.__login() == True:
            self.head()
    
    def __send(self, command: str):
        time.sleep(0.1)
        # print("Debug : {}, command = {}".format(self.__name, command))
        self.__socket.send(command.encode("utf-8"))
        time.sleep(0.1)
        self.__socket.recv(self.__BUFSIZE)

    def __recv(self) -> str:
        time.sleep(0.1)
        command = self.__socket.recv(self.__BUFSIZE).decode("utf-8")
        # print("Debug : {}, recv = {}".format(self.__name, command))
        time.sleep(0.1)
        msg = "TCP_SERVER_OK"
        self.__socket.send(msg.encode("utf-8"))

        return command

    def head(self):
        while True:
            try:
                command = self.__recv()
                command_list = command.split(",")

                # Menu
                if command_list[0] == "GET_LOBBY":
                    if len(command_list) == 1:
                        self.__getLobby()
                        continue

                if command_list[0] == "LOGOUT":
                    if len(command_list) == 1:
                        self.__logout()
                        self.__socket.close()
                        return
                
                # Lobby
                if command_list[0] == "CREATE":
                    if len(command_list) == 3:
                        self.__create(int(command_list[1]), int(command_list[2]))
                        continue
                
                if command_list[0] == "JOIN":
                    print("DEBUG : JOIN = {}".format(command_list))
                    if len(command_list) == 2:
                        result = self.__join(command_list[1])
                        if result  == True:
                            continue

                # Room
                if command_list[0] == "GET_PLAYER_LIST":
                    if len(command_list) == 1:
                        self.__roomPlayerList()
                        continue

                if command_list[0] == "READY":
                    if len(command_list) == 1:
                        result = self.__setReady()
                        if result == True:
                            continue
                
                if command_list[0] == "START":
                    if len(command_list) == 1:
                        self.__start()
                        continue

                if command_list[0] == "LEAVE":
                    if len(command_list) == 1:
                        self.__leave()
                        continue

                # Gamming
                if command_list[0] == "GET_BOARD":
                   if len(command_list) == 1:
                       self.__getBoard()
                       continue

                if command_list[0] == "GET_WHO":
                    if len(command_list) == 1:
                        self.__getWho()
                        continue

                if command_list[0] == "SET_POS":
                    if len(command_list) == 3:
                        self.__setPos(int(command_list[1]), int(command_list[2]))
                        continue

                if command_list[0] == "GET_WINNER":
                    if len(command_list) == 1:
                        self.__getWinner()
                        continue
                
                if command_list[0] == "GAMEOVER":
                    if len(command_list) == 1:
                        self.__gameOver()
                        continue
                
                self.__send("FAIL")
            except socket.error as socketError:
                print("Log : {} has logout this server by error(s).".format(self.__name))
                # print("Occurred serious problem about socket from player!")
                # print("Details : ")
                print(socketError)
                # print("...and FORCE STOP this thread.")
                self.__forceStop()
                return
            
            except Exception as otherError:
                print("Log : {} has logout this server by error(s).".format(self.__name))
                # print("Occurred other exception(s) from players")
                # print("when send/recv socket command!")
                print("Details : ")
                print(otherError)
                # print("...and FORCE STOP this thread.")
                self.__forceStop()
                return


    def __login(self) -> bool:
        try:
            command = self.__recv()
            command_list = command.split(",")

            if command_list[0] != "LOGIN":
                self.__send("FAIL")
                return False

            if len(command_list) != 2:
                self.__send("FAIL")
                return False

            self.__name = command_list[1]
            result_name = self.globallobby.joinPlayer(self.__name)
            if result_name == False:
                self.__send("FAIL")
                return False
            self.__send("OK")

            print("Log : {} join this server.".format(self.__name))

            return True
        except socket.error as clientError:
            print("Occurred error from player!")
            print("Details : ")
            print(clientError)
            return False

        except Exception as otherError:
            print("Occurred other error from player!")
            print("Details : ")
            print(otherError)
            return False

    
    # Lobby 
    # def lobby(self):
    #     pass

    def __logout(self):
        self.globallobby.removePlayer(self.__name)
        self.__send("OK")
        print("Log : {} has logout this server.".format(self.__name))

    def __getLobby(self):
        room_list = self.globallobby.getRoomList()
        room_json = json.dumps(room_list)
        self.__send(room_json)

    def __create(self, size: int, winCondi: int):
        id = self.globallobby.createRoom(size, winCondi)
        self.__send(id)

    def __join(self, id: str) -> bool:
        roomList = self.globallobby.getRoomList()
        if id in roomList:
            self.room = self.globallobby.getRoomObj(id)
            
            result = self.room.addPlayer(self.__name, self)
            if result == False:
                self.room = None
                return False
            
            self.__turn =  self.room.setPlayerTurn(self.__name)

            size = self.room.getSize()
            self.__send(str(size))

            return True
        return False

    # Room
    # def room(self):
    #     pass

    def __roomPlayerList(self):
        playerList = self.room.getPlayerList()
        list_json = json.dumps(playerList)

        self.__send(list_json)

    def __setReady(self):
        result = self.room.setPlayerReady(self.__name)
        if result == True:
            if self.__ready == True:
                self.__ready == False
            elif self.__ready == False:
                self.__ready == True
            self.__send("OK")
            return True
        else:
            return False

    def __leave(self):
        self.room.removePlayer(self.__name, self)
        player_count = self.room.getPlayerCount()

        if player_count <= 0:
            id = self.room.getRoomID()
            self.globallobby.removeRoom(id, self.room)

        self.room = None
        
        self.__send("OK")

    def __start(self):
        result = self.room.getAllReady()
        
        if result == True:
            self.room.resetGame()
            self.__turn = self.room.setPlayerTurn(self.__name)
            self.room.setGameRunning()
            self.__send(str(self.__turn))
        else:
            self.__send("NOT_ALL_READY")

    #Gamming
    # def gamming(self):
    #     pass

    def __getBoard(self):
        board = self.room.getBoard()
        board_json = json.dumps(board)
        self.__send(board_json)

    def __getWho(self):
        turn = self.room.getTurn()
        self.__send(str(turn))

    def __setPos(self, x: int, y: int):
        result_set = self.room.setPiece(x, y)

        if result_set == True:
            result_winner = self.room.decideWinner(x, y, self.__name)
            if result_winner == "NOT_YET":
                self.room.changeTurn()
            self.__send("OK")
        else:
            self.__send("ALREADY_SET")

    def __getWinner(self):
        self.__send(self.room.getWinner())

    def __gameOver(self):
        winner = self.room.getWinner()
        
        if winner == "NOT_YET":
            self.room.forceGameOver()
        else:
            self.room.setGameOver()

        self.__send("OK")
        
    def __forceStop(self):
        try:
            if self.room != None:
                # 有房間的話，要考慮是否在房間內、是否已經開始
                playerList = self.room.getPlayerList()

                if self.__name in playerList.keys():
                    # 檢查一下遊戲是否正在進行中
                    gameOver = self.room.getGameOver()

                    if gameOver == False:
                        self.room.forceGameOver()

                    # 將自己從房間移除
                    self.room.removePlayer(self.__name, self)

                    # 判斷一下是否為空房間，如果是的話就順便一起移除
                    player_count = self.room.getPlayerCount()

                    if player_count <= 0:
                        id = self.room.getRoomID()
                        self.globallobby.removeRoom(id, self.room)
                
                # 最後就是移除自身參照
                self.globallobby.removePlayer(self.__name)
                self.room = None
                self.__socket.close()
        except Exception as otherError:
            print("Occurred error while force stop thread!")
            print("Details: ")
            print(otherError)

