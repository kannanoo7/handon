


class ROM:
    def __init__(self,path):
        with open(path,'rb') as f:
            self.data = f.read()
    
    def read_byte(self,addr):
        return self.data[addr]
    