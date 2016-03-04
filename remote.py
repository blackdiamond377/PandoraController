
import os
import threading
import shlex
import subprocess


from collections import namedtuple

Song = namedtuple('Song', ['title', 'artist', 'album'])


class PianoBar:
    def __init__(self):

        # Hides console window
        #startupinfo = subprocess.STARTUPINFO()
        #startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        cmdline = 'pianobar'
        args = shlex.split(cmdline)

        self.reading = True

        self.process = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        readthread = threading.Thread(target=self.readLoop)
        readthread.daemon = True
        readthread.start()
        
    def sendCommand(self, cmd):
        try:
            self.process.communicate((cmd+'\n').encode('UTF-8', errors='ignore'), timeout=0.1)
        except subprocess.TimeoutExpired:
            pass

    def readLoop(self):
        songname = ''
        _mainthread = threading.main_thread()
        while self.reading:
            line = self.process.stdout.readline().decode("utf-8", errors='ignore')

            print(line, end='')

            if line == '':
                print('Everything is broken')

            if not(_mainthread.is_alive()):
                self.process.kill()
                break

    def kill(self):
        self.process.kill()


def main():
    p = PianoBar()

    while True:
        x = input('')
        if x == 'q':
            p.kill()
            break
        p.sendCommand(x)
        print('command sent')


if __name__ == '__main__':
    main()
