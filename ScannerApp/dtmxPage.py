import keyboard
import tkinter as tk
from threading import Thread
from .utils import validateBarcode
# https://pypi.org/project/keyboard/

from .camera import Camera

def get_next_scan():
    events = keyboard.record(until='enter')
    barcode = list(keyboard.get_typed_strings(events))[0]
    return barcode


class DTMXPage(tk.Frame):
    def __init__(self, parent, master):
        super().__init__(parent)
        self.master = master
        self.create_widgets()
        self.stopScan = False
        self.camera = Camera()
        
    def create_widgets(self):
        tk.Label(self, text='LP:', font=(
            'Arial', 40)).place( x=340, y=20, )
        # grid(column=0,row=0,sticky='e',padx=(40,10),pady=(55,50))

        self.scanVar1 = tk.StringVar()
        # self.scanVar1.set('1234567890')

        self.scan1 = tk.Label(
            self, textvariable=self.scanVar1, font=('Arial', 40))
        self.scan1.place(x=420, y=20)  # grid(column=1,row=0,)

        tk.Label(self, text='SP:', font=('Arial', 40)
                 ).place(  x=340, y=110)
        # .grid(column=0,row=1,sticky='e',padx=(40,10),pady=(55,50))
        self.scanVar2 = tk.StringVar()
        # self.scanVar2.set('1234567890')
        self.scan2 = tk.Label(
            self, textvariable=self.scanVar2, font=('Arial', 40))
        self.scan2.place(x=420, y=110)  # .grid(column=1,row=1,)

        tk.Button(self, text='Read', font=('Arial', 40), command=self.read).place(
            x=340, y=210, height=150, width=210)  # grid(column=0,row=2,sticky='n',pady=(55,50))
        tk.Button(self, text='Save', font=('Arial', 40), command=self.confirm).place(
            x=570, y=210, height=150, width=210)  # grid(column=1,row=2,sticky='n',padx=(50,20),pady=(55,50))

        self.msgVar = tk.StringVar()
        self.msg = tk.Label(self, textvariable=self.msgVar, font=('Arial', 20))
        self.msgVar.set('message for dtmx page')
        
        self.msg.place(x=20, y=430, width=660)

        tk.Button(self, text='Back', font=('Arial', 25),
                  command=self.goToHome).place(x=680, y=390, height=50,width=90)
    
    def showPage(self):
        self.stopScan = False
        Thread(target=self.scanlistener, daemon=True).start()
        self.tkraise()
        self.camera.start()
        

    def goToHome(self):
        self.stopScan = True
        self.camera.stop()
        self.master.showPage('HomePage')

    def displaymsg(self, msg, color='black'):
        self.msgVar.set(msg)
        if color:
            self.msg.config(fg=color)

    def scanlistener(self):
        while True:            
            res = get_next_scan()
            if self.stopScan:
                break
            if validateBarcode(res,'plate'):
                self.displayScan(res)
            else:
                self.displaymsg(f"Unrecoginzed: {res}", 'red')

    def displayScan(self, code):
        if code == self.scanVar1.get():
            self.displaymsg('Same code!', 'red')
            self.scan1.config(bg='red')
        elif not self.scanVar1.get():
            self.scanVar1.set(code)
            self.scan1.config(bg='green', fg='white')
        elif not self.scanVar2.get():
            self.scanVar2.set(code)
            self.scan2.config(bg='green', fg='white')
        else:
            self.displaymsg('Confirm/Cancel before new scan.', 'red')

    def confirm(self):
        code1 = self.scanVar1.get()
        code2 = self.scanVar2.get()
        if code1 and code2:
            self.displaymsg(f'Link {code1} to {code2}', 'green')
            self.scanVar1.set('')
            self.scanVar2.set('')

    def read(self):
        "read camera"
        result = self.camera.scan()
        highlights = []
        for idx, res in enumerate(result):
            if not validateBarcode(res,'specimen'):
                highlights.append(idx)
        self.camera.drawOverlay(highlights)
