import socket

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
            self.receive()

    def receive(self):
        opcode = self.clientsock.recv(1)
        print('Receved op', opcode)
        self.opcode_map[opcode]()
        self.socket.send("OK")

    def select_station(self):
        """ Receive the station number and pass it to the Pianobar controller """
        station_index = self.socket.recv(1)
        self.pandora.sendMessage(int(station_index))

    def quit(self):
        self.pandora.sendMessage('q')
        self.running = False

def main():
    Server()

if __name__ == '__main__':
    main()

