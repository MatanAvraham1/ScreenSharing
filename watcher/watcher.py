from watcher.helper import displayFrame, recvFrame
from constants import *
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
    # Recv the screen size of the sharing
    SCREEN_SHARING_WIDTH, SCREEN_SHARING_HEIGHT = soc.recv(
        1024).decode().split(' ')

    # Convert the screen size from str to int
    SCREEN_SHARING_WIDTH = int(SCREEN_SHARING_WIDTH)
    SCREEN_SHARING_HEIGHT = int(SCREEN_SHARING_HEIGHT)

    print(
        f"Starting watch on {SCREEN_SHARING_WIDTH}:{SCREEN_SHARING_HEIGHT}")

    while True:
        frame = recvFrame(soc, SCREEN_SHARING_WIDTH, SCREEN_SHARING_HEIGHT)
        displayFrame(frame, "screenSharing")

        if cv2.getWindowProperty("screenSharing", cv2.WND_PROP_VISIBLE) <1:
            print("Disconnecting...")
            break


def main(ip = SHARER_IP, port = SHARER_PORT):
    global SHARER_IP, SHARER_PORT
    
    SHARER_IP = ip
    SHARER_PORT = port

    connectToServer()


if __name__ == "__main__":
    main()
