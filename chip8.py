#!/usr/bin/env python3

import random

# Python Chip-8 emulator


class Chip8:
    def __init__():
        # Define fontset, each character is 4*5 pixels
        self.fontset = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80,  # F
        ]

    def initialize(self, pixels):
        self.pc = 0x200  # Program counter starts at 0x200
        opcode = 0
        I = 0  # Index register
        sp = 0  # Stack pointer

        # Clear display, stack, register, memory and keys
        self.graphics = [0] * pixels
        self.stack = []
        self.V = [0] * 16  # Registers
        self.I = 0  # Address/Index Register
        self.memory = [0] * 4096
        self.keys = [0] * 16  # CHIP-8 has 16key hex keyboard input

        # Reset timers
        self.delay_timer = 0
        self.sound_timer = 0

        # Flag to indicate drawing to screen
        self.draw_flag = True

        # Load fontset, stored up to location 0x50==80
        for i in range(80):
            self.memory[i] = self.fontset[i]

        # reset timers

    def loadProgram(self, file_name):
        with open(file_name, "rb") as file
        fileBuffer = file.read()
        for i in range(len(fileBuffer)):
            self.memory[self.pc + i] = fileBuffer[i]

    def emulateCycle():
        # Fetch Opcode - stored in 2 successive 1 byte memory locations
        # Must be merged to create the single 2 byte Opcode
        self.opcode = self.memory[pc] << 8 | self.memory[pc + 1]

        # Decode Opcode:READ FIRST 4 BITS (opcode & 0xF000)

        # Get X and Y values from opcode for setting V register
        # Bit shifts push just value at F position to first bit
        vx = (self.opcode & 0x0F00) >> 8
        vy = (self.opcode & 0x00F0) >> 4

        if (self.opcode & 0xF000 == 0x0000):
            if (self.opcode & 0x000F == 0x0000):  # 0x00EO: Clears the screen
                for i in range(len(self.graphics)):
                    self.graphics[i] = 0
                self.draw_flag = True

            elif(self.opcode & 0x000F == 0x000E):  # 0x00EE: Returns from subroutine
                self.pc = self.stack.pop()

                elif(self.opcode & 0x0F00 != 0x0000):  # 0x0NNN
                    self.pc = (self.opcode & 0x0FFF) - 2

            else:
                print("Opcode unknown [0x0000]: %s" % opcode)
                self.pc -= 2

        elif (self.opcode & 0xF000 == 0x1000):  # 0x1NNN: Jumps to address at NNN
            self.pc = (self.opcode & 0x0FFF) - 2

        elif (self.opcode & 0xF000 == 0x2000):  # 0x2NNN: Calls subroutine at address NNN
            self.stack.append(self.pc)
            self.pc = (self.opcode & 0x0FFF) - 2

        elif (self.opcode & 0xF000 == 0x3000):  # 0x3XNN: Skip next inst if VX==NN
            if self.V[vx] == self.opcode & 0x00FF:
                self.pc += 2

        elif (self.opcode & 0xF000 == 0x4000):  # 0x4XNN: Skip next inst if VX!==NN
            if self.V[vx] != self.opcode & 0x00FF:
                self.pc += 2

        elif (self.opcode & 0xF000 == 0x5000):  # 0x5XY0: Skip next inst if VX==VY
            if self.V[vx] == self.V[vy]:
                self.pc += 2

        elif (self.opcode & 0xF000 == 0x6000):  # 0x6XNN: Set VX to NN
            self.V[vx] = self.opcode & 0x00FF

        elif (self.opcode & 0xF000 == 0x7000):  # 0x5XY0: Add NN to VX
            self.V[vx] = self.opcode & 0x00FF

        elif (self.opcode & 0xF000 == 0x8000):  # 0x8---
            first_bit = self.opcode & 0x000F

            if (first_bit == 0x0000):  # 0x8XY0: Set VX to the value of VY
                self.V[vx] = self.V[vy]

            elif (first_bit == 0x0001):  # 0x8XY1: Set VX to VX OR VY
                self.V[vx] = self.V[vx] | self.V[vy]

            elif (first_bit == 0x0002):  # 0x8XY2: Set VX to VX AND VY
                self.V[vx] = self.V[vx] & self.V[vy]

            elif (first_bit == 0x0003):  # 0x8XY3: Set VX to VX XOR VY
                self.V[vx] = self.V[vx] ^ self.V[vy]

            elif (first_bit == 0x0004):  # 0x8XY4: Add VY to VX
                # VF set to 1 if carry, 0 if no carry
                self.V[vx] += self.V[vy]
                if V[vx] > 0xFF:  # greater than 255 = carry
                    self.V[0xF] = 1  # set carry
                else:
                    self.V[0xF] = 0
                self.V[vx] &= 0xFF

            elif (first_bit == 0x0005):  # 0x8XY5: VY subtract from VX
                # VF set to 0 if borrow, 1 if no borrow
                self.V[vx] -= self.V[vy]
                if V[vx] < self.V[vy]:
                    self.V[0xF] = 0  # set borrow
                else:
                    self.V[0xF] = 1
                self.V[vx] &= 0xFF

            elif (first_bit == 0x0006):  # 0x8XY6: Shifts VX RIGHT by 1
                # VF set to value of LEAST significant bit of VX BEFORE Shifts
                self.V[0xF] = self.V[vx] & 0x01
                self.V[vx] = self.V[vx] >> 1

            elif (first_bit == 0x0007):  # 0x8XY7: Sets VX TO VY-VX
                # VF set to 0 if borrow, 1 if no borrow
                result = self.V[vy] - self.V[vx]
                self.V[vx] = result
                if self.V[vx] < result:
                    self.V[0xF] = 0  # set borrow
                else:
                    self.V[0xF] = 1
                self.V[vx] &= 0xFF

            elif (first_bit == 0x000E):  # 0x8XYE: Shifts VX LEFT by 1
                # VF set to value of MOST significant bit of VX BEFORE Shifts
                self.V[0xF] = self.V[vx] & 0x80
                self.V[vx] = self.V[vx] << 1

        elif (self.opcode & 0xF000 == 0x9000):  # 0x9XY0: Skips next instruction if VX != VY
            if (self.V[vx] != self.V[vy]):
                self.pc += 2

        elif (self.opcode & 0xF000 == 0xA000):  # 0xANNN: Sets I address to NNN
            self.I = self.opcode & 0x0FFF

        elif (self.opcode & 0xF000 == 0xB000):  # 0xBNNN: Jumps to the address NNN + V0
            address = (self.opcode & 0x0FFF) + self.V[0]
            self.pc = address - 2

        elif (self.opcode & 0xF000 == 0xC000):  # 0xCXNN:
            # Sets VX to result of bitwise AND on random number(0,255) and NN
            nn = self.opcode & 0x00FF
            rand = random.uniform(0, 255)
            self.V[vx] = nn & rand

        elif (self.opcode & 0xF000 == 0xD000):  # 0xDXYN:
            # Draws sprite at coord(VX,VY) width=8 height=N
            # VF set to 1 if any screen pixels are flipped from set->unset
            # VF set to 0 if not
            x_loc = vx
            y_loc = vy
            height = self.opcode & 0x000F
            self.V[0xF] = 0
            pixel = 0
            for y in range(0, height):
                pixel = self.memory[self.I + y]
                for x in range(0, 8):  # sprites are 8px wide
                    if pixel & (0x80 >> x) != 0 and not(y + y_loc >= 32 or x + x_loc >= 64):
                        if self.graphics[i] == 1:
                            self.V[0xf] = 1
                        self.graphics[i] ^= 1
            self.draw_flag = True

        elif(self.opcode & 0xF000 == 0xE000):  # 0xE---
            first_two_bits = self.opcode & 0x00FF

            if(first_two_bits == 0x009E):  # 0xEX9E: Skip next inst if key in VX pressed
                key = self.V[vx]
                if self.keys[key] == 1:
                    self.pc += 2

            elif(first_two_bits == 0x00A1):  # 0xEXA1 Skip next inst if key in VX not pressed
                key = self.V[vx]
                if self.keys[key] == 0:
                    self.pc += 2

        elif(self.opcode & 0xF000 == 0xF000):  # 0xF---
            first_two_bits = self.opcode & 0x00FF

            if(first_two_bits == 0x0007):  # 0xFX07: Sets VX to val of delay timer
                self.V[vx] = self.delay_timer

            if(first_two_bits == 0x000A):  # 0xFX0A: Key press awaited then stored in VX
                key = -1
                for i in range(len(self.keys)):
                    if self.keys[i] == 1:
                        key = i
                        break
                if key >= 0:
                    self.V[vx] = key
                else:
                    self.pc -= 2
            if(first_two_bits == 0x0015):  # 0xFX15: Sets delay timer to VX
                self.delay_timer = self.V[vx]
            if(first_two_bits == 0x0018):  # 0xFX18: Sets sound timer to VX
                self.sound_timer = self.V[vx]
            if(first_two_bits == 0x001E):  # 0xFX1E: Adds VX to I
                self.I += self.V[vx]
            if(first_two_bits == 0x0029):  # 0xFX29
                #: Sets I to loc of sprite for character in VX (0-F character hex, 4x5 font)
                self.I = self.V[vx] * 5  # Sprites are 5 bytes long
            if(first_two_bits == 0x0033):  # 0xFX33:Stores binary coded decimal representation of VX
                # Most significant digits at addr in I (hundreds)
                # Middle digit at addr in I+1 (tens)
                # Least significant digit at addr I+2 (ones)

                self.memory[I] = vx / 100
                self.memory[I + 1] = (vx / 10) % 10
                self.memory[I + 2] = (vx % 100) % 10

            if(first_two_bits == 0x0055):  # 0xFX55
                # Stores V0 to VX (incl VX) in memory starting at addr I

                for i in range(0, vx + 1):
                    self.memory[self.I + i] = self.V[i]

            if(first_two_bits == 0x0065):  # 0xFX65
                # Fill V0 to VX(incl VX)w/values from memory starting at addr I

                for i in range(0, vx + 1):
                    self.V[i] = self.memory[self.I + i]

        else:
            print("Opcode - {0} - not found".format(hex(self.opcode)))
            self.pc -= 2

            # Next instruction starts 2 locations after first (1 byte each loc)
        self.pc += 2

        # Update Timers

    def setKeys():
        pass
