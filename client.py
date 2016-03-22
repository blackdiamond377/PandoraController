import socket

#internal packages
import opcodes

class Client:
    def __init__(self):
        """ TCP Client for controlling Pandora """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("localhost", 8000))

        self.running = True

        self.run()

    def run(self):
        while self.running:
            x = input(">").split(" ", 1)
            op = x[0]
            if len(x) > 1:
                args = x[1]

            op = get_opcode(x)

            print(op + ", " + args)

    def get_opcode(op):
        opcode_map = {
            'P':  opcodes.PLAY,
            'S':  opcodes.PAUSE,
            'n':  opcodes.NEXT,
            'ss': opcodes.SELECT_STATION,
            'q':  opcodes.QUIT
        }

        return opcode_map[op]

def main():
    Client()

if __name__ == "__main__":
    main()