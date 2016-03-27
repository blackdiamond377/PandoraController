import socket

#internal packages
import opcodes

class Client:
    def __init__(self):
        """ TCP Client for controlling Pandora """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("localhost", 8000))

        self.opcode_map = {
            'P': opcodes.PLAY,
            'S': opcodes.PAUSE,
            'n': opcodes.NEXT,
            'r': opcodes.SELECT_STATION,
            'q': opcodes.QUIT
        }

        self.running = True

        self.run()

    def run(self):
        while self.running:
            x = ''
            while x == '':
                x = input(">").split(" ", 1)
            op = x[0]
            if len(x) > 1:
                args = x[1]

            op = self.opcode_map[op]

            #print(op + ", " + args)
            self.socket.send(op)
            ack = self.socket.recv(1)
            if ack == opcodes.ACK:
                print('Received OK')
            elif ack == b'':
                print('Connection broken....')
                break
            else:
                print('Received ' + ack)


def main():
    Client()

if __name__ == "__main__":
    main()
