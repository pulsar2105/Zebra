bits 64 ; for 64 bits only

: program who get all the components from our library and groups them here

%include "exit.asm"
%include "print.asm"
%include "hello_world.asm"
%include "allocation.asm"

section .data

section .bss

section .text