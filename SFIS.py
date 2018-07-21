from MySFIS import SFISWebService
from data import *
import threading
import dialog

lock = threading.Lock()

class SFIS():
	def __init__(self):
		# DATA.Readini()
		self.dlg = dialog.dialog('')
		self.sfis = SFISWebService(DATA.sfis_url, DATA.DEVICE_ID, DATA.sfis_tsp)

	def SFIS_LOGIN_DB(self):
		if not int(DATA.STATION_ONLINE):
			DATA.op('SFIS_LOGIN_DB,0,PASS,N/A,N/A')
			return

		try:
			lock.acquire()
			logV('lock.acquire')

			logV(self.sfis.SFIS_Connect())
			r, s = self.sfis.SFIS_Login(DATA.OPID, '1')
			logV(r, repr(s))
			if r == '1' or s.find('Login Twice') >= 0:
				DATA.op('SFIS_LOGIN_DB,0,PASS,N/A,N/A')
			else:
				DATA.op('SFIS_LOGIN_DB,1,FAIL,N/A,N/A')
		except Exception as e:
			logE(Exception, e)
		finally:
			lock.release()
			logV('lock.release\n')

	def SFIS_CHECK_ROUTE(self, argv):
		if not int(DATA.STATION_ONLINE):
			DATA.op('SFIS_STATION_INPUT_CHECK,0,PASS,N/A,N/A')
			return

		try:
			lock.acquire()
			logV('lock.acquire')

			r,s = self.sfis.SFIS_CheckRoute(argv)
			logV(r, repr(s))

			if r == '1':
				DATA.op('SFIS_STATION_INPUT_CHECK,0,PASS,N/A,N/A')
				return
			if r == '0' and 'REPAIR OF' in s:
				t = GetMiddleStr(s, 'LF#:', ']')
				try:
					int(t)
				except:
					t = '0'
				if int(DATA.repair) and int(DATA.repair) <= int(t):
					self.dlg.info({'msg': 'OVER REPAIR COUNT = %s' % t})
					DATA.op('SFIS_STATION_INPUT_CHECK,1,FAIL,N/A,N/A')
					return

				if DATA.AAB == 'YES':
					r, s = self.sfis.SFIS_GetVersion(argv, 'MO_D', 'DEVICE')
					log(r, repr(s))
					if r != '1' or s.find('DATA GET OK') == -1:
						self.dlg.info({'msg': 'get device fail'})
						DATA.op('SFIS_STATION_INPUT_CHECK,1,FAIL,N/A,N/A')
						return

					items = s.split(chr(127))
					try:
						predeviceid = items[1]
					except:
						predeviceid = 'UNKNOW'

					if predeviceid == DATA.DEVICE_ID and int(t)%2 == 1:
						self.dlg.info({'msg': 'AAB:should not test on device:%s'%predeviceid})
						DATA.op('SFIS_STATION_INPUT_CHECK,1,FAIL,N/A,N/A')
						return
					elif predeviceid != DATA.DEVICE_ID and int(t)%2 == 0:
						self.dlg.info({'msg': 'AAB:should test on device:%s' % predeviceid})
						DATA.op('SFIS_STATION_INPUT_CHECK,1,FAIL,N/A,N/A')
						return

				r, s = self.sfis.SFIS_Repair(argv)
				logV(r, repr(s))
				if r == '1':
					r,s = self.sfis.SFIS_CheckRoute(argv)
					logV(r, repr(s))
					if r == '1':
						DATA.op('SFIS_STATION_INPUT_CHECK,0,PASS,N/A,N/A')
						return

			self.dlg.info({'msg':s})
			DATA.op('SFIS_STATION_INPUT_CHECK,1,FAIL,N/A,N/A')
			return

		except Exception as e:
			logE(Exception, e)
			DATA.op('SFIS_STATION_INPUT_CHECK,1,FAIL,N/A,N/A')
		finally:
			lock.release()
			logV('lock.release\n')

	def BUILD_PHASE(self, argv):
		if not int(DATA.STATION_ONLINE):
			DATA.op('BUILD_PHASE,0,PASS,N/A,N/A')
			return

		try:
			lock.acquire()
			logV('lock.acquire')

			for i in range(3):
				r, s = self.sfis.SFIS_GetVersion(argv, 'GET_CONFIG', 'MO_MEMO', 'MEMOCLS,RSDATE')
				logV(r, repr(s))
				if r == '1':
					break
				else:
					logV('retry')

			if r == '1':
				items = s.split(chr(127))
				if len(items) > 3 and len(items[2]) > 0:
					DATA.op('BUILD_PHASE,0,' + items[2] + ',N/A,N/A')
					# DATA.build_phase=items[2]
					return
			DATA.op('BUILD_PHASE,1,FAIL,N/A,N/A')
		except Exception as e:
			logE(Exception, e)
		finally:
			lock.release()
			logV('lock.release\n')

	def TEST_READ_FACTORY_CONFIG_MLB(self, argv):
		if not int(DATA.STATION_ONLINE):
			DATA.op('TEST_READ_FACTORY_CONFIG_MLB,0,PASS,N/A,N/A')
			return

		try:
			lock.acquire()
			logV('lock.acquire')

			for i in range(3):
				r, s = self.sfis.SFIS_GetVersion(argv, 'GET_CONFIG', 'MO_MEMO')
				logV(r, repr(s))

				if r == '1':
					break
				else:
					logV('retry')

			if r == '1':
				items = s.split(chr(127))
				if len(items) > 3 and len(items[1]) > 0:
					DATA.op('TEST_READ_FACTORY_CONFIG_MLB,0,' + items[1] + ',N/A,N/A')
					# DATA.mlbconfig = items[1]
					return
			DATA.op('TEST_READ_FACTORY_CONFIG_MLB,1,FAIL,N/A,N/A')
		except Exception as e:
			logE(Exception, e)
		finally:
			lock.release()
			logV('lock.release\n')

	def SFIS_UPLOAD_TEST_RESULT(self, argv):
		if not int(DATA.STATION_ONLINE):
			DATA.op('SFIS_UPLOAD_TEST_RESULT,0,PASS,N/A,N/A')
			return

		try:
			lock.acquire()
			logV('lock.acquire')

			DATA.create_streamData()
			r, s = self.sfis.SFIS_TestResult(argv, DATA.errorcode, DATA.logStreamData)
			logV(r, repr(s))
			if r == '0':
				DATA.op('SFIS_UPLOAD_TEST_RESULT,1,FAIL,N/A,N/A')
			else:
				DATA.op('SFIS_UPLOAD_TEST_RESULT,0,PASS,N/A,N/A')
		except Exception as e:
			logE(Exception, e)
		finally:
			lock.release()
			logV('lock.release\n')

	def SFIS_LOGIN_OUT(self):
		DATA.op('SFIS_LOGIN_OUT,0,PASS,N/A,N/A')


def GetMiddleStr(content, startStr, endStr):
    startIndex = content.index(startStr)
    if startIndex >= 0:
        startIndex += len(startStr)
        endIndex = content.index(endStr, startIndex)
        return content[startIndex:endIndex]
    else:
        return ''


if __name__ == '__main__':
	sfis = SFIS()
	sfis.SFIS_LOGIN_DB()

