import os, socket, time
import controller

class UI:
    def __init__(self):
        self.__name: str = None
        self.__size: int = None
        self.__id: str = None
        self.__ADDR: str = None
        self.__PORT: int = None
        self.__controller: controller.Controller = controller.Controller()

    def __enter(self):
        input("Press [ENTER] to continue...")

    def __clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def __login(self):
        while True:
            try:
                name = str(input("Enter your name: "))
                addr = str(input("Enter server address: "))
                port = int(input("Enter server port: "))
            except:
                print("You type wrong data, try again!")
                self.__enter()
                continue
            
            result = self.__controller.login(addr, port, name)
            
            if result == "FAIL":
                print("Connection failed.")
                self.__enter()
                continue

            if result == "EXCEPTION":
                print("Force end.")
                exit(2)
            
            self.__name = name
            self.__ADDR = addr
            self.__port = port
            return

    def __quit(self):
        result = self.__controller.logout()
        
        if result == "FAIL":
            print("Logout error!")
            self.__enter()
            return

        exit(0)

    def menu(self):
        while True:
            try:
                self.__clear()
                if self.__name == None:
                    self.__login()
                    continue
                print("Your name : {}".format(self.__name))
                print("====== Menu ======")
                print("[L] Lobby")
                print("[Q] Quit")
                print("==================")
                choose = str(input("Choose > "))

                if choose == "L":
                    self.__lobby()
                elif choose == "Q":
                    self.__quit()
                else:
                    print("Unknown option.")
                    self.__enter()
                    continue

            except socket.error as socketError:
                print("Occurred connect exception on menu!")
                print("Details: ")
                print(socketError)
                print("Force stop...")
                exit(2)
            except Exception as otherError:
                print("Occurred other exception on menu!")
                print("Details: ")
                print(otherError)
                print("Force stop...")
                exit(2)


    #Lobby

    def __updateLobbyList(self):
        result = self.__controller.getLobby()

        if result == "FAIL" or result == "EXCEPTION":
            print("Failed to get lobby!")
            self.__enter()
            return "FAIL"

        return result

    def __lobby(self):
        while True:
            self.__clear()
            
            result = self.__updateLobbyList()
            if result == "FAIL":
                return

            print("Your name : {}".format(self.__name))
            print("====== Lobby ======")
            if len(result) > 0:
                for i in result:
                    print("Room [{}]".format(i))
            else:
                print("No room available.")
            print("===================")
            print("[R] Refresh [J] Join [C] Create [B] Back")
            
            choose = str(input("Choose > "))

            if choose == "R":
                continue
            elif choose == "J":
                if len(result) > 0:
                    self.__joinRoom(result)
            elif choose == "C":
                self.__createRoom()
            elif choose == "B":
                return
            else:
                print("Unknown option.")
                self.__enter()
                continue
        

    def __createRoom(self):
        result = self.__create()
        
        if result == "FAIL":
            print("Failed to create room.")
            self.__enter()
            return

        result = self.__updateLobbyList()
        if result == "FAIL":
            return

        self.__joinRoom(result, choose=self.__id)

    def __create(self):
        while True:
            self.__clear()
            try:
                size = int(input("Input board size: "))
                winCondi = int(input("Input win condition: "))
                break
            except:
                print("You data has wrong, try again!")
                self.__enter()

        result = self.__controller.create(size, winCondi)

        if result != "FAIL" and result != "EXCEPTION":
            self.__id = result
            return "SUCCESS"
        else:
            return "FAIL"


    def __joinRoom(self, lobbyList: list, choose=None):
        while True:
            
            if choose == None:
                choose = str(input("Which one > "))
                if choose not in lobbyList:
                    print("Unknown option.")
                    self.__enter()
                    choose = None
                    continue
            
            self.__id = choose
            result = self.__controller.joinRoom(choose)

            if result != "FAIL" and result != "EXCEPTION":
                self.__size = int(result)
                self.__room()
                return
            else:
                print("Failed to join room!")
                self.__enter()
                return

    # Room
    def __room(self):
        while True:
            self.__clear()

            result = self.__controller.getPlayerList()
            if result != "FAIL" and result != "EXCEPTION":
                print("Your name : {}".format(self.__name))
                print("====== Room ======")
                for i in result.keys():
                    print("{}, Ready : {}".format(i, result[i]))
                print("==================")
                print("[E] Ready [L] Leave [R] Refresh")
                choose = str(input("Choose > "))

                if choose == "E":
                    result_ready = self.__controller.ready()
                    if result_ready != "FAIL" and result_ready != "EXCEPTION":
                        result_start = self.__controller.start()
                        if result_start != "FAIL" and result_start != "EXCEPTION":
                            while result_start == "NOT_ALL_READY":
                                print("Not all players ready! Wait for 3 second...")
                                time.sleep(3.0)
                                result_start = self.__controller.start()
                            self.__gamming()
                        else:
                            print("Failed to start game.")
                            self.__enter()
                            result_ready = self.__controller.ready()
                            if result_ready != "FAIL" and result_ready != "EXCEPTION":
                                continue
                            else:
                                print("Failed to set ready.")
                                self.__enter()
                                continue
                    else:
                        print("Failed to set ready.")
                        self.__enter()
                        continue
                elif choose == "L":
                    result = self.__controller.leave()
                    self.__enter()
                    return
                elif choose == "R":
                    continue
                else:
                    print("Unknown option.")
                    self.__enter()
            else:
                print("Failed to get player list!")
                self.__enter()



    # Gamming

    def __gamming(self):
        
        while True:
            self.__size = self.__controller.getSize()
            result_board = self.__controller.getBoard()

            if result_board != "FAIL" and result_board != "EXCEPTION":
                self.__printBoard(result_board)

                result_continue = self.__getWinner()

                if result_continue == "CONTINUE":
                    result_who = self.__controller.getWho()
                    if result_who != "FAIL" and result_who != "EXCEPTION":
                        while result_who == "NO_YOU":
                            print("Not your turn now, waiting for three second...")
                            time.sleep(3.0)

                            self.__size = self.__controller.getSize()
                            result_board = self.__controller.getBoard()

                            self.__printBoard(result_board)
                            result_continue = self.__getWinner()

                            if result_continue == "CONTINUE":
                                result_who = self.__controller.getWho()
                                continue
                            elif result_continue == "FORCE_STOP":
                                print("Game force stop...")
                                self.__enter()
                                self.__controller.gameOver()
                                return
                            elif result_continue == "GAMEOVER":
                                print("Game over!")
                                self.__enter()
                                self.__controller.gameOver()
                                return
                            else:
                                print("Error! Force to stop...")
                                self.__enter()
                                self.__controller.gameOver()
                                return
                        
                        self.__size = self.__controller.getSize()
                        result_board = self.__controller.getBoard()
                        result_continue = self.__getWinner()

                        self.__printBoard(result_board)
                        result_continue = self.__setPiece()
                        if result_continue == "ERROR_FORCE_STOP":
                            print("Failed to set piece! Force stop...")
                            self.__enter()
                            self.__controller.gameOver()
                            return
                        continue
                    else:
                        print("Failed to get who is turn! Force stop...")
                        self.__enter()
                        self.__controller.gameOver()
                        return

                elif result_continue == "FORCE_STOP" or result_continue == "ERROR_FORCE_STOP":
                    print("Error! Game force stop...")
                    self.__enter()
                    self.__controller.gameOver()
                    return
                else:
                    self.__controller.gameOver()
                    self.__enter()
                    return 
                    
            else:
                print("Failed to get board! Stop gamming...")
                self.__controller.gameOver()
                self.__enter()
                return

    def __printBoard(self, result_board: list):
        self.__clear()
        count_x = 0
        count_y = 0
        turn = self.__controller.getLocalTurn()
        print("Your piece: {}".format(turn))
        print("====== Gamming ======")
        print("  ",end="")
        for j in range(0, self.__size):
            print("{} ".format(count_x), end="")
            count_x += 1
        print()
        for i in range(0, self.__size):
            print("{} ".format(count_y), end="")
            count_y += 1
            for j in range(0, self.__size):
                text = result_board[i][j]
                if text == "EMPTY":
                    print("_ ", end="")
                else:
                    print("{} ".format(text), end="")
            print()
        print("=====================")

    def __setPiece(self):
        while True:
            try:
                x = int(input("Input x: "))
                y = int(input("Input y: "))

                if (x >= self.__size or x < 0) or (y >= self.__size or y < 0):
                    print("Enter data error! Try again.")
                    continue
                result_setPiece = self.__controller.setPos(x, y)
                if result_setPiece == "EXIST":
                    print("This pos is not empty! Try again!")
                    self.__enter()
                    continue
                elif result_setPiece == "FAIL" or result_setPiece == "EXCEPTION":
                    return "ERROR_FORCE_STOP"
                else:
                    return "CONTINUE"

            except:
                print("Enter data error! Try again.")
                continue

    def __getWinner(self) -> str:
        result_winner = self.__controller.getWinner()
        if result_winner != "FAIL" and result_winner != "EXCEPTION":
            if result_winner == "NOT_YET":
                return "CONTINUE"
            elif result_winner == "TIE":
                print("Winner : {}".format(result_winner))
                self.__enter()
                return "GAMEOVER"
            elif result_winner == "FORCE_GAMEOVER":
                return "FORCE_STOP"
            else:
                print("Winner : {}".format(result_winner))
                return "GAMEOVER"
        else:
            return "ERROR_FORCE_STOP"