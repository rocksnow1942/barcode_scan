import tkinter as tk
from threading import Thread
import serial.tools.list_ports
import time


class Controller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Motor Controller')        
        self.geometry('+10+10')    
        self.create_widgets()    
        self.motorPort = None
        Thread(target=self.scanMotor,daemon=True).start()

        
        
    def create_widgets(self):

        self.stepVar = tk.IntVar()
        self.stepVar.set(200)
        tk.Label(text='Steps (Interger)').grid(column=0,row=0,padx=15,pady=10,sticky='e')
        tk.Entry(textvariable=self.stepVar, width=20).grid(column=1,row=0,padx=(0,15))


        self.speedVar = tk.IntVar()
        self.speedVar.set(400)
        tk.Label(text='Speed (steps/second)',).grid(column=0,row=1,padx=15,pady=10,sticky='e')
        tk.Entry(textvariable=self.speedVar, width=20).grid(column=1,row=1,padx=(0,15))

        self.runBtn = tk.Button(text='Run',font=('Helvetica',32),command=self.runBtnCb)
        self.runBtn.grid(column=0,row=2,padx=15,pady=10,sticky='we')

        self.stopBtn = tk.Button(text='Stop',font=('Helvetica',32),command=self.stopBtnCb)
        self.stopBtn.grid(column=1,row=2,padx=15,pady=10,sticky='we')
        self.stopBtn['state']='disabled'

        self.msgVar = tk.StringVar()
        self.msgVar.set('Searching motor...')
        self.msg = tk.Label(textvariable=self.msgVar,font=('Helvetica',12))
        self.msg.grid(column=0,row=3,columnspan=2,pady=(0,10))
    
    def clearBtnStatus(self):
        "reset btn status when motor done moving."
        while True:
            res = self.motorPort.read_all().decode()
            if res:
                self.runBtn['state']='normal'
                self.stopBtn['state']='disabled'
                break 
            time.sleep(0.2)

    def runBtnCb(self):
        step = self.stepVar.get()
        speed = self.speedVar.get()
        if self.motorPort:
            self.motorPort.write(f"{step} {speed}".encode())
            self.runBtn['state']='disabled'
            self.stopBtn['state']='normal'
            Thread(target = self.clearBtnStatus,daemon=True).start()

    def stopBtnCb(self):
        if self.motorPort:
            self.motorPort.write("s".encode())
            
         
    def displaymsg(self,msg,color='black'):
        self.msgVar.set(msg)
        if color:
            self.msg.config(fg=color)

    def scanMotor(self):
        "scan Pico connected and update pico list"        
        def findPort(p):
            #/dev/cu.usbserial-0001
            try:

                ser = serial.Serial(p,115200)
                time.sleep(0.3)
                print(ser.read_all())
                time.sleep(0.3)
                ser.write('test'.encode())
                time.sleep(3)
                
                res = ser.readline().decode()
                print(res)
                if res[0:4]=='send' and self.motorPort==None:
                    self.motorPort = ser
                    self.displaymsg(f"Connected to Motor @ {p}.",'green')
            except: pass
        
        def scan():
            ports = [i.device for i in serial.tools.list_ports.comports()]
            
            for i in ports:
                print(i)
                Thread(target=findPort,args=(i,),daemon=True).start()

        Thread(target=scan,daemon=True).start() 
   
    def on_closing(self):
        print('exit...')
        if self.motorPort:
            self.motorPort.close()
        self.destroy()

if __name__ == '__main__':
    app = Controller()
    app.protocol('WM_DELETE_WINDOW',app.on_closing)
    app.mainloop()