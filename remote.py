import sys
import threading
import pexpect
from collections import namedtuple

Song = namedtuple('Song', [ 'title', 'artist', 'album'])

def list_builder(func):
    return lambda l: list(func(l))

@list_builder
def get_quoted_items(line):
    in_quote = False

    current_string = ''

    for c in line:
        # invert in_quote if we hit a quote

        if in_quote:
            if c != '"':
                current_string += c
            else:
                yield current_string

        in_quote = c == '"' ^ in_quote


class Pianobar:
	"""docstring for Pianobar"""

	def __init__(self):
		self.station_name = ''
		self.current_track = None

		self.proc = pexpect.spawnu('pianobar')

		readthread = threading.Thread(target=self.follow_output)
		readthread.daemon = True
		readthread.start()

	def follow_output(self):
		while True:
			try:
				line = self.proc.readline()
				self.interpret_output(line)
				print(line, end='')

			except pexpect.exceptions.TIMEOUT:
				pass

	def interpret_output(self, output):
		if line.startswith('|>'):
			data = line.split(' ')
			if data[0] != 'Station':
				self.current_track = Song(get_quoted_items(line))


	def send_command(self, cmd):
		self.proc.write(cmd+'\n')

    def play(self):
        self.send_command('P')
    
    def pause(self):
        self.send_command('S')

def main():
	p = Pianobar()
	while p.proc.isalive():
		x = input('')
		p.send_command(x)
		if(x == 'q'):
			break


if __name__ == '__main__':
	main()

