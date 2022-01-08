import room

class Lobby:
    def __init__(self):
        self.__roomList: dict = dict()
        self.__roomListObj: dict = dict()
        self.__onlinePlayer: list = list()
        self.__nextID: int = 0

    def joinPlayer(self, name: str) -> bool:
        if name not in self.__onlinePlayer:
            self.__onlinePlayer.append(name)
            return True
        return False

    def removePlayer(self, name: str) -> bool:
        if name in self.__onlinePlayer:
            self.__onlinePlayer.remove(name)
            return True
        
        return False

    def createRoom(self, size: int, winCondi: int) -> str:
        id = str(self.__nextID)
        new_room = room.Room(id, size, winCondi)

        self.__roomList[id] = id
        self.__roomListObj[id] = new_room
        
        self.__nextID += 1

        return id

    def removeRoom(self, id: str, obj: room.Room):
        if id in self.__roomList:
            del self.__roomList[id]

        if id in self.__roomListObj:
            del self.__roomListObj[id]

    def getRoomObj(self, id: str) -> room.Room:
        return self.__roomListObj[id]

    def getRoomList(self) -> dict:
        return self.__roomList