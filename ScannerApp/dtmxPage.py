import tkinter as tk
from .utils import validateBarcode,PageMixin
# https://pypi.org/project/keyboard/

from .camera import Camera
 


class DTMXPage(tk.Frame,PageMixin):
    def __init__(self, parent, master):
        super().__init__(parent)
        self.master = master
        self.create_widgets()
         
        self.camera = Camera()
        self.initKeyboard()
        

    def create_widgets(self):
        tk.Label(self, text='LP:', font=(
            'Arial', 40)).place( x=340, y=20, )
        # grid(column=0,row=0,sticky='e',padx=(40,10),pady=(55,50))

        self.scanVar1 = tk.StringVar()
        # self.scanVar1.set('1234567890')

        self.scan1 = tk.Label(
            self, textvariable=self.scanVar1, font=('Arial', 40))
        self.scan1.place(x=440, y=20)  # grid(column=1,row=0,)

        tk.Label(self, text='SP:', font=('Arial', 40)
                 ).place(  x=340, y=110)
        # .grid(column=0,row=1,sticky='e',padx=(40,10),pady=(55,50))
        self.scanVar2 = tk.StringVar()
        # self.scanVar2.set('1234567890')
        self.scan2 = tk.Label(
            self, textvariable=self.scanVar2, font=('Arial', 40))
        self.scan2.place(x=440, y=110)  # .grid(column=1,row=1,)

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
    
    

    def keyboardCb(self,code):
        ""
        print(f"received code {code}")
    

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
