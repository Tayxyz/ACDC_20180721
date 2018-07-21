from data import *
import win32gui, win32api, win32con
import time, os, threading
import localLog
import UI

class FindDlg:
	def __init__(self):
		DATA.Readini()
		self.ll = localLog.LocalLog()

		self.windowname = DATA.WindowName
		self.id = 0

	def sendISNtowindow(self):
		hld = win32gui.FindWindow(None, self.windowname)
		if hld > 0:
			btdlg = win32gui.FindWindowEx(hld, None, 'Button', None) # child
			# print('Button: %x' %btdlg)

			eddlg1 = win32gui.FindWindowEx(hld, None, 'Edit', None) # child
			# print('Edit: %x' %eddlg1)
			id = win32gui.GetDlgCtrlID(eddlg1)
			for i in range(6):
				if DATA.ISN[i]:
					win32api.SendMessage(win32gui.GetDlgItem(hld, id), win32con.WM_SETTEXT, 0, DATA.ISN[i])
				id += 1
		win32gui.SetForegroundWindow(btdlg)
		time.sleep(0.3)
		win32api.SendMessage(btdlg, win32con.WM_LBUTTONDOWN, 0, 0)
		time.sleep(0.3)
		win32api.SendMessage(btdlg, win32con.WM_LBUTTONUP, 0, 0)

	def searchwindow(self):
		hld = win32gui.FindWindow(None, self.windowname)
		while hld == 0:
			time.sleep(1)
			hld = win32gui.FindWindow(None, self.windowname)
		print('find window')

		self.sendISNtowindow()
		for i in DATA.ISN:
			if DATA.ISN[i]:
				print('send %s success' % DATA.ISN[i])

		self.WaitChromaTxt()

	def WaitChromaTxt(self):
		while not os.path.exists(DATA.chromalogpath): pass
		print('found txt')

		for i in DATA.ISN:
			if DATA.ISN[i]:
				self.firstfindISN = False
				self.final = True
				self.flag = True
				self.result = False
				self.find = False
				self.items_content = []
				self.id = i + 1
				DATA.totalfails = 0
				DATA.test_failures = ''
				DATA.errorcode = ''
				DATA.currentpass = True
				DATA.full_info = []
				DATA.csv = []
				self.record(self.id, DATA.ISN[i])

	def DeleteChromaTxt(self):
		if os.path.exists(DATA.chromalogpath):
			os.remove(DATA.chromalogpath)
			print('Delete txt')

	def handleChromaTxt(self, id, isn):
		with open(DATA.chromalogpath, 'r') as f:
			for line in f:
				if len(line.strip()):
					self.items_content.append(line.strip().split(';'))

		for items in self.items_content:
			if len(items) < 2:
				continue
			item = []
			for i in range(len(items)):
				item.append(items[i].strip())

			if item and 'Serial_No' in item:
				serial_no = item[1]

				if serial_no == isn:
					self.find = True
					self.firstfindISN = True
					DATA.logfilepath = 'log' + str(id)
					with open(DATA.logfilepath, 'w') as fw:
						fw.write('START TEST: ')
						fw.write(isn + '\n')

					DATA.csvfilepath = 'csv' + str(id)
					with open(DATA.csvfilepath, 'w') as fw:
						fw.write('')
					self.ll.basic(str(id))
				else:
					self.find = False
					self.firstfindISN = False

			if not self.find:
				continue

			if item and 'TEST_' in item[0]:
				if item[1] == 'PASS':
					item[1] = '0'
				if item[1] == 'FAIL':
					item[1] = '1'

				if item[1] == '1':
					if (float(item[2]) > float(item[4])) and (float(item[2]) < float(item[3])):
						item[1] = '0'

				if self.firstfindISN:
					DATA.op(item[0] +','+ item[1] +','+ item[2] +','+ item[3] +','+item[4])

				if int(item[1]):
					DATA.totalfails += 1

					if len(DATA.test_failures):
						DATA.test_failures += ';'
					DATA.test_failures += item[0]

			if not self.firstfindISN:
				win32api.MessageBox(0, 'Not find ISN %s in file' %isn, 'Waring', win32con.MB_OK)
				logE('Not find ISN %s in file' %isn)
				return

		# DATA.end(isn)



	def record(self, id, *argv):
		self.handleChromaTxt(id, argv[0])






if __name__ == '__main__':
	fd = FindDlg()
	# fd.searchwindow()
	# fd.sendISNtowindow()
	# fd.WaitChromaTxt()
	# fd.handleChromaTxt(1, '26EA01AC051802YX')
	# fd.handleChromaTxt(1, '26EA01AC051802YX')
