from .helper import getFrame, sendFrame
from .constants import *
import socket
import threading

connectedClients = 0

def startServer(ip = SHARER_IP, port = SHARER_PORT):
    global connectedClients, SHARER_IP, SHARER_PORT

    SHARER_IP = ip
    SHARER_PORT = port

    print("Starting Server...")

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((SHARER_IP, SHARER_PORT))
    soc.listen()

    print("Waiting for clients...")

    # Accept clients
    while True:
        clientSocket, clientAddr = soc.accept()
        print(f"{clientAddr} has been connected!")

        if (ONLY_ONE_CONNECTION and connectedClients == 0) or connectedClients < MAX_CONNECTED_CLIENTS:  
            connectedClients += 1

            t = threading.Thread(target=shareScreen, args=(
                clientSocket,))
            t.start()

            if ONLY_ONE_CONNECTION and connectedClients == 1:
                t.join() # Waits to the thread to ending
                print("Closing becusae ONLY_ONE_CONNECTION is true!")
                exit(0)   

        else:
            clientSocket.close()

            if ONLY_ONE_CONNECTION and connectedClients == 1:
                print(f"{clientAddr} tried to connect but we becuase ONLY_ONE_CONNECTION is true we can accept only 1 client and there is already one connected!")

            elif (connectedClients == MAX_CONNECTED_CLIENTS):
                print(f"{clientAddr} tried to connect but we are already on the connected clients limit! connected clients:{connectedClients} limit:{MAX_CONNECTED_CLIENTS}")


def shareScreen(soc):
    global connectedClients

    # Send some initiation things

    # Sends the Width and Height of the screen sharing
    SCREEN_WIDTH = size().width
    SCREEN_HEIGHT = size().height

    screenResolution = f"{SCREEN_WIDTH} {SCREEN_HEIGHT}"
    # Sends the len of [screenResolution] as one byte (This len tells the client 
    # how much bytes recv from the socket to get [screenResolution] and not to blend with the other socket data)
    # We send the len only as 1 byte because the len will not be bigger than 1 byte presentation ability (0 - 128)
    soc.send(len(screenResolution).to_bytes(1, 'big')) 
    soc.send(screenResolution.encode()) # Sends the screen resulution

    # Starts sends frames
    while True:
        frame = getFrame()
        try:
            sendFrame(soc, frame)
            
        except socket.error as e: # If the client has been disconnected
            print(f"{soc.getsockname()} Client has been disconnected!") 
            connectedClients -= 1
            break



def main(ip = SHARER_IP, port = SHARER_PORT, max_connected_clients = MAX_CONNECTED_CLIENTS, only_one_connection = ONLY_ONE_CONNECTION):
    global SHARER_IP, SHARER_PORT, MAX_CONNECTED_CLIENTS, ONLY_ONE_CONNECTION
    SHARER_IP = ip
    SHARER_PORT = port
    MAX_CONNECTED_CLIENTS = max_connected_clients 
    ONLY_ONE_CONNECTION = only_one_connection

    if ONLY_ONE_CONNECTION:
        MAX_CONNECTED_CLIENTS = 1

    startServer()


if __name__ == "__main__":
    main()
