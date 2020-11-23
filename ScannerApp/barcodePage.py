import tkinter as tk
from .utils import validateBarcode,PageMixin
# https://pypi.org/project/keyboard/
 

class BarcodePage(tk.Frame,PageMixin):
    def __init__(self, parent, master):
        super().__init__(parent)
        self.master = master
        self.create_widgets()
        self.initKeyboard()

    def create_widgets(self):
        tk.Label(self, text='From Plate:', font=(
            'Arial', 40)).place(anchor='ne', x=390, y=20)
        # grid(column=0,row=0,sticky='e',padx=(40,10),pady=(55,50))

        self.scanVar1 = tk.StringVar()
        # self.scanVar1.set('1234567890')

        self.scan1 = tk.Label(
            self, textvariable=self.scanVar1, font=('Arial', 40))
        self.scan1.place(x=410, y=20)  # grid(column=1,row=0,)

        tk.Label(self, text='To Plate:', font=('Arial', 40)
                 ).place(anchor='ne', x=390, y=110)
        # .grid(column=0,row=1,sticky='e',padx=(40,10),pady=(55,50))
        self.scanVar2 = tk.StringVar()
        # self.scanVar2.set('1234567890')
        self.scan2 = tk.Label(
            self, textvariable=self.scanVar2, font=('Arial', 40))
        self.scan2.place(x=410, y=110)  # .grid(column=1,row=1,)

        tk.Button(self, text='Confirm', font=('Arial', 60), command=self.confirm).place(
            x=20, y=210, height=150, width=360)  # grid(column=0,row=2,sticky='n',pady=(55,50))
        tk.Button(self, text='Cancel', font=('Arial', 60), command=self.cancel).place(
            x=420, y=210, height=150, width=360)  # grid(column=1,row=2,sticky='n',padx=(50,20),pady=(55,50))

        self.msgVar = tk.StringVar()
        self.msg = tk.Label(self, textvariable=self.msgVar, font=('Arial', 30))
        # self.msgVar.set('Confirm/Cancel before new scan')
        # grid(column=0,row=3,columnspan=2)
        self.msg.place(x=20, y=380, width=660)

        tk.Button(self, text='Back', font=('Arial', 25),
                  command=self.goToHome).place(x=680, y=390, height=50,width=90)

    def showPage(self):
        self.keySequence = []
         
        self.tkraise()
        self.focus_set()
      
        
    def goToHome(self):
         
        self.master.showPage('HomePage')
        self.keySequence = []

    def keyboardCb(self,code):
        if validateBarcode(code, 'plate'):
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
        else:
            self.displaymsg(f"Unrecoginzed: {code}", 'red')
 
    def confirm(self):
        code1 = self.scanVar1.get()
        code2 = self.scanVar2.get()
        if code1 and code2:
            self.displaymsg(f'{code1} <-> {code2}', 'green')
            self.scanVar1.set('')
            self.scanVar2.set('')

    def cancel(self):
        self.scanVar1.set('')
        self.scanVar2.set('')
        self.scan1.config(bg='white')
        self.scan2.config(bg='white')
        self.displaymsg('', 'white')
