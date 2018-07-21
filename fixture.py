from data import *
import serial, time

class Fixture:
	def __init__(self):
		DATA.Readini()
		try:
			self.comport = DATA.ComPort
		except Exception as e:
			logE(Exception, e)

		self.baudrate = int(DATA.Baudrate)
		self.parity = serial.PARITY_NONE

	def connect(self):
		try:
			self.com = serial.Serial(self.comport, self.baudrate, parity = self.parity , timeout = 0)
			logV(self.comport, 'connected')

		except Exception as e:
			logE(Exception, e)

	def sendcmd(self, cmd, end, timeout = 3):
		try:
			self.com.write(cmd.encode('ascii'))
			buf = ''
			t0 = time.time()
			while time.time() - t0 < timeout:
				buf += self.com.readall()
				if buf.endswith(end):
					return True, buf
			return False, buf
		except Exception as e:
			logE(Exception, e)
			return False, e


	def fixturein(self):
		r, v = self.sendcmd('$in#', 'in pass\r')
		logV(r, repr(v))

	def fixtureout(self):
		r, v = self.sendcmd('$out#', 'out pass\r')
		logV(r, repr(v))


if __name__ == '__main__':
	f = Fixture()
	f.connect()
	f.fixturein()
