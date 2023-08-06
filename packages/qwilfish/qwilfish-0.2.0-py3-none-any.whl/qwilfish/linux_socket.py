# Standard lib imports
import socket

def create(interface):
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    sock.bind((interface, 0))
    return sock

def send(frame, sock):
    return sock.send(frame)
