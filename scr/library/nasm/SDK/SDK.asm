bits 64 ; for 64 bits only

; program who get all the components from our library and groups them here

%include "exit.asm"
%include "print.asm"
%include "hello_world.asm"
;%include "allocation.asm"

section .data
    ; message in utf16, must be in utf16 or utf32, utf8 don't work
    $message dq 9, __utf16__("01A🎈🟢🟠🔴⚫🔵5"), 0 ; we must add a single character at the end of the string ¯\_(ツ)_/¯
    $last_chr dq 1, 10, 0

section .bss

section .text
    global main
    main:
        mov rbp, rsp; for correct debugging

        ; we print message print(message, last_chr)
        push $message
        push $last_chr
        call print

        push $message
        push $last_chr
        call print_log

        call hello_world

        push 1 ; if exit program must print additional informations (0:no, 1:yes)
        call exit