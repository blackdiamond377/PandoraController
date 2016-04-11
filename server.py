import socket
import threading
import json

# internal packages
import opcodes
import remote

class ClientHandler(threading.Thread):
    def __init__(self, server, sock, addr, *args, **kwargs):
        super(ClientHandler, self).__init__(*args, **kwargs)
        self.addr = addr
        self.sock = sock
        self.server = server
        self.pandora = pandora = server.pandora
        self.current_song = self.pandora.current_track

        self.opcode_map = {
            opcodes.PLAY:           pandora.play,
            opcodes.PAUSE:          pandora.pause,
            opcodes.NEXT:           pandora.next,
            opcodes.SELECT_STATION: self.select_station,
        }

    def run(self):
        self.listen()

    def listen(self):
        while self.server.running:
            opcode = self.sock.recv(1)
            if opcode == b'':
                print('Connection to client at {} broken.'.format(self.addr))
                break

            if opcode == opcodes.QUIT:
                self.sock.send(opcodes.QUIT)
                print('Connection to client at {} severed.'.format(self.addr))
                break

            print('Received op {} from {}'.format(str(opcode), self.addr))

            # Handle opcode functionality
            self.sock.send(opcodes.ACK)
            self.opcode_map[opcode]()

            if self.current_song != self.pandora.current_track:
                self.notify_new_song()
                self.current_song = self.pandora.current_track

        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def recv_arg(self, length):
        arg = self.sock.recv(length)
        print('Received argument {} from {}'.format(arg, self.addr))
        self.sock.send(opcodes.ACK)
        return arg

    def select_station(self):
        station_index = int.from_bytes(self.recv_arg(1), byteorder='big')
        self.pandora.select_station(station_index)

    def notify_new_song(self):
        self.sock.send(opcodes.GET_SONG)
        ack = self.sock.recv(1)

        try:
            serialized_song = json.dumps(self.pandora.current_track).encode()
            length = len(serialized_song)

            self.sock.send(length.toBytes(1, byteorder='big'))
        except OverflowError:
            print('Song didn\'t parse correctly. (Too long?)')

        ack = self.sock.recv(1)
        self.sock.sendall(serialized_song)
        ack = self.sock.recv(1)


class Server:
    def __init__(self):
        """ TCP Server for clients to connect to for controlling Pandora """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 8000))
        self.socket.listen(5) # keep a backlog of up to 5 clients waiting
        self.pandora = remote.Pianobar()
        self.running = True

        try:
            self.mainloop()
        finally:
            # Gracefully shutdown and unbind the port
            self.quit()

    def mainloop(self):
        while self.running:
            ClientHandler(self, *self.socket.accept()).start()

    def quit(self):
        self.running = False
        self.socket.shutdown(socket.SHUT_RDWR)


def main():
    Server()

if __name__ == '__main__':
    main()

