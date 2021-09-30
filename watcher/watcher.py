from .helper import displayFrame, recvFrame
from .constants import *
import cv2
import socket


def connectToServer(ip = SHARER_IP, port = SHARER_PORT):
    """
    Connects to the server
    """

    global SHARER_IP, SHARER_PORT
    
    SHARER_IP = ip
    SHARER_PORT = port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((SHARER_IP, SHARER_PORT))

    # Starts watching
    watchScreen(soc)


def watchScreen(soc):
    global SCREEN_SHARING_WIDTH, SCREEN_SHARING_HEIGHT
    
    """
    Starts watching the screen
    """
    
    # Some initial things


    # Recv the len of the screen resolution string (we receiving the len of the screen resultion string only as 1 byte
    # because the len will not be bigger than 1 byte presentation ability (0 - 128)
    screenResolutionLen = int.from_bytes(soc.recv(1), 'big') 

    # Recv the screen resolution of the shared screen
    SCREEN_SHARING_WIDTH, SCREEN_SHARING_HEIGHT = soc.recv(screenResolutionLen).decode().split(' ')

    # Convert the screen size from str to int
    SCREEN_SHARING_WIDTH = int(SCREEN_SHARING_WIDTH)
    SCREEN_SHARING_HEIGHT = int(SCREEN_SHARING_HEIGHT)

    print(
        f"Start watching on {SCREEN_SHARING_WIDTH}:{SCREEN_SHARING_HEIGHT}")

    while True:
        frame = recvFrame(soc, SCREEN_SHARING_WIDTH, SCREEN_SHARING_HEIGHT)
        displayFrame(frame, "screenSharing")

        if cv2.getWindowProperty("screenSharing", cv2.WND_PROP_VISIBLE) <1:
            print("Screen sharing window has been closed")
            break


def main(ip = SHARER_IP, port = SHARER_PORT):
    global SHARER_IP, SHARER_PORT
    
    SHARER_IP = ip
    SHARER_PORT = port

    connectToServer()


if __name__ == "__main__":
    main()
