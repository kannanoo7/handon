[org 0x7c00]
[bits 16]

CODE_SEG equ 0x08
DATA_SEG equ 0x10

mov ah, 0x0e
mov al, 'A'
int 0x10

start:
    cli

    ; -------------------------
    ; SETUP SEGMENTS
    ; -------------------------
    xor ax, ax
    mov ds, ax
    mov es, ax

    ; -------------------------
    ; LOAD KERNEL FROM DISK
    ; -------------------------
    mov ah, 0x02        ; BIOS read sector
    mov al, 10          ; load 10 sectors (5120 bytes)
    mov ch, 0           ; cylinder
    mov cl, 2           ; start from sector 2
    mov dh, 0           ; head
    mov dl, 0x80        ; first hard disk

    mov bx, 0x1000      ; load address (0x1000)
    int 0x13

    mov ah, 0x0e
    mov al, 'B'
    int 0x10

    ; -------------------------
    ; LOAD GDT
    ; -------------------------
    lgdt [gdt_descriptor]

    ; -------------------------
    ; ENABLE PROTECTED MODE
    ; -------------------------
    mov eax, cr0
    or eax, 1
    mov cr0, eax

    ; -------------------------
    ; FAR JUMP TO 32-BIT MODE
    ; -------------------------
    jmp CODE_SEG:protected_mode

; -------------------------
; GDT (GLOBAL DESCRIPTOR TABLE)
; -------------------------
gdt_start:
    dq 0x0000000000000000      ; null descriptor
    dq 0x00cf9a000000ffff      ; code segment (base=0, limit=4GB, type=code/execute/read)
    dq 0x00cf92000000ffff      ; data segment (base=0, limit=4GB, type=data/read/write)
gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

; -------------------------
; PROTECTED MODE (32-bit)
; -------------------------
[bits 32]

protected_mode:
    ; setup segment registers
    mov ax, DATA_SEG
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax


    ; write 'P' to video memory
    mov byte [0xb8000], 'P'
    mov byte [0xb8001], 0x0F

    ; -------------------------
    ; JUMP TO KERNEL
    ; -------------------------
    call 0x1000

hang:
    jmp hang

; -------------------------
; BOOT SIGNATURE
; -------------------------
times 510-($-$$) db 0
dw 0xaa55