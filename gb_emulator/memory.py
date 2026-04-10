


class Memory:
    def __init__(self,rom):
        self.rom = rom 
        self.ram = [0]* 65536

    def read_byte(self,addr):
        if addr < 0x8000:
            return self.rom.read_byte(addr)
        return self.ram[addr]
    
    def write_byte(self,addr,value):
        self.ram[addr] = value
        