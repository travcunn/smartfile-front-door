import time

from BreakfastSerial import Led


class Door(object):
    def __init__(self, board):
        self.relay = Led(board, 7)

    def unlock(self):
        self.relay.on()
        time.sleep(5)
        self.relay.off()
