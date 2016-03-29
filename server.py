import socket
import threading

# internal packages
import opcodes
import remote

class Server:
    def __init__(self):
        """ TCP Server for clients to connect to for controlling Pandora """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 8000))
        self.socket.listen(5) # keep a backlog of up to 5 clients waiting
        self.pandora = remote.Pianobar()
        self.running = True

        self.opcode_map = {
            opcodes.PLAY:           self.play,
            opcodes.PAUSE:          self.pause,
            opcodes.NEXT:           self.next,
            opcodes.SELECT_STATION: self.select_station,
            opcodes.QUIT:           self.quit
        }

        while self.running:
            (clientsock, addr) = self.socket.accept()
            clientthread = threading.Thread(target=self.receive, args=(clientsock,))
            clientthread.start()

    def receive(self, sock):
        while self.running:
            opcode = sock.recv(1)
            if opcode == b'':
                print('Connection to client broken...')
                break

            if opcode == opcodes.QUIT:
                sock.send(opcodes.QUIT)
                print('Connection to client severed.')
                break

            print('Received op', opcode)
            self.opcode_map[opcode](sock)

        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

    def play(self, sock):
        self.pandora.play()
        sock.send(opcodes.ACK)

    def pause(self, sock):
        self.pandora.pause()
        sock.send(opcodes.ACK)

    def next(self, sock):
        self.pandora.next()
        sock.send(opcodes.ACK)

    def select_station(self, sock):
        """ Receive the station number and pass it to the Pianobar controller """
        self.pandora.send_command('s', end='') # Send station select
        sock.send(opcodes.ACK)
        station_index = sock.recv(1)
        sock.send(opcodes.ACK) # Tell client we're ready for the id
        self.pandora.send_command(int.from_bytes(station_index,
            byteorder='big')) # Send station id
        sock.send(opcodes.ACK)

    def quit(self, sock):
        sock.send(opcodes.QUIT)
        self.pandora.send_command('q')
        self.running = False

def main():
    Server()

if __name__ == '__main__':
    main()

