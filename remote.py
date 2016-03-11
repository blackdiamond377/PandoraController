import sys
import threading
import pexpect

class Pianobar:
	"""docstring for Pianobar"""

	def __init__(self):
		self.proc = pexpect.spawnu('pianobar')
		
		readthread = threading.Thread(target=self.follow_output)
		readthread.daemon = True
		readthread.start()

	def follow_output(self):
		while True:
			try:
				line = self.proc.readline()
				print(line, end='')

			except pexpect.exceptions.TIMEOUT:
				pass

	def send_command(self, cmd):
		self.proc.write(cmd+'\n')


def main():
	p = Pianobar()
	while p.proc.isalive():
		x = input('')
		p.send_command(x)
		if(x == 'q'):
			break


if __name__ == '__main__':
	main()