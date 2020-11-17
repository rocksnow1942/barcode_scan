import keyboard
import tkinter as tk
from threading import Thread
# https://pypi.org/project/keyboard/

def get_next_scan():
    "return 10 digits barcode or "
    # scan = []
    # laste = None
    # while True:
    #     e = keyboard.read_key()
    #     if e == laste:
    #         laste = None
    #         if e in '0123456789':
    #             scan.append(e)
    #         elif e=='enter':
    #             return ''.join(scan)
    #         else:
    #             scan = []
    #     else:
    #         laste = e
        
        
    events = keyboard.record(until='enter')
    barcode = list(keyboard.get_typed_strings(events))[0]
    return barcode
    # if len(barcode)==10 and barcode.isnumeric():
    #     return barcode
    # else:
    #     return None
    
    

class Scaner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Scanner App')        
        self.geometry('1920x1080+10+10')    
        self.create_widgets()    
        Thread(target=self.scanlistener,daemon=True).start()
        
        
    def create_widgets(self):
        tk.Label(text='First Scan: ',font=('Helvetica',80)).grid(column=0,row=0,sticky='e',padx=(40,10),pady=(55,50))
        
        self.scanVar1 = tk.StringVar()
        
        self.scan1 = tk.Label(textvariable=self.scanVar1,font=('Helvetica',70))
        self.scan1.grid(column=1,row=0,)
        
        tk.Label(text='Second Scan: ',font=('Helvetica',80)).grid(column=0,row=1,sticky='e',padx=(40,10),pady=(55,50))
        self.scanVar2 = tk.StringVar()
        self.scan2 = tk.Label(textvariable=self.scanVar2,font=('Helvetica',70))
        self.scan2.grid(column=1,row=1,)
        
        tk.Button(text='Confirm',font=('Helvetica',90),command=self.confirm).grid(column=0,row=2,sticky='n',pady=(55,50))
        tk.Button(text='Cancel',font=('Helvetica',90),command=self.cancel).grid(column=1,row=2,sticky='n',padx=(50,20),pady=(55,50))
         
        self.msgVar = tk.StringVar()
        self.msg = tk.Label(textvariable=self.msgVar,font=('Helvetica',60))
        self.msg.grid(column=0,row=3,columnspan=2)
         
    def displaymsg(self,msg,color='black'):
        self.msgVar.set(msg)
        if color:
            self.msg.config(fg=color)
    def scanlistener(self):
        while True:            
            res = get_next_scan()
            if len(res)==10 and res.isnumeric():
                self.displayScan(res)
            else:
                
                self.displaymsg(f"Unrecoginzed: {res}",'red')

    def displayScan(self,code):
        if code == self.scanVar1.get():
            self.displaymsg('Same code!','red')
            self.scan1.config(bg='red')
        elif not self.scanVar1.get():
            self.scanVar1.set(code)
            self.scan1.config(bg='green',fg='white')
        elif not self.scanVar2.get():
            self.scanVar2.set(code)
            self.scan2.config(bg='green',fg='white')
        else:
            self.displaymsg('Confirm/Cancel before new scan.','red')

    def confirm(self):
        code1 = self.scanVar1.get()
        code2 = self.scanVar2.get()
        if code1 and code2:
            self.displaymsg(f'Link {code1} to {code2}','green')
            self.scanVar1.set('')
            self.scanVar2.set('')
    
    def cancel(self):
        self.scanVar1.set('')
        self.scanVar2.set('')
        self.scan1.config(bg='white')
        self.scan2.config(bg='white')
        self.displaymsg('','white')

    def on_closing(self):
        print('exit...')
        self.destroy()

if __name__ == '__main__':
    app = Scaner()
    app.protocol('WM_DELETE_WINDOW',app.on_closing)
    app.mainloop()