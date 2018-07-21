import configparser as cp
import time, os, datetime
import shutil

class Data():
	ini_time = time.time()

	def __init__(self):
		self.totalfails = 0
		self.test_failures = ''
		self.currentpass = True
		self.full_info = []
		self.errorcode = ''
		self.csv = []

	def Readini(self):
		try:
			config = cp.ConfigParser()
			config.read(DATA.settingpath)

			# SFIS
			DATA.sfis_url = config.get('SFIS', 'URL')
			DATA.sfis_tsp = config.get('SFIS', 'TSP')
			DATA.DEVICE_ID = config.get('SFIS', 'Device')
			DATA.STATION_ONLINE = config.get('SFIS', 'OnLine')  #  1 or  0
			DATA.repair = config.get('SFIS', 'Repair')
			try:
				DATA.AAB = config.get('SFIS', 'AAB')
			except:
				DATA.AAB = 'NO'


			DATA.chromalogpath = config.get('ChromaTxt', 'PATH')

			# INITIAL_SETTING
			DATA.STATION_NAME = config.get('INITIAL_SETTING', 'STATION_NAME')
			DATA.PROJECT_NAME = config.get('INITIAL_SETTING', 'PROJECT_NAME')
			DATA.LOG_DIRECTORY = config.get('INITIAL_SETTING', 'LOG_DIRECTORY')
			DATA.SERVER_LOG_DIRECTORY = config.get('INITIAL_SETTING', 'SERVER_LOG_DIRECTORY')
			DATA.SAVE_SERVER_LOG = config.get('INITIAL_SETTING', 'SAVE_SERVER_LOG')
			DATA.BUILD_EVENT = config.get('INITIAL_SETTING', 'BUILD_EVENT')
			DATA.FIXTURE_ID = config.get('INITIAL_SETTING', 'FIXTURE_ID')
			DATA.CHROMA_VERSION = config.get('INITIAL_SETTING', 'CHROMA_VERSION')
			DATA.CODE_VERSION = config.get('INITIAL_SETTING', 'CODE_VERSION')
			DATA.OPID = config.get('INITIAL_SETTING', 'OPID')
			DATA.WindowName = config.get('INITIAL_SETTING', 'WINDOWNAME')
			DATA.MODEL_MLB = config.get('INITIAL_SETTING', 'READ_MODEL_MLB')

			DATA.ComPort = config.get('Com', 'ComPort')
			DATA.Baudrate = config.get('Com', 'Baudrate')

			DATA.AutoTest = config.get('Auto', 'AutoTest')
		except:
			logE('Read setting.ini error')

	def op(self, content, csv = True, ):
		logV(content)
		items = content.split(',')

		if len(items) != 5:
			logE('The quantity of items is error')
			return
		else:
			items[2] = items[2].replace('"', '')

		cur = time.time()
		cost = cur - Data.ini_time
		Data.ini_time = cur
		content = ','.join(items)

		self.full_info.append(content + ',' + '%.2f' %cost)
		with open(DATA.csvfilepath, 'a') as fa:
			fa.write(content + ',' + '%.2f\n' % cost)

		if csv:
			self.csv.append(content)

	def readerrorcode(self, fail):
		try:
			with open('errorcode.txt') as f:
				for line in f:
					if fail in line:
						return line.strip().split()[1]
			return ''
		except:
			return ''

	def end(self, isn):
		final = 0
		fails = ''

		for line in self.csv:
			items = line.split(',')
			if items[1] == '1':
				final += 1
				if fails == '':
					fails = items[0]

		DATA.op('TEST_FAIL_ITEM_QTY' + ',0,' + str(self.totalfails) + ',N/A,N/A')
		if len(self.test_failures):
			DATA.op('TEST_FAILURES,0,' + str(DATA.test_failures) + ',N/A,N/A')
		else:
			DATA.op('TEST_FAILURES,0,NA,N/A,N/A')

		DATA.op('TEST_END_TIME,0,' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ',N/A,N/A')

		if final:
			# print(final, isn)
			pf = 'FAIL'
			self.errorcode = self.readerrorcode(fails)
			if len(self.errorcode) != 6:
				self.errorcode = 'WIETOR'
		else:
			pf = 'PASS'

		if int(DATA.STATION_ONLINE):
			onoffline = 'ON_LINE'
		else:
			onoffline = 'OFF_LINE'

		logV(DATA.PROJECT_NAME, ' ', DATA.BUILD_EVENT, ' ', DATA.STATION_NAME, ' ', DATA.DEVICE_ID, ' ', onoffline)

		if self.LOG_DIRECTORY.endswith(os.sep):
			self.LOG_DIRECTORY = self.LOG_DIRECTORY[:self.LOG_DIRECTORY.rindex(os.sep)]

		dirpath = DATA.PROJECT_NAME + os.sep + DATA.BUILD_EVENT + os.sep + DATA.STATION_NAME + os.sep + DATA.DEVICE_ID + os.sep + onoffline + os.sep + pf + os.sep + datetime.datetime.now().strftime('%Y%m%d')

		logdir = self.LOG_DIRECTORY + os.sep + dirpath
		logV(logdir)

		try:
			os.makedirs(logdir)
		except Exception as e:
			logD(Exception, e)

		if len(self.errorcode) == 6:
			errcode = self.errorcode + '_'
		else:
			errcode = ''

		filename = isn + '_' + errcode + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

		self.csvfilename = logdir + os.sep + filename + '.csv'
		self.cpkfilename = logdir + os.sep + filename + '.cpk'
		self.logfilename = logdir + os.sep + filename + '.txt'

		with open(self.csvfilename, 'w') as f:
			for line in self.csv:
				f.write(line)
				f.write('\n')

		with open(self.csvfilename, 'a') as f:
			f.write('SPC_RUN_ID,0,NA,N/A,N/A\n')
			self.op('SPC_RUN_ID,0,NA,N/A,N/A')
			f.write('SPC_ITERATION,0,0,N/A,N/A\n')
			self.op('SPC_ITERATION,0,0,N/A,N/A')

		if final:
			self.op('OVERALL_TEST_RESULT,1,FAIL,N/A,N/A')
			with open(self.csvfilename, 'a') as f:
				f.write('OVERALL_TEST_RESULT,1,FAIL,N/A,N/A')
		else:
			self.op('OVERALL_TEST_RESULT,0,PASS,N/A,N/A')
			with open(self.csvfilename, 'a') as f:
				f.write('OVERALL_TEST_RESULT,0,PASS,N/A,N/A')

		with open(self.cpkfilename, 'w') as f:
			for line in self.full_info:
				f.write(line)
				f.write('\n')

		with open(DATA.logfilepath, 'r') as fr:
			with open(self.logfilename, 'w') as fw:
				fw.write(fr.read())

		try:
			for file in self.morefiles:
				newfile = logdir + os.sep + file
				shutil.copy(file, newfile)
		except:
			pass

		# try:
		# 	directory = DATA.s

	def create_streamData(self):
		self.logStreamData = 'TEST,STATUS,VALUE,U_LIMIT,L_LIMIT\n'
		final = 0
		fails = ''

		for line in self.csv:
			items = line.split(',')
			if 'TEST_' in items[0]:
				if items[1] == '1':
					self.logStreamData += line + '\n'
					final += 1
					if fails == '':
						fails = items[0]
					break
		if final:
			self.errorcode = self.readerrorcode(fails)
			if len(self.errorcode) != 6:
				self.errorcode = 'WIETOR'
		else:
			self.errorcode = ''

		logV(self.errorcode)
		logV(self.logStreamData)




DATA = Data()
# DATA.logfilepath = '1.txt'
DATA.logfilepath = ''
DATA.settingpath = 'setting.ini'

if os.path.exists(DATA.logfilepath):
	os.remove(DATA.logfilepath)

def logV(*args):
    v = ' '.join([str(s) for s in args])
    with open(DATA.logfilepath,'a') as fa:
        fa.write('\n'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        fa.write('[verbose] ')
        fa.write(v)

def logE(*args):
    v = ' '.join([str(s) for s in args])
    with open(DATA.logfilepath,'a') as fa:
        fa.write('\n'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        fa.write('[error] ')
        fa.write(v)

def logD(*args):
    v = ' '.join([str(s) for s in args])
    with open(DATA.logfilepath,'a') as fa:
        fa.write('\n'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        fa.write('[debug] ')
        fa.write(v)

if __name__ == '__main__':
	DATA.Readini()
	print(DATA.Baudrate)
	# DATA.end('26EA01AC051802YX')
	# DATA.op('TEST,STATUS,VALUE,U_LIMIT,L_LIMIT')
	# DATA.op('TEST_DATE_TIME,1,' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ',N/A,N/A')
	# DATA.op('TEST_XXXX,1,' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ',N/A,N/A')

	# print(DATA.readerrorcode('TEST_C_T1_LOAD_NEUTRAL_DETECT'))

