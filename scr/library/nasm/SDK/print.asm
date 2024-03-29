bits 64 ; for 64 bits only

extern GetStdHandle  ; for console
extern WriteConsoleA ; for log console
extern WriteConsoleW ; for utf-8 console

extern ExitProcess   ; for exit

section .data

section .bss
    $print_written resq 1 ; display

section .text
    ;global main
    ;main:
    ;    ; we print message print(data, last_chr)
    ;    push $message
    ;    push $last_chr
    ;    call print

    ;    push $message
    ;    push $last_chr
    ;    call print_log

    ;    push 1 ; if exit program must print additional informations (0:no, 1:yes)
    ;    call exit

    ;    xor ecx, ecx
    ;    call ExitProcess

    ; rsp+16 = data to display
    ; rsp+8 = last character to display$print_end
    print:
        ; data
        mov rcx, -11            ; normal settings
        call GetStdHandle

        mov rcx, rax            ; handle
        mov rdx, [rsp+16]       ; message, +8 to skip the length field
        add rdx, 8
        mov r8, [rsp+16]         ; message length (and the final character)
        mov r8, [r8]
        imul r8, 2
        inc r8                  ;
        mov r9, $print_written  ; written characters
        push 0                  ; lpReserved
        call WriteConsoleW      ; utf-8
        ; stack cleaning
        pop rcx

        ; if data is NULL character, 0
        cmp qword [rsp+8], 0
        je $print_end

        ; last character
        push qword [rsp+8]
        push 0
        call print

        ret 16

    $print_end:
        ret 16

    ; print data ANSI
    ; rsp+16 = data to display
    ; rsp+8 = last character to display
    print_log:
        ; data
        mov rcx, -11            ; normal settings
        call GetStdHandle

        mov rcx, rax            ; handle
        mov rdx, [rsp+16]       ; message, +8 to skip the length field
        add rdx, 8
        mov r8, [rsp+16]        ; message length (and the final character)
        mov r8, [r8]
        imul r8, 2
        inc r8                  ;
        mov r9, $print_written  ; written characters
        push 0                  ; lpReserved
        call WriteConsoleA
        ; stack cleaning
        pop rcx

        ; if data is NULL character, 0
        cmp qword [rsp+8], 0
        je $print_log_end

        ; last character
        push qword [rsp+8]
        push 0
        call print_log

        ret 16

    $print_log_end:
        ret 16