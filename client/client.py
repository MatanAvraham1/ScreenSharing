import constants as sc
from zlib import decompress
import cv2
import socket
from mss import screenshot
import numpy as np

def recvall(conn, length):
    """ Retreive all pixels. """

    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


def connectToServer():
    """
    Connects to the server
    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((sc.HOST_IP, sc.HOST_PORT))

    # Starts watching
    startWatching(soc)


def startWatching(soc):
    """
    Starts watching the screen
    """

    # Some initial things
    # Recv the screen size of the sharing
    sc.SCREEN_SHARING_WIDTH, sc.SCREEN_SHARING_HEIGHT = soc.recv(
        1024).decode().split(' ')

    # Convert the screen size from str to int
    sc.SCREEN_SHARING_WIDTH = int(sc.SCREEN_SHARING_WIDTH)
    sc.SCREEN_SHARING_HEIGHT = int(sc.SCREEN_SHARING_HEIGHT)

    print(
        f"Starting watch on {sc.SCREEN_SHARING_WIDTH}:{sc.SCREEN_SHARING_HEIGHT}")

    while True:
        frame = recvFrame(soc)
        displayFrame(frame)


def recvFrame(soc):
    """
    Receives and returns frame from the socket

    param 1: the socket connection
    param 1 type: socket.socket

    return type: mss.screenshot.ScreenShot
    """

    # Retreive the size of the pixels length, the pixels length and pixels
    size_len = int.from_bytes(soc.recv(1), byteorder='big')
    size = int.from_bytes(soc.recv(size_len), byteorder='big')
    framePixels = decompress(recvall(soc, size))

    return screenshot.ScreenShot(framePixels, {'top': 0, 'left': 0,
                                               'width': sc.SCREEN_SHARING_WIDTH, 'height': sc.SCREEN_SHARING_HEIGHT})


def displayFrame(frame):
    """
    Displays the frame

    param 1: frame from the server screen
    """

    mat = np.array(frame)
    cv2.imshow("screenSharing", mat)
    cv2.waitKey(1)


def main(ip = sc.HOST_IP, port = sc.HOST_PORT):
    sc.HOST_IP = ip
    sc.HOST_PORT = port

    connectToServer()


if __name__ == "__main__":
    main()
