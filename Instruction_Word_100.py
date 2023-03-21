BIT_LENGTH = 28
OP_LEN = 6
F_LEN = 6
class Translator:
    def __init__(self) -> None:
        self.funct = {
            'add': self.pad(F_LEN,'100000'),
            'and':self.pad(F_LEN,'100100'),
            'or': self.pad(F_LEN,'100101'),
            'sub': self.pad(F_LEN,'100010'),
            'sw': self.pad(F_LEN,'0'),
            'lw':self.pad(F_LEN,'0'),
            'slt':self.pad(F_LEN, '101010')
        }
        self.op = {
            'r':self.pad(OP_LEN,'000000'),
            'lw':self.pad(OP_LEN,'100011'),
            'sw':self.pad(OP_LEN,'101011'),
            'b':self.pad(OP_LEN,'000100'),
            'i':self.pad(OP_LEN,'001000'),
            'j':self.pad(OP_LEN, '000010')
        }
        self.register_op = ['add','sgt','slt','and','or','sub']
        self.immediate=['addi','andi','ori','subi']
        self.branch=['beq']
        self.memory=['sw','lw']
        self.jump=['j']
        self.instructions=self.register_op+self.immediate+self.memory+self.branch+self.jump
        self.reg = {'$'+i:self.int2bs(i,3) for i in [str(j) for j in range(8)]}
    
    def compile(self,instruction):
        # instructions are only space separated {add, }
        instructions = [j for j in [i.strip().lower() for i in instruction.split(' ')] if j not in ['']]
        if len(instructions)>0 and instructions[0] in self.instructions:
            pass
        else:
            return 'ERROR'

        if instructions[0] in self.register_op:
            if  instructions[0] == 'sgt':
                src2=self.reg[instructions[2]]
                src1=self.reg[instructions[3]]
                dest = self.reg[instructions[1]]
                to_return = self.op['r']+dest+src1+src2+self.pad(7,'0')+self.funct['slt']
                return to_return
            else:
                src1=self.reg[instructions[2]]
                src2=self.reg[instructions[3]]
                dest = self.reg[instructions[1]]
                to_return = self.op['r']+dest+src1+src2+self.pad(7,'0')+self.funct[instructions[0]]
                return to_return

        elif instructions[0] in self.immediate:
            dest = self.reg[instructions[1]]
            src1=self.reg[instructions[2]]
            imm = self.int2bs(instructions[3],16)
            return self.op['i']+dest+src1+imm
        
        elif instructions[0] in self.memory:
            dest = self.reg[instructions[1]]
            offset = self.int2bs(instructions[2][:-4],16)
            src=self.reg[instructions[2][-3:-1]]
            return self.op[instructions[0]]+dest+src+offset
        
        elif instructions[0] in self.branch:
            dest = self.reg[instructions[1]]
            src1=self.reg[instructions[2]]
            imm = self.int2bs(instructions[3],16)
            return self.op['b']+dest+src1+imm
        
        elif instructions[0] in self.jump:
            target_addres = self.int2bs(instructions[1],22)
            return self.op['j']+target_addres

        return 'ERROR'


    def pad(self,size, strin):
        """ Pads a string with leading zeros to produce a string with desirable length"""
        pad_amt = size-len(strin)
        return ("0"*(pad_amt) + strin)
    
    def pad_end(self,size, strin):
        """ Pads a string with ending zeros to produce a string with desirable length"""
        pad_amt = size-len(strin)
        return (strin+"0"*(pad_amt))

    def int2bs(self, s, n):
        """ Converts an integer string to a 2s complement binary string.

            Args: s = Integer string to convert.to 2s complement binary.
                n = Length of outputted binary string.
            
            Example Input: stpd("4", 4)
            Example Output: "0100"

            Example Input: stpd("-3", 16)
            Example Output: "1111111111111101" """
    
        x = int(s)                              # Convert string to integer, store in x.
        if x >= 0:                              # If not negative, use python's binary converter and strip the "0b"
            ret = str(bin(x))[2:]
            return self.pad(n,ret)     # Pad with 0s to length.
        else:
            ret = 2**n - abs(x)                 # If negative, convert to 2s complement integer
            return bin(ret)[2:]                 # Convert to binary using python's binary converter and strip the "0b"
        
    def bs2hex(self,v):
        """ Converts a binary string into hex.

            Args: v = Binary string to convert to hex

            Example Input: bs2hex("1010000010001111") 
            Example Output: "a08f" """
        return(hex(int(v,2))[2:])
    

if __name__ == "__main__":
    i = Translator()
    print (i.int2bs('2',5))
    print (i.int2bs('-1',8))
    print (i.bs2hex(i.int2bs('-1',8)))
    print (i.pad(2,i.bs2hex(i.int2bs('2',8))))

    print ("add $1 $0 $1")
    print (i.compile("add $1 $0 $1"))

    print ("addi $1 $0 -1")
    print (i.compile("addi $1 $0 -1"))

    print("sw $1 -1($0)")
    print (i.compile("sw $1 -1($0)"))
    
    print("lw $1 -1($0)")
    print (i.compile("lw $1 -1($0)"))

    print("beq $1 $2 3")
    print(i.compile("beq $1 $2 3"))

    print("j 7")
    print(i.compile("j 3"))

    print("slt $1 $2 $3")
    print(i.compile("slt $1 $2 $3"))

    print("slt $1 $2 $3")
    print(i.compile("slt $1 $2 $2"))
