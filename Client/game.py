class Game:
    def __init__(self):
        self.__board: list = None
        self.__id: str = None
        self.__turn: int = 0
        self.__size: int = 0

    def getBoard(self) -> list:
        return self.__board

    def getID(self) -> str:
        return self.__id

    def getTurn(self) -> int:
        return self.__turn

    def getSize(self) -> int:
        return self.__size

    def setBoard(self, board: list):
        self.__board = board

    def setID(self, id: str):
        self.__id = id

    def setTurn(self, turn: int):
        self.__turn = turn

    def setSize(self, size: int):
        self.__size = size