from zlib import compress
import mss
from pyautogui import size

def getFrame():
    SCREEN_WIDTH = size().width
    SCREEN_HEIGHT = size().height

    with mss.mss() as sct:
        monitor = {'top': 0, 'left': 0,
                   'width':  SCREEN_WIDTH, 'height': SCREEN_HEIGHT}

        return sct.grab(monitor)


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