bits 64 ; for 64 bits only

extern GetStdHandle  ; for console
extern WriteConsoleA ; for console
extern WriteConsolew ; for console

extern ExitProcess   ; for exit

section .data
    message dq 5, 'hello', 0 ; we must add a single character at the end of the string ¯\_(ツ)_/¯
    last_chr dq 1, 10, 0

section .bss
    written resq 1 ; display

section .text
    global main

    main:
    mov rbp, rsp; for correct debugging

        ; we print message print(data, last_chr)
        push message 
        push last_chr  
        call print
        
        push message 
        push last_chr  
        call print

        xor ecx, ecx
        call ExitProcess


    ; rsp+16 = data to display
    ; rsp+8 = last character to display
    print:       
        ; data
        mov rcx, -11            ; normal settings
        call GetStdHandle

        mov rcx, rax            ; handle
        mov rdx, [rsp+16]       ; message, +8 to skip the length field
        add rdx, 8
        mov r8, [rsp+16]        ; message length (and the final character)
        mov r8, [r8]
        inc r8                  ; 
        mov r9, written         ; written characters
        push 0                  ; lpReserved
        call WriteConsoleA
        ; stack cleaning
        pop rcx
        
        ; if data is NULL character, 0
        cmp qword [rsp+8], 0
        je print_end
        
        ; last character
        push qword [rsp+8]
        push 0
        call print

        ret 16

    print_end:
        ret 16
