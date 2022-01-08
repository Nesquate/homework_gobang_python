import sys, socket
import server, player, lobby

def main():
    if len(sys.argv) < 3:
        print("Usage : {} <ADDR> <PORT>".format(sys.argv[0]))
        exit(1)

    try:
        mainServer = server.Server(sys.argv[1], int(sys.argv[2]))
        globalLobby = lobby.Lobby()
        print("Established server socket!")
        print("IP : {}, PORT : {}".format(sys.argv[1], sys.argv[2]))
        print("Press [CTRL+C] to stop this server.")
        countThread = 0
        while True:
            client = mainServer.accept()
            playerThread = player.Player(countThread, client, globalLobby)
            countThread += 1
        
    except socket.error as serverError:
        print("Failed to run server!")
        print("Details : ")
        print(serverError)
        exit(2)

    except (KeyboardInterrupt, SystemExit):
        print("Close server.")
        mainServer.closeServer()
        exit(0)

    except Exception as otherError:
        print("Occurred other error(s)!")
        print("Details : ")
        print(otherError)
        exit(3)

if __name__ == "__main__":
    main()