#!/bin/bash

# Assemble bootloader
nasm -f bin boot/boot.asm -o boot.bin

# Compile kernel - added -fno-pic and -fno-stack-protector to avoid PIC errors
gcc -m32 -ffreestanding -fno-pie -c kernel/kernel.c -o kernel.o

# Link kernel
ld -m elf_i386 -T linker.ld -o kernel.bin kernel.o --oformat binary

# Create OS image
cat boot.bin kernel.bin > os.bin

echo "Build complete: build/os-image"

#run qemu
qemu-system-i386 -drive format=raw,file=os.bin
