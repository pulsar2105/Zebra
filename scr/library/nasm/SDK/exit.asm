bits 64 ; for 64 bits only

extern GetStdHandle  ; for console
extern WriteConsoleA ; for log console
extern ExitProcess

section .data
    exit_msg dq 10, "bye bye !", 10, 0

section .bss
    written_exit resq 1 ; display

section .text
    ;;global main
    ;;main:
    ;;    push 0 ; if exit program must print additional informations (0:no, 1:yes)
    ;;    call exit

    ; [rsp+8] additional informations yes/no
    exit:
        cmp qword [rsp+8], 1
        je exit_with_msg

        pop rcx

        xor ecx, ecx
        call ExitProcess

    exit_with_msg:
        mov rcx, -11        ; normal settings
        call GetStdHandle

        mov rcx, rax        ; handle
        mov rdx, exit_msg   ; message, +8 to skip the length field
        add rdx, 8
        mov r8, exit_msg    ; message length (and the final character)
        mov r8, [r8]
        imul r8, 2
        inc r8              ;
        mov r9, written_exit     ; written characters
        push 0              ; lpReserved
        call WriteConsoleA
        ; stack cleaning
        pop rcx

        xor ecx, ecx
        call ExitProcess

