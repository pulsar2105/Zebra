bits 64 ; for 64 bits only

; external functions
extern GetProcessHeap
extern HeapAlloc
extern HeapFree

extern GetStdHandle  ; for console
extern WriteConsoleA ; for console

extern ExitProcess   ; for exit

section .data
    a dq 1, 10
    b dq 1, 31
    c dq 1, 41

section .bss
    Handle resq 1  ; dynamic allocation
    written resq 1 ; display

section .text
    global main

    main:
    mov rbp, rsp; for correct debugging
        call pre_alloc

        push c
        push a ; + 32 a
        push b ; + 24 b
        push 1 ; + 16 i
        push 0 ; + 8  carry
        call addition


        ; display c
        mov rcx, -11
        call GetStdHandle

        sub rsp, 32
        sub rsp, 8

        mov rcx, rax
        mov rdx, c
        mov r8, 13
        mov r9, written
        mov qword [rsp+32], 0
        call WriteConsoleA

        add rsp, 32+8

        xor ecx, ecx
        call ExitProcess
        
        ; to prepare for allocation
    pre_alloc:
        call GetProcessHeap ; Set RAX to heap handle
        mov [Handle], rax
        ret

    ; rsp+8 = number of bytes to alloc
    alloc:
        mov rcx, [Handle]   ; [in] HANDLE hHeap
        mov rdx, 0x00000008 ; [in] DWORD dwFlags, réaction vs erreur (cf doc Microsoft)
        mov r8, [rsp+8]     ; [in] SIZE_T dwBytes, nombre d'octet alloués
        call HeapAlloc      ; alloc
        ; rax = pointer to allocated memory
        ret 8 ; pop in RIP and remove 8 bytes from the beginning of the stack

    ; rsp+8 = pointer to allocated memory
    free_aloc:
        mov rcx, [Handle]   ; [in] HANDLE hHeap
        mov rdx, 0x00000001 ; [in] DWORD dwFlags
        mov r8, [rsp+8]     ; [in] _Frees_ptr_opt_ LPVOID lpMem
        call HeapFree

        ret 8 ; pop in RIP and remove 8 bytes from the beginning of the stack

    ; function that uses the allocation function and copies data from another variable to the newly created one
    ; rsp+8 = size to allocate
    ; rsp+16 = pointer to old allocation
    allocate_and_copy:
        ; allocate memory
        push qword [rsp+8]
        call alloc
        ; rax = pointer allocated

        mov rcx, rax
        mov rdx, [rsp+16] ; rsp+16 = pointer to old allocation
        mov r8, 1 ; rdx = i=0
        call allocate_and_copy1

        ret 16

    allocate_and_copy1:
        mov rbx, [rdx + r8*8]
        mov [rcx + r8*8], rbx
        inc rdx ; rdx++

        ; while i != size(old_memory)
        cmp [rdx], r8
        jne allocate_and_copy1

        ; update the size of the new memory
        mov [rcx], r8

        mov rax, rcx
        ret

    ; rsp + 40, c ; result
    ; rsp + 32, a ; number 1 to add
    ; rsp + 24, b ; number 2 to add
    ; rsp + 16, 0 ; iterator to a big number
    ; rsp + 8,  0 ; carry
    ; rsp + 0,    ; next instruction
    ; important to manage addition with int/int, float/int, float/float, list/list
    addition:
        CLC ; clear carry
        jmp addition_arith
        ret 8*5

    addition_arith:
        ; on vérifie si on a pas dépasser la taille d'un des deux variables
        ; si size(a) > i et
        ; si size(b) > i
        mov rbx, [rsp+32]
        mov rbx, [rbx]
        cmp rbx, [rsp+16]
        seta al

        mov rbx, [rsp+24]
        mov rbx, [rbx]
        cmp rbx, [rsp+16]
        seta bl

        cmp al, bl
        je add_arith_end0 ; if the value have the same size

        ; si size(a) > i
        mov rbx, [rsp+32]
        mov rbx, [rbx]
        cmp rbx, [rsp+16]
        ja add_arith_end1

        ; si size(b) > i
        mov rbx, [rsp+24]
        mov rbx, [rbx]
        cmp rbx, [rsp+16]
        ja add_arith_end2

        ; rax est l'adresse de ou on stocke notre résultat

        ; do addition
        ; add previous carry
        ; [rsp+32] + [rsp+16]*8
        mov rbx, [rsp+16]
        imul rbx, 8
        add rax, [rsp+32]

        mov rcx, qword [rax]
        add rcx, [rsp+8]

        ; set carry to 0 and add the carry from adding the previous carry
        mov qword [rsp+8], 0
        adc qword [rsp+8], 0

        ; add a chunk of a with A value  chunk of B value
        ; [rsp+24] + [rsp+16]*8
        mov rbx, [rsp+16]
        imul rbx, 8
        add rax, [rsp+24]

        add rcx, qword [rax]
        adc qword [rsp+8], 0

        ; save result
        mov [rsp + 40], rcx

        ; i++
        inc qword [rsp + 16]

        jmp addition_arith


    ; si size(a) < i et size(b) < i
    ; it is fine
    add_arith_end0:
        ret

    ; si size(a) < i
    add_arith_end1:
        ret

    ; si size(b) < i
    add_arith_end2:
        ret