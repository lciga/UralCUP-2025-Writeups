; MASM
; ML NYANFLAG.ASM UNDER DOS

.8086
.model tiny

.code
	org 100h
	
start:
	mov ax, 0003h
	int 10h
	
	call clear
	call drframe
	call ascii
	xor ah, ah
	int 16h

	jmp exitprog
	
decrypt proc near ; we just see it there, never jump to this proc though!
    call getip

getip:
    pop bp
    lea si, [bp + bytes_stream - getip + 1]
    lea di, flagbuf
    mov cx, flaglen

    lea bx, xorkeys
    mov bp, bx
    mov dx, bx
    add dx, 7
    mov ah, 1

unroll:
    mov al, [si]
    xor al, byte ptr [bx]
    stosb

    cmp ah, 1
    jne backward

    cmp bx, dx
    je backdec
    inc bx
    jmp cont

backward:
    cmp bx, bp
    je forwrdinc
    dec bx
    jmp cont

backdec:
    mov ah, 0
    dec bx
    jmp cont

forwrdinc:
    mov ah, 1
    inc bx

cont:
    add si, 2
    loop unroll

    mov byte ptr [di], '$'
    mov dx, offset flagbuf
    mov ah, 09h ; output for the flag!
    int 21h

    mov ax, 4c00h ; if we call the procedure, we don't need the rest to execute anymore!
    int 21h
decrypt endp


bytes_stream label byte ; let's just play ping pong rn
	mov al, ('U' xor xorkey0)
	mov al, ('r' xor xorkey1)
	mov al, ('a' xor xorkey2)
	mov al, ('l' xor xorkey3)
	mov al, ('C' xor xorkey4)
	mov al, ('T' xor xorkey5)
	mov al, ('F' xor xorkey6)
	mov al, ('{' xor xorkey7)
	mov al, ('d' xor xorkey6)
	mov al, ('0' xor xorkey5)
	mov al, ('s' xor xorkey4)
	mov al, ('_' xor xorkey3)
	mov al, ('d' xor xorkey2)
	mov al, ('3' xor xorkey1)
	mov al, ('b' xor xorkey0)
	mov al, ('u' xor xorkey1)
	mov al, ('g' xor xorkey2)
	mov al, ('g' xor xorkey3)
	mov al, ('3' xor xorkey4)
	mov al, ('r' xor xorkey5)
	mov al, ('_' xor xorkey6)
	mov al, ('v' xor xorkey7)
	mov al, ('s' xor xorkey6)
	mov al, ('_' xor xorkey5)
	mov al, ('k' xor xorkey4)
	mov al, ('1' xor xorkey3)
	mov al, ('t' xor xorkey2)
	mov al, ('t' xor xorkey1)
	mov al, ('3' xor xorkey0)
	mov al, ('n' xor xorkey1)
	mov al, ('}' xor xorkey2)
bytes_streamend label byte

clear proc near
	mov ax, 0600h
	mov bh, 07h
	mov cx, 0000h
	mov dx, 184fh
	int 10h
	
	ret
clear endp

drframe proc near
	mov ah, 02h
	mov bh, 0
	mov dh, 0
	mov dl, 0
	int 10h
	
	mov ah, 0ah
	mov al, '+'
	mov cx, 1
	int 10h
	
	mov al, '-'
	mov cx, 78
	int 10h
	
	mov al, '+'
	mov cx, 1
	int 10h
	
	ret
drframe endp

ascii proc near
    mov si, offset lines
    mov cx, 24

next_line:
    lodsw
    mov dx, ax
    call printline
    loop next_line

    ret
ascii endp

printline proc near
	mov ah, 09h
	int 21h
	
	ret
printline endp

line1  db "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@","$" ; 80x24, full window and one line is for the DOS cursor at the very end
line2  db "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@","$"
line3  db "@@+                                                                          *@@","$"
line4  db "@@+                                                                          *@@","$"
line5  db "@@+                   :*=                           -*-                      *@@","$"
line6  db "@@+                  %@@@@=                       :@@@@@:                    *@@","$"
line7  db "@@+                %@@* -@@@:                   .@@@= +@@#.                  *@@","$"
line8  db "@@+              *@@%     =@@+                 %@@+     *@@.                 *@@","$"
line9  db "@@+               -                            .:                            *@@","$"
line10 db "@@+              .@@@@     #@@= :@@@-    -@@%:     @@@@*                     *@@","$"
line11 db "@@+  ------:.    .@@@@@:   #@@=  :@@@:  -@@%.     *@@%@@-        .::-----.   *@@","$"
line12 db "@@+   .-=*****#+ .@@@+@@=  #@@=   :%@@:-@@#      :@@#:@@%.    =#*****=-:     *@@","$"
line13 db "@@+  .:::::::::. .@@@ +@@+ #@@=    .#@@@@#       @@@: +@@+    .::::::::::    *@@","$"
line14 db "@@+  -=========- .@@@  =@@+#@@=      %@@#       *@@@**#@@@-   -==========.   *@@","$"
line15 db "@@+         :=*+..@@@   =@@@@@=      *@@=      :@@@@@@@@@@@   +*+-.          *@@","$"
line16 db "@@+ =@@@@#+--::. .@@@    :@@@@=      *@@=      %@@=     *@@*  .::--=*@@@@*   *@@","$"
line17 db "@@+               ===     .===.      :==.     .===      .===                 *@@","$"
line18 db "@@+                                                                          *@@","$"
line19 db "@@+                     our baby kitten ate your flag                        *@@","$"
line20 db "@@+                                                                          *@@","$"
line21 db "@@+                                                                          *@@","$"
line22 db "@@+                                                                          *@@","$"
line23 db "@@@#########################################################################@@@@","$"
line24 db "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@","$"

lines dw offset line1, offset line2, offset line3, offset line4, offset line5, offset line6, offset line7, offset line8
      dw offset line9, offset line10, offset line11, offset line12, offset line13, offset line14, offset line15, offset line16
      dw offset line17, offset line18, offset line19, offset line20, offset line21, offset line22, offset line23, offset line24

xorkey0 equ 26h
xorkey1 equ 56h
xorkey2 equ 13h
xorkey3 equ 7ah
xorkey4 equ 3bh
xorkey5 equ 91h
xorkey6 equ 33h
xorkey7 equ 7dh

xorkeys db xorkey0, xorkey1, xorkey2, xorkey3
        db xorkey4, xorkey5, xorkey6, xorkey7

flaglen equ (bytes_streamend - bytes_stream) / 2
flagbuf db 64 dup(?)

exitprog:
	mov ax, 4c00h
	int 21h

end start
