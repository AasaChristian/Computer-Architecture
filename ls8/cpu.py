"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.running = True
        self.sp = 7
        self.fl = 6
        
        

    def load(self, filename):
        """Load a program into memory."""
        address = 0
        with open( filename ) as f:
            for line in f:
                line = line.split("#")
                try:
                    v = int(line[0], 2)
                    self.ram[address] = v
                    
                    address += 1
                except ValueError:
                    continue
        
    def ram_read(self, MAR):
        return self.ram[MAR] 

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.reg[self.sp] = 0xf4 # = 244
        self.reg[self.fl] = 200
        branch_table = {
            0b00000001: self.op_hlt,
            0b10000010: self.op_LDI,
            0b01000111: self.op_PRN,
            0b10100010: self.op_mul,
            0b01000101: self.op_PUSH,
            0b01000110: self.op_POP,
            0b10100111: self.op_CMP,
            0b01010101: self.op_JEQ,
            0b01010110: self.op_JNE,
            0b01010100: self.op_JMP
        }
        while self.running:
            # print(self.pc, "self.pc")

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            ir = self.ram[self.pc]

            if ir in branch_table:
                fun = branch_table[ir]

            fun( operand_a, operand_b)
    
    def op_hlt(self, operand_a, operand_b):
        # print("HLT")
        self.running = False

    def op_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        # print("load", self.reg, "reg")
        self.pc +=3

    def op_PRN(self, operand_a, operand_b):
        value = self.reg[operand_a]
        print(value)
        self.pc += 2


    def op_mul(self, operand_a, operand_b):
        self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
        self.pc += 3

    def op_PUSH(self, operand_a, operand_b):
        self.reg[self.sp] -= 1

        reg_num = self.ram[self.pc + 1]

        value = self.reg[reg_num]

        top_of_stack = self.reg[self.sp]
        self.ram[top_of_stack] = value
        # print(top_of_stack, "TOP of stock")
        # print(self.reg, "reg")
        self.pc += 2
        # print(self.ram, "ram")

    def op_POP(self, operand_a, operand_b):
        top_of_stack = self.reg[self.sp]
        # print(top_of_stack, "top of stack")
        value = self.ram[top_of_stack]
        # print(value, "value")
        reg_num = self.ram[self.pc + 1]
        self.reg[reg_num] = value
        # print(self.pc, "self.pc")
        # print("POP")
        self.reg[self.sp] += 1
        self.pc +=2

    def op_CMP(self, operand_a, operand_b):
        flag_num = self.reg[self.fl]
        # print(self.reg[operand_a], "self.reg[operand_a]")
        # print(self.reg[operand_b], "self.reg[operand_b]")
        if self.reg[operand_a] > self.reg[operand_b]:
            self.ram[flag_num] = 0b00000010
            # print("greater than") 
        elif self.reg[operand_a] < self.reg[operand_b]:
            self.ram[flag_num] = 0b00000100
            # print("less than")
        elif self.reg[operand_a] == self.reg[operand_b]:
            self.ram[flag_num] = 0b00000001 
            # print("equal")
        self.pc +=3

    def op_JEQ(self, operand_a, operand_b):
        # print("here JEQ is false")
        flag_num = self.reg[self.fl]
        if self.ram[flag_num] == 0b00000001:
            value = self.reg[operand_a]
            # print(value, "value added", self.pc, "self.pc")
            self.pc = value 
            # print(self.pc,"self.pc JEQ")
        else:
            self.pc += 2

    def op_JNE(self, operand_a, operand_b):
        # print("here JNE")
        flag_num = self.reg[self.fl]
        # print(self.ram[flag_num], "flagNumber")
        if self.ram[flag_num] != 0b00000001:
            value = self.reg[operand_a]
            # print(value, "value added", self.pc,  "self.pc")
            self.pc = value 
            # print(self.pc,"self.pc JNE")
        else:
            self.pc += 2

    def op_JMP(self, operand_a, operand_b):
        value = self.reg[operand_a]
        self.pc = value 
            
            













    # def op_CALL(self, operand_a, operand_b):
    #     return_addr = self.pc + 2

    #     self.reg[self.sp] -= 1
    #     self.ram[self.reg[self.sp]] = return_addr
        
        


