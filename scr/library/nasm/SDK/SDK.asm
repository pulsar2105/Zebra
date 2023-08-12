bits 64 ; for 64 bits only

; program who get all the components from our library and groups them here

%include "exit.asm"
%include "print.asm"
%include "hello_world.asm"
;%include "allocation.asm"

section .data

section .bss

section .text
    global main
    main:
        ; we print message print(data, last_chr)
        push $message
        push $last_chr
        call print

        push $message
        push $last_chr
        call print_log

        push 1 ; if exit program must print additional informations (0:no, 1:yes)
        call exit