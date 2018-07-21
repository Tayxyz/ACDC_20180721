from tkinter import *
import win32con, win32gui, win32api
import tkinter.messagebox as tm
import time, os
import threading
from data import *
import localLog
import SFIS
from fixture import Fixture

mutex = threading.Lock()

class UI:
	def __init__(self):
		DATA.Readini()
		self.ll = localLog.LocalLog()
		self.sfis = SFIS.SFIS()
		self.fix = Fixture()


		self.windowname = DATA.WindowName
		self.id = 0
		self.ISNid_list = []

	def drawframe(self):
		self.root = Tk(className = '\ACDC')
		self.root.geometry('800x550')

		self.drawlabel()
		self.drawcheckbox()
		self.drawbutton()

		self.edt_label1.focus_set()
		self.con_label7.set(DATA.OPID)
		self.con_label1.set('26EA01AC221803B6')
		self.con_label2.set('26EA01AC221800UL')
		self.con_label3.set('26EA01AC221803G3')
		# self.con_label6.set('26EA01AC221803B6')
		# self.con_label4.set('26EA01AC2118003M')
		# self.con_label5.set('26EA01AC22180192')

		for i in range(6):
			self.setresultlabel(i+1, ' Result ', 0)

		self.root.mainloop()

	def ret_btn(self, *argv):
		self.Start()

	def ret_lab1(self, *argv):
		val = self.edt_label1.get()

		if len(val) != 16:
			self.edt_label1.delete(0, END)

		if not self.ck2_con.get():
			self.edt_label2.focus_set()
		elif not self.ck3_con.get():
			self.edt_label3.focus_set()
		elif not self.ck4_con.get():
			self.edt_label4.focus_set()
		elif not self.ck5_con.get():
			self.edt_label5.focus_set()
		elif not self.ck6_con.get():
			self.edt_label6.focus_set()
		else:
			self.btn.focus_set()

	def ret_lab2(self, *argv):
		val = self.edt_label2.get()

		if len(val) != 16:
			self.edt_label2.delete(0, END)

		if not self.ck3_con.get():
			self.edt_label3.focus_set()
		elif not self.ck4_con.get():
			self.edt_label4.focus_set()
		elif not self.ck5_con.get():
			self.edt_label5.focus_set()
		elif not self.ck6_con.get():
			self.edt_label6.focus_set()
		else:
			self.btn.focus_set()

	def ret_lab3(self, *argv):
		val = self.edt_label3.get()

		if len(val) != 16:
			self.edt_label3.delete(0, END)

		if not self.ck4_con.get():
			self.edt_label4.focus_set()
		elif not self.ck5_con.get():
			self.edt_label5.focus_set()
		elif not self.ck6_con.get():
			self.edt_label6.focus_set()
		else:
			self.btn.focus_set()

	def ret_lab4(self, *argv):
		val = self.edt_label4.get()

		if len(val) != 16:
			self.edt_label4.delete(0, END)

		if not self.ck5_con.get():
			self.edt_label5.focus_set()
		elif not self.ck6_con.get():
			self.edt_label6.focus_set()
		else:
			self.btn.focus_set()

	def ret_lab5(self, *argv):
		val = self.edt_label5.get()

		if len(val) != 16:
			self.edt_label5.delete(0, END)

		if not self.ck6_con.get():
			self.edt_label6.focus_set()
		else:
			self.btn.focus_set()

	def ret_lab6(self, *argv):
		val = self.edt_label6.get()

		if len(val) != 16:
			self.edt_label6.delete(0, END)

		self.btn.focus_set()

	def drawcheckbox(self):
		self.ck1_con = IntVar()
		self.ck1 = Checkbutton(self.root, variable = self.ck1_con, font = ('arial', 30), command = self.click_1)
		self.ck1.grid(row = 1, column = 0)

		self.ck2_con = IntVar()
		self.ck2 = Checkbutton(self.root, variable = self.ck2_con, font = ('arial', 30), command = self.click_2)
		self.ck2.grid(row = 2, column = 0)

		self.ck3_con = IntVar()
		self.ck3 = Checkbutton(self.root, variable = self.ck3_con, font = ('arial', 30), command = self.click_3)
		self.ck3.grid(row = 3, column = 0)

		self.ck4_con = IntVar()
		self.ck4 = Checkbutton(self.root, variable = self.ck4_con, font = ('arial', 30), command = self.click_4)
		self.ck4.grid(row = 4, column = 0)

		self.ck5_con = IntVar()
		self.ck5 = Checkbutton(self.root, variable = self.ck5_con, font = ('arial', 30), command = self.click_5)
		self.ck5.grid(row = 5, column = 0)

		self.ck6_con = IntVar()
		self.ck6 = Checkbutton(self.root, variable = self.ck6_con, font = ('arial', 30), command = self.click_6)
		self.ck6.grid(row = 6, column = 0)

		self.ck7_con = IntVar()
		self.ck7 = Checkbutton(self.root, variable = self.ck7_con, font = ('arial', 30))
		self.ck7.grid(row = 1, column = 3)

		self.ck8_con = IntVar()
		self.ck8 = Checkbutton(self.root, variable = self.ck8_con, font = ('arial', 30))
		self.ck8.grid(row = 2, column = 3)

		self.ck9_con = IntVar()
		self.ck9 = Checkbutton(self.root, variable = self.ck9_con, font = ('arial', 30))
		self.ck9.grid(row = 3, column = 3)

		self.ck10_con = IntVar()
		self.ck10 = Checkbutton(self.root, variable = self.ck10_con, font = ('arial', 30))
		self.ck10.grid(row = 4, column = 3)

		self.ck11_con = IntVar()
		self.ck11 = Checkbutton(self.root, variable = self.ck11_con, font = ('arial', 30))
		self.ck11.grid(row = 5, column = 3)

		self.ck12_con = IntVar()
		self.ck12 = Checkbutton(self.root, variable = self.ck12_con, font = ('arial', 30))
		self.ck12.grid(row = 6, column = 3)

	def drawlabel(self):
		Label(self.root, font = ('arial', 15)).grid(row = 0, column = 0)
		Label(self.root).grid(row = 7, column = 0)

		self.label1 = Label(self.root, text = 'DUT1:', font = ('arial', 20))
		self.label1.grid(row = 1, column = 1)
		self.label2 = Label(self.root, text = 'DUT2:', font = ('arial', 20))
		self.label2.grid(row = 2, column = 1)
		self.label3 = Label(self.root, text = 'DUT3:', font = ('arial', 20))
		self.label3.grid(row = 3, column = 1)
		self.label4 = Label(self.root, text = 'DUT4:', font = ('arial', 20))
		self.label4.grid(row = 4, column = 1)
		self.label5 = Label(self.root, text = 'DUT5:', font = ('arial', 20))
		self.label5.grid(row = 5, column = 1)
		self.label6 = Label(self.root, text = 'DUT6:', font = ('arial', 20))
		self.label6.grid(row = 6, column = 1)


		self.con_label1 = StringVar()
		self.edt_label1 = Entry(self.root, textvariable = self.con_label1, font = ('arial', 25), borderwidth = 4)
		self.edt_label1.grid(row = 1, column = 2)
		self.edt_label1.bind('<Return>', self.ret_lab1)


		self.con_label2 = StringVar()
		self.edt_label2 = Entry(self.root, textvariable = self.con_label2, font = ('arial', 25), borderwidth = 4)
		self.edt_label2.grid(row = 2, column = 2)
		self.edt_label2.bind('<Return>', self.ret_lab2)

		self.con_label3 = StringVar()
		self.edt_label3 = Entry(self.root, textvariable = self.con_label3, font = ('arial', 25), borderwidth = 4)
		self.edt_label3.grid(row = 3, column = 2)
		self.edt_label3.bind('<Return>', self.ret_lab3)

		self.con_label4 = StringVar()
		self.edt_label4 = Entry(self.root, textvariable = self.con_label4, font = ('arial', 25), borderwidth = 4)
		self.edt_label4.grid(row = 4, column = 2)
		self.edt_label4.bind('<Return>', self.ret_lab4)

		self.con_label5 = StringVar()
		self.edt_label5 = Entry(self.root, textvariable = self.con_label5, font = ('arial', 25), borderwidth = 4)
		self.edt_label5.grid(row = 5, column = 2)
		self.edt_label5.bind('<Return>', self.ret_lab5)

		self.con_label6 = StringVar()
		self.edt_label6 = Entry(self.root, textvariable = self.con_label6, font = ('arial', 25), borderwidth = 4)
		self.edt_label6.grid(row = 6, column = 2)
		self.edt_label6.bind('<Return>', self.ret_lab6)

		self.rst_label1 = Label(self.root, font = ('arial', 32))
		self.rst_label1.grid(row = 1, column = 4)
		self.rst_label2 = Label(self.root, font = ('arial', 32))
		self.rst_label2.grid(row = 2, column = 4)
		self.rst_label3 = Label(self.root, font = ('arial', 32))
		self.rst_label3.grid(row = 3, column = 4)
		self.rst_label4 = Label(self.root, font = ('arial', 32))
		self.rst_label4.grid(row = 4, column = 4)
		self.rst_label5 = Label(self.root, font = ('arial', 32))
		self.rst_label5.grid(row = 5, column = 4)
		self.rst_label6 = Label(self.root, font = ('arial', 32))
		self.rst_label6.grid(row = 6, column = 4)



		self.ID_label = Label(self.root, text = 'OPID: ', font = ('arial', 14))
		self.ID_label.grid(row = 8, column = 1)

		self.con_label7 = StringVar()
		self.edt_label7 = Entry(self.root, textvariable = self.con_label7, font = ('arial', 14), width = 12)
		self.edt_label7.grid(row = 8, column = 2)

		self.Tms_label1 = Label(self.root, text = 'Times: ', font = ('arial', 14))
		self.Tms_label1.grid(row = 9, column = 1)
		self.Tms_label2 = Label(self.root, font = ('arial', 14))
		self.Tms_label2.grid(row = 9, column = 2)

		self.context_label = Label(self.root, font = ('arial', 15)) # times
		self.context_label.grid(row = 9, column = 2)

	def drawbutton(self):
		self.btn = Button(self.root, text = ' Start ', font = ('arial', 20), command = self.Start)
		self.btn.grid(row = 10, column = 4)
		self.btn.bind('<Return>', self.Start)

	def barcodeready(self):
		DATA.ISN = {}
		if not self.ck1_con.get():
			DATA.ISN[0] = self.con_label1.get().upper()
		else:
			DATA.ISN[0] = ''

		if not self.ck2_con.get():
			DATA.ISN[1] = self.con_label2.get().upper()
		else:
			DATA.ISN[1] = ''

		if not self.ck3_con.get():
			DATA.ISN[2] = self.con_label3.get().upper()
		else:
			DATA.ISN[2] = ''

		if not self.ck4_con.get():
			DATA.ISN[3] = self.con_label4.get().upper()
		else:
			DATA.ISN[3] = ''

		if not self.ck5_con.get():
			DATA.ISN[4] = self.con_label5.get().upper()
		else:
			DATA.ISN[4] = ''

		if not self.ck6_con.get():
			DATA.ISN[5] = self.con_label6.get().upper()
		else:
			DATA.ISN[5] = ''

		for key, value in DATA.ISN.items():
			if value:
				# self.ISNid_list.append(key)

				DATA.logfilepath = 'log' + str(key+1)
				with open(DATA.logfilepath, 'w') as fw:
					fw.write('START TEST: ')
					fw.write(value + '\n')

				DATA.csvfilepath = 'csv' + str(key+1)
				with open(DATA.csvfilepath, 'w') as fw:
					fw.write('')

	def clearbarcode(self):
		if not self.ck7_con.get():
			self.con_label1.set('')
		if not self.ck8_con.get():
			self.con_label2.set('')
		if not self.ck9_con.get():
			self.con_label3.set('')
		if not self.ck10_con.get():
			self.con_label4.set('')
		if not self.ck11_con.get():
			self.con_label5.set('')
		if not self.ck12_con.get():
			self.con_label6.set('')

	def setresultlabel(self, id, result, *argv):
		if id == 1:
			if not self.ck1_con.get():
				self.rst_label1['text'] = result
				if argv[0] == 1:
					self.rst_label1['bg'] = 'Red'
				elif argv[0] == 2:
					self.rst_label1['bg'] = 'MediumSpringGreen'
				elif argv[0] == 3:
					self.rst_label1['bg'] = 'MistyRose'
				else:
					self.rst_label1['bg'] = 'AliceBlue'

		if id == 2:
			if not self.ck2_con.get():
				self.rst_label2['text'] = result
				if argv[0] == 1:
					self.rst_label2['bg'] = 'red'
				elif argv[0] == 2:
					self.rst_label2['bg'] = 'MediumSpringGreen'
				elif argv[0] == 3:
					self.rst_label2['bg'] = 'MistyRose'
				else:
					self.rst_label2['bg'] = 'AliceBlue'

		if id == 3:
			if not self.ck3_con.get():
				self.rst_label3['text'] = result
				if argv[0] == 1:
					self.rst_label3['bg'] = 'red'
				elif argv[0] == 2:
					self.rst_label3['bg'] = 'MediumSpringGreen'
				elif argv[0] == 3:
					self.rst_label3['bg'] = 'MistyRose'
				else:
					self.rst_label3['bg'] = 'AliceBlue'

		if id == 4:
			if not self.ck4_con.get():
				self.rst_label4['text'] = result
				if argv[0] == 1:
					self.rst_label4['bg'] = 'red'
				elif argv[0] == 2:
					self.rst_label4['bg'] = 'MediumSpringGreen'
				elif argv[0] == 3:
					self.rst_label4['bg'] = 'MistyRose'
				else:
					self.rst_label4['bg'] = 'AliceBlue'

		if id == 5:
			if not self.ck5_con.get():
				self.rst_label5['text'] = result
				if argv[0] == 1:
					self.rst_label5['bg'] = 'red'
				elif argv[0] == 2:
					self.rst_label5['bg'] = 'MediumSpringGreen'
				elif argv[0] == 3:
					self.rst_label5['bg'] = 'MistyRose'
				else:
					self.rst_label5['bg'] = 'AliceBlue'

		if id == 6:
			if not self.ck6_con.get():
				self.rst_label6['text'] = result
				if argv[0] == 1:
					self.rst_label6['bg'] = 'red'
				elif argv[0] == 2:
					self.rst_label6['bg'] = 'MediumSpringGreen'
				elif argv[0] == 3:
					self.rst_label6['bg'] = 'MistyRose'
				else:
					self.rst_label6['bg'] = 'AliceBlue'



		self.edt_label1.focus_set()

	def Start(self, *argv):
		try:
			self.fix.connect()
			self.fix.fixturein()
		except  Exception as e:
			logE(Exception, e)

		threading.Thread(target = self.temp).start()


	def click_1(self):
		# self.flag_1 = not self.flag_1
		if self.ck1_con.get():
			self.label1['state'] = DISABLED
			self.edt_label1['state'] = DISABLED
		else:
			self.label1['state'] = NORMAL
			self.edt_label1['state'] = NORMAL

	def click_2(self):
		if self.ck2_con.get():
			self.label2['state'] = DISABLED
			self.edt_label2['state'] = DISABLED
		else:
			self.label2['state'] = NORMAL
			self.edt_label2['state'] = NORMAL

	def click_3(self):
		if self.ck3_con.get():
			self.label3['state'] = DISABLED
			self.edt_label3['state'] = DISABLED
		else:
			self.label3['state'] = NORMAL
			self.edt_label3['state'] = NORMAL

	def click_4(self):
		if self.ck4_con.get():
			self.label4['state'] = DISABLED
			self.edt_label4['state'] = DISABLED
		else:
			self.label4['state'] = NORMAL
			self.edt_label4['state'] = NORMAL

	def click_5(self):
		if self.ck5_con.get():
			self.label5['state'] = DISABLED
			self.edt_label5['state'] = DISABLED
		else:
			self.label5['state'] = NORMAL
			self.edt_label5['state'] = NORMAL

	def click_6(self):
		if self.ck6_con.get():
			self.label6['state'] = DISABLED
			self.edt_label6['state'] = DISABLED
		else:
			self.label6['state'] = NORMAL
			self.edt_label6['state'] = NORMAL

# find Dlg
	def temp(self):
		try:
			for i in range(int(DATA.AutoTest)):
				self.barcodeready()

				for ii in DATA.ISN:
					if DATA.ISN[ii]:
						self.setresultlabel(ii+1, ' Testing ', 3)
					else:
						self.setresultlabel(ii+1, ' Result ', 0)

				self.btn['state'] = 'disabled'
				self.context_label['text'] = i+1
				self.DeleteChromaTxt()
				self.searchwindow()
				# print(i + 1)
				time.sleep(5)
			self.fix.fixtureout()
		except  Exception as e:
			logE(Exception, e)
			logE('temp() fail')

	def DeleteChromaTxt(self):
		if os.path.exists(DATA.chromalogpath):
			os.remove(DATA.chromalogpath)
			print('Delete txt')

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

	def sendISNtowindow(self):
		try:
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
			time.sleep(0.5)
			win32api.SendMessage(btdlg, win32con.WM_LBUTTONDOWN, 0, 0)
			time.sleep(0.5)
			win32api.SendMessage(btdlg, win32con.WM_LBUTTONUP, 0, 0)
		except Exception as e:
			logE(Exception, e)
			logE('sendISNtowindow fail')
			return

	def WaitChromaTxt(self):
		while not os.path.exists(DATA.chromalogpath): pass
		print('found txt')

		for i in DATA.ISN:
			if DATA.ISN[i]:
				self.firstfindISN = False
				self.final = True
				# self.flag = True
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
				self.handleChromaTxt(self.id, DATA.ISN[i])
		self.clearbarcode()
		self.btn['state'] = 'normal'

	# def record(self, id, argv):
	# 	self.handleChromaTxt(id, argv)

	def handleChromaTxt(self, id, isn):
		firstfind = 0
		ISNlist = []
		time.sleep(1)

		try:
			with open(DATA.chromalogpath, 'r') as f:
				for line in f:
					if len(line.strip()):
						self.items_content.append(line.strip().split(';'))

			for items in self.items_content:
				if len(items) < 2:
					continue
				item = []
				for iii in range(len(items)):
					item.append(items[iii].strip())

				# print(items)
				if item and 'Serial_No' in item:
					serial_no = item[1]
					firstfind += 1

					if not serial_no in ISNlist:
						ISNlist.append(serial_no)

					if serial_no == isn and not self.firstfindISN:

						self.find = True
						self.firstfindISN = True
						DATA.logfilepath = 'log' + str(id)
						with open(DATA.logfilepath, 'a') as fw:
							fw.write('')
							# fw.write('START TEST: ')
							# fw.write(isn + '\n')

						DATA.csvfilepath = 'csv' + str(id)
						with open(DATA.csvfilepath, 'a') as fw:
							fw.write('')
						self.ll.basic(str(id))
						self.sfis.SFIS_LOGIN_DB()
						self.sfis.SFIS_CHECK_ROUTE(isn)
						self.sfis.BUILD_PHASE(isn)
						self.sfis.TEST_READ_FACTORY_CONFIG_MLB(isn)
					# else:
					# 	self.find = False
					# 	self.firstfindISN = False

				if firstfind != id:
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

			for key, value in DATA.ISN.items():
				if isn in ISNlist:
					self.sfis.SFIS_UPLOAD_TEST_RESULT(isn)
					self.sfis.SFIS_LOGIN_OUT()
					DATA.end(isn)
					break
				else:
					if value == isn:
						self.setresultlabel(key+1, '   FAIL  ', 1)
						return

			for key, value in DATA.ISN.items():
				if isn == value:
					if DATA.errorcode:
						self.setresultlabel(key+1, DATA.errorcode, 1)
					else:
						self.setresultlabel(key+1, '  PASS  ', 2)
		except Exception as e:
			logE(Exception, e)
			logE('handleChromaTxt fail')

if __name__ == '__main__':
	ui = UI()
	ui.drawframe()

