

class CPU :
    def __init__(self,memory):

        self.memory = memory 

        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        self.H = 0
        self.L = 0

        self.sp = 0
        self.pc = 0

    def fetch(self):
        opcode =self.memory.read_byte(self.pc)
        self.pc+=1
        return opcode 
    
    def execute(self,opcode):
        if opcode == 0x00: #NOP
            pass
        elif opcode == 0x3E: #LD A, d8
            value = self.memory.read_byte(self.pc)
            self.pc+=1
            self.A = value 
        else:
            print("unknown opcode:", hex(opcode))
    
    def step(self):
       opcode = self.fetch()
       print("Opcode:", hex(opcode)," PC:", hex(self.pc))
