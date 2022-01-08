from ctypes import sizeof


class Room:
    def __init__(self, id: str, size: int, winCondi: int):
        self.__id: str = id
        self.__size: int = size
        self.__winCondi: int = winCondi
        self.__nowTurn: int = 1
        self.__winner: str = "NOT_YET"
        self.__board: list = None
        self.__gameRunning: bool = False
        self.__gameOver: bool = False
        self.__playerNameList: dict = dict()
        self.__playerNameObj: list = list()
        self.__initRoom()

    def __initRoom(self):
        self.__board = list()
        for i in range(0, self.__size):
            emptyList = list()
            for j in range(0, self.__size):
                emptyList.append("EMPTY")
            self.__board.append(emptyList)
        
        self.__gameRunning = False
        self.__gameOver == False
        self.__winner = "NOT_YET"

    def addPlayer(self, name, playerObj) -> bool:
        if len(self.__playerNameObj) >= 2:
            return False

        self.__playerNameList[name] = "N"
        self.__playerNameObj.append(playerObj)

        return True

    def removePlayer(self, name, playerObj):
        if name in self.__playerNameList.keys():
            del self.__playerNameList[name]
        if playerObj in self.__playerNameObj:
            self.__playerNameObj.remove(playerObj)

    def getPlayerList(self) -> dict:
        return self.__playerNameList
    
    # 設定玩家的 Turn，以 dict key 的 index 為準
    def setPlayerTurn(self, name: str) -> int:
        key_index = 0
        # 暴力窮舉
        for key in self.__playerNameList.keys():
            if name == key:
                return key_index + 1
            key_index += 1
        
        return -1

    def setPlayerReady(self, name: str) -> bool:
        if name in self.__playerNameList.keys():
            if self.__playerNameList[name] == "N":
                self.__playerNameList[name] = "Y"
                return True
            elif self.__playerNameList[name] == "Y":
                self.__playerNameList[name] = "N"
                return True
        return False

    def getPlayerCount(self) -> int:
        return len(self.__playerNameList.keys())

    def getAllReady(self) -> bool:
        count = 0
        for name in self.__playerNameList.keys():
            ready = self.__playerNameList[name]
            if ready == "Y":
                count += 1

        if count >= 2:
            return True
        return False

    def setGameRunning(self):
        if self.__gameRunning == False:
            self.__gameRunning = True

    # 取得現在遊線過程的 Turn
    def getTurn(self) -> int:
        return self.__nowTurn

    # 變更遊玩順序
    def changeTurn(self):
        if self.__nowTurn == 1:
            self.__nowTurn = 2
            return
        else:
            self.__nowTurn = 1
            return

    def getRoomID(self) -> str:
        return self.__id

    def getBoard(self) -> list:
        return self.__board

    def getSize(self) -> int:
        return self.__size
    
    def setPiece(self, x: int, y: int) -> bool:
        if self.__board[y][x] == "EMPTY":
            self.__board[y][x] = str(self.__nowTurn)
            return True
        return False

    # 看看目前的勝敗狀況
    def getWinner(self) -> str:
        return self.__winner

    def decideWinner(self, x: int, y: int, name: str) -> str:
        """
        勝敗演算法
        
        - 玩家名稱 -> 決定勝負
        - "TIE" -> 平手
        - "NOT_YET" -> 還在進行
        """

        if self.__winner == "FORCE_GAMEOVER":
            return "FORCE_GAMEOVER"

        if self.__winner == "NOT_YET":
            print("Debug : wincondi = {}".format(self.__winCondi))
            count = 1
            # 左上 & 右下
            ## 左上
            copy_x = x - 1
            copy_y = y - 1
            while copy_x >= 0 and copy_y >= 0:
                if self.__board[copy_y][copy_x] == str(self.__nowTurn):
                    count += 1
                    copy_x -= 1
                    copy_y -= 1
                else:
                    break
            ## 右下
            copy_x = x + 1
            copy_y = y + 1

            while copy_x < self.__size and copy_y < self.__size:
                if self.__board[copy_y][copy_x] == str(self.__nowTurn):
                    count += 1
                    copy_x += 1
                    copy_y += 1
                else:
                    break
            
            print("Debug : count = {}".format(count))
            if count >= self.__winCondi:
                self.__winner = name
                return self.__winner

            count = 1

            # 上 & 下
            ## 上
            copy_x = x
            copy_y = y - 1
            while copy_y >= 0:
                if self.__board[copy_y][copy_x] == str(self.__nowTurn):
                    count += 1
                    copy_y -= 1
                else:
                    break
            ## 下
            copy_x = x
            copy_y = y + 1

            while copy_y < self.__size:
                if self.__board[copy_y][copy_x] == str(self.__nowTurn):
                    count += 1
                    copy_y += 1
                else:
                    break

            print("Debug : count = {}".format(count))
            if count >= self.__winCondi:
                self.__winner = name
                return self.__winner

            count = 1


            # 右上 & 左下
            ## 右上
            copy_x = x + 1
            copy_y = y - 1
            while copy_x < self.__size and copy_y >= 0:
                if self.__board[copy_y][copy_x] == str(self.__nowTurn):
                    count += 1
                    copy_x += 1
                    copy_y -= 1
                else:
                    break
            ## 左下
            copy_x = x - 1
            copy_y = y + 1

            while copy_x >= 0 and copy_y < self.__size:
                if self.__board[copy_y][copy_x] == str(self.__nowTurn):
                    count += 1
                    copy_x -= 1
                    copy_y += 1
                else:
                    break
            
            print("Debug : count = {}".format(count))
            if count >= self.__winCondi:
                self.__winner = name
                return self.__winner

            count = 1

            #左&右
            ## 左
            copy_x = x - 1
            copy_y = y
            while copy_x >= 0:
                if self.__board[copy_y][copy_x] == str(self.__nowTurn):
                    count += 1
                    copy_x -= 1
                else:
                    break
            ## 右
            copy_x = x + 1
            copy_y = y

            while copy_y < self.__size:
                if self.__board[copy_y][copy_x] == str(self.__nowTurn):
                    count += 1
                    copy_x += 1
                else:
                    break

            print("Debug : count = {}".format(count))
            if count >= self.__winCondi:
                self.__winner = name
                return self.__winner

            count = 1

            # 棋盤全掃
            ## 看是否棋盤全滿，若全滿就是平手
            for i in range(0, self.__size):
                for j in range(0, self.__size):
                    text = self.__board[i][j]
                    if text == "EMPTY":
                        self.__winner = "NOT_YET"
                        return "NOT_YET"
            
            self.__winner = "TIE"
            
            return "TIE"

        else:
            return "HAS_WINNER"

    def getGameOver(self) -> bool:
        return self.__gameOver

    def setGameOver(self) -> bool:
        self.__gameRunning = False
        self.__gameOver = True
        for name in self.__playerNameList.keys():
            self.__playerNameList[name] = "N"

    def forceGameOver(self):
        self.setGameOver()
        self.__winner = "FORCE_GAMEOVER"

    def resetGame(self):
        self.__initRoom()
