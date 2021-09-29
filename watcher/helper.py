from mss import screenshot
import numpy as np
from zlib import decompress
import cv2

def recvall(conn, length):
    """ Retreive all pixels. """

    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


def recvFrame(soc, SCREEN_SHARING_WIDTH, SCREEN_SHARING_HEIGHT):
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
                                               'width': SCREEN_SHARING_WIDTH, 'height': SCREEN_SHARING_HEIGHT})

def displayFrame(frame, windowName):
    """
    Displays the frame

    param 1: frame from the server screen
    """

    mat = np.array(frame)
    cv2.imshow(windowName, mat)
    cv2.waitKey(1)
