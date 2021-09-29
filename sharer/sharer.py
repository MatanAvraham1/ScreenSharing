from constants import *
import socket
import threading
import mss
from zlib import compress

connectedClients = 0

def startServer():
    global connectedClients

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
    soc.send(f"{SCREEN_WIDTH} { SCREEN_HEIGHT}".encode())

    # Starts sends frames
    while True:
        frame = getFrame()
        try:
            sendFrame(soc, frame)
            
        except socket.error as e: # If the client has been disconnected
            print(f"{soc.getsockname()} Client has been disconnected!") 
            connectedClients -= 1
            break

def sendFrame(sock, frame):
    """
    Sends the frame to the client

    param 1: the socket connection
    param 2: the frame to send

    param 1 type: socket.socket
    param 2 type: mss.screenshot.Screenshot

    How the sending is done:

    Compresses the rgb pixels of the frame  
    Computes the length of the compressed rgb bytes array
    Computes how much bits needed to presents the length of the compressed rgb bytes array

    Sends the bits number
    Sends the actual length of the pixels
    Sends the actual pixels
    """

    # Compressed the rgb pixels of the image
    compressedImg = compress(frame.bgra, 6)

    # Send the size of the pixels length

    # The len of the [compressedImg] bytes array
    compressedPixelsLen = len(compressedImg)
    # How much bits needed to presents [compressedPixelsLen]
    # TODO: check the + 7 // 8 meaning
    compressedPixelsLen_bitsLen = (compressedPixelsLen.bit_length() + 7) // 8
    # Sends [compressedPixelsLen_bitsLen]
    sock.send(bytes([compressedPixelsLen_bitsLen]))

    # Send the actual pixels length
    size_bytes = compressedPixelsLen.to_bytes(
        compressedPixelsLen_bitsLen, 'big')
    sock.send(size_bytes)

    # Send pixels
    sock.sendall(compressedImg)


def getFrame():
    with mss.mss() as sct:
        monitor = {'top': 0, 'left': 0,
                   'width':  SCREEN_WIDTH, 'height': SCREEN_HEIGHT}

        return sct.grab(monitor)


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
