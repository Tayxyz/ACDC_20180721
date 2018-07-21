from data import *
import time, datetime
import uuid

class LocalLog:
	def __init__(self): pass
		# mkrdir()

	def basic(self, *argv):
		try:
			DATA.op('TEST,STATUS,VALUE,U_LIMIT,L_LIMIT')
			DATA.op('TEST_DATE_TIME,0,' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ',N/A,N/A')
			DATA.op('TEST_READ_ISN_MLB' + ',0,' + DATA.ISN[int(argv[0])-1] + ',N/A,N/A')
			DATA.op('STATION_NAME' + ',0,' + DATA.STATION_NAME + ',N/A,N/A')
			if DATA.STATION_ONLINE == '0':
				DATA.op('STATION_ONLINE' + ',0,' + '0' + ',N/A,N/A')
				DATA.op('STATION_MODE,0,OFFLINE,N/A,N/A')
			else:
				DATA.op('STATION_ONLINE' + ',0,' + '1' + ',N/A,N/A')
				DATA.op('STATION_MODE,0,ONLINE,N/A,N/A')

			DATA.op('USER_ID,0,' + DATA.OPID + ',N/A,N/A')
			DATA.op('LINE_NUMBER,0,1,N/A,N/A')
			DATA.op('BUILD_EVENT,0,' + DATA.BUILD_EVENT + ',N/A,N/A')
			DATA.op('FIXTURE_ID,0,' + DATA.FIXTURE_ID + ',N/A,N/A')
			DATA.op('FIXTURE_INDEX,0,' + argv[0] + ',N/A,N/A')
			DATA.op('DEVICE_ID,0,' + DATA.DEVICE_ID + ',N/A,N/A')
			DATA.op('STATION_MAC,0,' + self.getmacaddress()+',N/A,N/A')
			DATA.op('REL_STATUS,0,0,N/A,N/A')
			DATA.op('STATION_SW_VERSION,0,2.0.55.10,N/A,N/A')
			DATA.op('SCRIPT_VERSION,0,' + DATA.CHROMA_VERSION + ',N/A,N/A')
			DATA.op('LIMITS_VERSION,0,' + DATA.CHROMA_VERSION + ',N/A,N/A')
			DATA.op('TEST_READ_MODEL_MLB,0,' + DATA.MODEL_MLB + ',N/A,N/A')
			DATA.op('TEST_READ_FW_VERSION_MLB,0,PASS,N/A,N/A')
		except:
			logE('set LocalLog.basic() fail')
			return

		self.handleisn(DATA.ISN[int(argv[0])-1])

	def getmacaddress(self):
		mac = uuid.UUID(int = uuid.getnode()).hex[-12:].upper()
		return '%s:%s:%s:%s:%s:%s' % (mac[:2], mac[2:4], mac[4:6], mac[6:8],mac[8:10], mac[-2:])

	def handleisn(self, *argv):
		PRODUCT_NAME_DESC = {'21A':'M1','26A':'M1','26E':'TR1','26C':'TR1','22':'KR1'}
		PRODUCT_TYPE_DESC = {'A':'NA'}
		PRODUCT_CODE_DESC = {'22A':'KR1 FATP','21A': 'M1 FATP','26A': 'M1 FATP','21B': 'M1 MLB','21D': 'M1 Interface MLB','24A': 'TR1 FATP','21C': 'TR1 FATP','26C': 'TR1 FATP','24B': 'TR1 MLB','24D': 'TR1 Daughter MLB','26E': 'TR1 MLB'}
		PRODUCT_VERSION_DESC = {'A':'WHITE'}
		MFG_LOCATION_DESC = {'AB':'Pegatron Protek Shanghai','AC':'PEGATRON_MAINTEK_SUZHOU','RA':'Pegatron Protek Shanghai','RC':'Pegatron Maintek Suzhou'}

		isn_info = {}
		isn_info['PRODUCT_NAME'] = argv[0][0:2]
		isn_info['PRODUCT_TYPE'] = argv[0][2:3]
		isn_info['PRODUCT_CODE'] = argv[0][0:3]
		isn_info['PRODUCT_VERSION'] = argv[0][3:4]
		isn_info['PRODUCT_REVISION'] = argv[0][4:6]
		isn_info['MFG_LOCATION'] = argv[0][6:8]
		isn_info['MFG_WW'] = argv[0][8:10]
		isn_info['MFG_YEAR'] = argv[0][10:12]

		isn_info['PRODUCT_CODE_DESC'] = PRODUCT_CODE_DESC[isn_info['PRODUCT_CODE']]
		isn_info['PRODUCT_TYPE_DESC'] = isn_info['PRODUCT_CODE_DESC']
		isn_info['PRODUCT_NAME_DESC'] = PRODUCT_NAME_DESC[isn_info['PRODUCT_CODE']]
		isn_info['PRODUCT_VERSION_DESC'] = PRODUCT_VERSION_DESC[isn_info['PRODUCT_VERSION']]
		isn_info['MFG_LOCATION_DESC'] = MFG_LOCATION_DESC[isn_info['MFG_LOCATION']]

		DATA.op('PRODUCT_CODE' + ',0,' + isn_info['PRODUCT_CODE'] + ',N/A,N/A')
		DATA.op('PRODUCT_CODE_DESC' +  ',0,' + isn_info['PRODUCT_CODE_DESC'] + ',N/A,N/A')
		DATA.op('PRODUCT_NAME' +  ',0,' + isn_info['PRODUCT_NAME'] + ',N/A,N/A')
		DATA.op('PRODUCT_NAME_DESC' + ',0,' + isn_info['PRODUCT_NAME_DESC'] + ',N/A,N/A')
		DATA.op('PRODUCT_TYPE' +  ',0,' + isn_info['PRODUCT_TYPE'] + ',N/A,N/A')
		DATA.op('PRODUCT_TYPE_DESC' + ',0,' + isn_info['PRODUCT_TYPE_DESC'] + ',N/A,N/A')
		DATA.op('PRODUCT_VERSION' +  ',0,' + isn_info['PRODUCT_VERSION'] + ',N/A,N/A')
		DATA.op('PRODUCT_VERSION_DESC' +  ',0,' + isn_info['PRODUCT_VERSION_DESC'] + ',N/A,N/A')
		DATA.op('PRODUCT_REVISION' +  ',0,' + isn_info['PRODUCT_REVISION'] + ',N/A,N/A')
		DATA.op('MFG_LOCATION' +  ',0,' + isn_info['MFG_LOCATION'] + ',N/A,N/A')
		DATA.op('MFG_LOCATION_DESC' +  ',0,' + isn_info['MFG_LOCATION_DESC'] + ',N/A,N/A')
		DATA.op('MFG_WW' + ',0,'+ isn_info['MFG_WW'] + ',N/A,N/A')
		DATA.op('MFG_YEAR' +  ',0,' + isn_info['MFG_YEAR'] + ',N/A,N/A')




if __name__ == '__main__':
	pass


