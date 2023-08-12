bits 64

extern GetStdHandle
extern WriteConsoleA
extern ExitProcess

section .data
    $hl_message db "Hello, World!", 10

section .bss
    $hl_written resq 1

section .text
    global hello_world

    hello_world:
        mov rcx, -11
        call GetStdHandle

        sub rsp, 32
        sub rsp, 8

        mov rcx, rax
        mov rdx, $hl_message
        mov r8, 13
        mov r9, $hl_written
        mov qword [rsp+32], 0
        call WriteConsoleA

        add rsp, 32+8

        xor ecx, ecx
        call ExitProcess