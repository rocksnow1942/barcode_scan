def validateBarcode(code,sampleType):
    "to validate a barcode if its right format"
    
    return len(code) == 10 and code.isnumeric()


def indexToGridName(index,grid=(12,8),direction='top'):
    "convert 0-95 index to A1-H12,"
    rowIndex = "ABCDEFGHIJKLMNOPQRST"[0:grid[1]]
    rowIndex = rowIndex if direction == 'top' else rowIndex[::-1]
    row = index//grid[0] + 1
    col = index - (row-1) * grid[0] + 1
    rowM = rowIndex[row-1]
    return f"{rowM}{col}"


class PageMixin():
    def showPage(self):
        self.keySequence = []
        # Thread(target=self.scanlistener, daemon=True).start()
        self.tkraise()
        self.focus_set()
        # self.camera.start()
        
    def goToHome(self):
        
        # self.camera.stop()
        self.master.showPage('HomePage')
        self.keySequence = []

    def displaymsg(self, msg, color='black'):
        self.msgVar.set(msg)
        if color:
            self.msg.config(fg=color)
    
    def initKeyboard(self):
        self.bind("<Key>",self.scanlistener)
        self.keySequence = []

    def scanlistener(self,e):
        # while True:            
            # res = get_next_scan()
        # if self.stopScan:
        #     self.keySequence = []
        #     return
        char = e.char
        if char.isalnum():
            self.keySequence.append(char)
        else:
            if self.keySequence:
                self.keyboardCb(''.join(self.keySequence))
            self.keySequence=[]
        # if validateBarcode(res,'plate'):
        #     self.displayScan(res)
        # else:
        #     self.displaymsg(f"Unrecoginzed: {res}", 'red')
