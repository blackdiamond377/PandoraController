import sys
import pexpect

class Pianobar:
	"""docstring for Pianobar"""

	def __init__(self):
		self.proc = pexpect.spawnu('pianobar')
		#self.proc.logfile = sys.stdout


	def follow_output(self):
		while True:
			line = self.proc.readline()
			print(line, end='')



def main():
	p = Pianobar()
	p.follow_output()


if __name__ == '__main__':
	main()