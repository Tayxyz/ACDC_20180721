# -*- coding:utf-8 -*-
import tkinter as tk
import time,threading

class dialog():
    def __init__(self,argv):
        pass


    def info(self,argv):
        try:
            msg=argv['msg']
        except:
            msg='Example'
        rt = tk.Tk()
        rt.wm_attributes('-topmost',1)  #top windows
        rt.withdraw()                   #hide windows
        # rt.attributes("-alpha", 1)
        l = tk.Label(rt, text=msg,font=('Times', '35', 'bold italic'),foreground='#ff00dd',background='#ffff09',wraplength=1000)
        b = tk.Button(rt,text='OK',font=('Times', '50', 'bold italic'),foreground='#fff0dd',background='#999999',command=rt.quit)
        l.pack(padx=20,pady=20) #show
        b.pack(padx=20,pady=20)

        #rt.overrideredirect(True)
        try:
            rt.iconbitmap('d:/Python27/DLLs/py.ico')
        except:
            pass
        rt.resizable(False, False)  # whether is able to change size of length and width
        rt.title("Warning")
        rt.update()  # update window ,must do
        curWidth = rt.winfo_reqwidth()  # get current width
        curHeight = rt.winfo_reqheight()  # get current height
        scnWidth, scnHeight = rt.maxsize()  # get screen width and height
        # now generate configuration information
        tmpcnf = '%dx%d+%d+%d' % (curWidth, curHeight,
                                  (scnWidth - curWidth) / 2, (scnHeight - curHeight) / 2)
        rt.geometry(tmpcnf)  #size of windows
        rt.deiconify() #to show again
        rt.mainloop()
        try:
            rt.destroy()
        except:
            pass
