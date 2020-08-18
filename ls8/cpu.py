"""CPU functionality."""

import sys


# Day 2 Goals:

# 1. -> refactor the load() func to accept a ls8 file as an arg (instead of hardcoded program)

# 2. -> create multiple instruction (`run mutl.ls8`)


class CPU:
    """Main CPU class."""

    def __init__(self):
        # pc
        self.pc = 0
        # ram
        self.ram = [0] * 256
        # register
        self.reg = [0] * 8

    def ram_read(self, mar):
        read = self.ram[mar]
        return read

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    # todo: "program" will be removed from inside func
    # "program" will be an arg passed into load()
    def load(self, program):
        """Load a program into memory."""

        address = 0

        with open(program) as f:
            for line in f:
                # remove '#' from lines
                line_split = line.split("#")[0]
                action = line_split.strip()

                if action == "":
                    continue

                # set instruction based on aciton
                instruction = int(action, 2)
                self.ram_write(address, instruction)

                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # addition
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        # multiplication
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def run(self):
        """Run the CPU."""

        # add instruction handlers

        #         program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8 plus 3 -> PRN
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0 plus 2 -> PRN
        #     0b00000000,
        #     0b00000001,  # HLT plus 1 -> LDI
        # ]

        # pointer
        LDI = 0b10000010
        # print
        PRN = 0b01000111
        # halt
        HLT = 0b00000001
        # multiply
        MUL = 0b10100010

        # computer "on" var to perform while loop
        isRunning = True

        while isRunning:
            # set instruction from our pc counter
            instruction = self.ram_read(self.pc)

            # standard naming convention is opr_a (operation)
            opr_a = self.ram_read(self.pc + 1)
            opr_b = self.ram_read(self.pc + 2)

            if instruction == HLT:
                self.pc += 1
                isRunning = False

            elif instruction == LDI:
                self.pc += 3
                self.reg[opr_a] = opr_b

            elif instruction == PRN:
                self.pc += 2
                print(self.reg[opr_a])

            # case: multiply
            elif instruction == MUL:
                self.pc += 3
                self.alu("MUL", opr_a, opr_b)

            else:
                isRunning = False
                print("Error operation not found")

