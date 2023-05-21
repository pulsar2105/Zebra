bits 64 ; for 64 bits only

extern GetStdHandle  ; for console
extern WriteConsoleA ; for console
extern WriteConsolew ; for console

extern ExitProcess   ; for exit

section .data
    message dq 8, 'bonjour', 10, 0 ; we must add a single character at the end of the string

section .bss
    written resq 1 ; display

section .text
    global main

    main:
    mov rbp, rsp; for correct debugging

        mov rcx, -11    ; normal settings
        call GetStdHandle

        mov rcx, rax            ; handle
        mov rdx, message + 8    ; message, +8 to skip the length field
        mov r8, [message]              ; message length (and the final character)
        inc r8
        mov r9, written         ; written characters
        push 0                  ; lpReserved
        call WriteConsoleA

        ; stack cleaning
        pop rcx
        
        ; we print message                
        push message
        call print        

        xor ecx, ecx
        call ExitProcess


    ; rsp+8 = data to display
    print:
        mov rcx, -11    ; normal settings
        call GetStdHandle

        mov rcx, rax            ; handle
        mov rdx, [rsp+8]    ; message, +8 to skip the length field
        add rdx, 8
        mov r8, [rsp+8] ; message length (and the final character)
        mov r8, [r8]
        inc r8
        mov r9, written         ; written characters
        push 0                  ; lpReserved
        call WriteConsoleA

        ; stack cleaning
        pop rcx

        ret 8

