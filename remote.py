
import os
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

        self.readLoop()

        print(input(''))
        
    def sendCommand(self, cmd):
        p.communicate(input=cmd)

    def readLoop(self):
        songname = ''
        while self.reading:
            line = self.process.stdout.readline().decode("utf-8", errors='ignore')

            print(line, end='')



            if line == '':
                break


def main():
    p = PianoBar()

if __name__ == '__main__':
    main()