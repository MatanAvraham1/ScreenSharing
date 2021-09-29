from pyautogui import size

SHARER_IP = "127.0.0.1"
SHARER_PORT = 44444

SCREEN_WIDTH = size().width
SCREEN_HEIGHT = size().height

MAX_CONNECTED_CLIENTS = 5555 # How much clients allowed to connect in parallel
ONLY_ONE_CONNECTION = False # If True - the host will accept only 1 client and after the client will disconnect the program will exit