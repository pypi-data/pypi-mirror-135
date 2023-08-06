# Local imports
from qwilfish.socket import Socket

class SocketCourier():
    '''Delivers fuzz data to a system by writing to a raw socket.'''

    def __init__(self, interface="lo"):
        self.sock = Socket(interface)

    def deliver(self, data):
        frame = []
        for byte in range(0, len(data), 8):
            frame.append(int(data[byte:byte+8], 2))

        frame = bytes(frame)

        return self.sock.send(frame)
