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
        self.socket.listen(5) # keep a backlock of up to 5 clients waiting
        self.pandora = remote.Pianobar()
        self.running = True

        self.opcode_map = {
            opcodes.PLAY:           self.pandora.play,
            opcodes.PAUSE:          self.pandora.pause,
            opcodes.NEXT:           self.pandora.next,
            opcodes.SELECT_STATION: self.select_station,
            opcodes.QUIT:           self.quit
        }

        while self.running:
            (self.clientsock, addr) = self.socket.accept()
            clientthread = threading.Thread(target=self.receive, args=(self.clientsock,))
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
            self.opcode_map[opcode]()
            sock.send(opcodes.ACK)

    def select_station(self):
        """ Receive the station number and pass it to the Pianobar controller """
        self.clientsock.send(opcodes.ACK)
        self.pandora.send_command('s', end='') # Send station select
        station_index = self.clientsock.recv(1)
        self.clientsock.send(opcodes.ACK) # Tell client we're ready for the id
        self.pandora.send_command(int.from_bytes(station_index,
            byteorder='big')) # Send station id

    def quit(self):
        self.clientsock.send(opcodes.QUIT)
        self.pandora.send_command('q')
        self.running = False

def main():
    Server()

if __name__ == '__main__':
    main()

