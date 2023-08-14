bits 64 ; for 64 bits only

; external functions
extern GetProcessHeap
extern HeapAlloc
extern HeapFree

extern GetStdHandle  ; for console
extern WriteConsoleA ; for console

extern ExitProcess   ; for exit

section .data
    $Handle dq 0 ; dynamic allocation

section .bss

section .text
    ;global main
    ;main:
    ;    xor rax, rax

    ; prepare for allocation
    alloc:
        ; test if The Handle is dfine or not
        cmp [$Handle], 0
        jne $post_alloc

        call GetProcessHeap ; Set RAX to heap handle
        mov [$Handle], rax
        jmp $post_alloc

    ; rsp+8 = number of bytes to alloc
    $post_alloc:
        mov rcx, [$Handle]   ; [in] HANDLE hHeap
        mov rdx, 0x00000008 ; [in] DWORD dwFlags, reaction vs error (cf doc Microsoft)
        mov r8, [rsp+8]     ; [in] SIZE_T dwBytes, number of bytes to allocate
        call HeapAlloc      ; alloc
        ; rax = pointer to allocated memory
        ret 8 ; pop in RIP and remove 8 bytes from the beginning of the stack

    ; rsp+8 = pointer to allocated memory
    free_alloc:
        mov rcx, [$Handle]   ; [in] HANDLE hHeap
        mov rdx, 0x00000001 ; [in] DWORD dwFlags
        mov r8, [rsp+8]     ; [in] _Frees_ptr_opt_ LPVOID lpMem
        call HeapFree

        ret 8 ; pop in RIP and remove 8 bytes from the beginning of the stack