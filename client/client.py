from zlib import decompress
import cv2
import constants
import socket
import constants
from mss import screenshot
import numpy as np
import pygame


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
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((constants.HOST_IP, constants.HOST_PORT))

    # Starts watching
    startWatching(soc)


def startWatching(soc):

    # Some initial things
    # Recv the screen size of the sharing
    constants.SCREEN_SHARING_WIDTH, constants.SCREEN_SHARING_HEIGHT = soc.recv(
        1024).decode().split(' ')

    # Convert the screen size from str to int
    constants.SCREEN_SHARING_WIDTH = int(constants.SCREEN_SHARING_WIDTH)
    constants.SCREEN_SHARING_HEIGHT = int(constants.SCREEN_SHARING_HEIGHT)

    print(
        f"Starting watch on {constants.SCREEN_SHARING_WIDTH}:{constants.SCREEN_SHARING_HEIGHT}")

    while True:
        frame = recvFrame(soc)
        displayFrame(frame)


def recvFrame(soc):
    # Retreive the size of the pixels length, the pixels length and pixels
    size_len = int.from_bytes(soc.recv(1), byteorder='big')
    size = int.from_bytes(soc.recv(size_len), byteorder='big')
    framePixels = decompress(recvall(soc, size))

    return screenshot.ScreenShot(framePixels, {'top': 0, 'left': 0,
                                               'width': constants.SCREEN_SHARING_WIDTH, 'height': constants.SCREEN_SHARING_HEIGHT})


def displayFrame(frame):
    mat = np.array(frame)
    cv2.imshow("screenSharing", mat)
    cv2.waitKey(1)


def main():
    connectToServer()


if __name__ == "__main__":
    main()
