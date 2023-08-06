# Standard lib imports
import platform

# Local imports
if platform.system() == "Linux":
    import qwilfish.linux_socket as socket
elif platform.system() == "Windows":
    import qwilfish.win_socket as socket
else:
    raise SystemError("Unsupported system for creating sockets: " + platform.system())

class Socket():

    def __init__(self, interface):
        self.sock = socket.create(interface)

    def send(self, frame):
       return socket.send(frame, self.sock)
