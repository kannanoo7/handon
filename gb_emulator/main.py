

from rom import ROM
from memory import Memory
from cpu import CPU

rom = ROM("roms/tetris.gb")
memory= Memory(rom)
cpu = CPU(memory)


while True:
    cpu.step()

# print("ROM Size:", len(rom.data), "bytes")
# print("First byte:", hex(memory.read_byte(0x100)))