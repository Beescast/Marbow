#-*- coding: utf-8 -*-
import socket
import time
from packet import Packet
from message import Message
import threading

MAX_RECV_SIZE = 9999

class Client:
    def __init__(self, host, port):
        self.s = socket.create_connection((host, port))
        self.buff = None
        self.msg_buff = None

        # Lock for avoiding race conditions when sending packets
        self.send_lock = threading.Lock()

    def receive(self):

        self.buff = ''
        self.msg_buff = ''

        while True:

            data = self.s.recv(MAX_RECV_SIZE)

            if not data:
                time.sleep(0.01)
                continue

            self.buff += data

            while True:

                packet = Packet.sniff(self.buff)
                if packet is None:
                    break

                # Slice buffer
                self.buff = self.buff[packet.size():]

                # Append text data
                self.msg_buff += packet.body

                while True:

                    message = Message.sniff(self.msg_buff)
                    if message is None:
                        break

                    # Slice message buffer
                    self.msg_buff = self.msg_buff[(message.size() + 1):]  # +1 means to skip '\0' in the end

                    yield message
    def send(self, message_body):
        self.send_lock.acquire()
        try:
            self.s.send(Packet(Message(message_body).to_text()).to_raw())
        finally:
            self.send_lock.release()