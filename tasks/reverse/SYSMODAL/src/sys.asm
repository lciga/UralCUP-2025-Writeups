; rixus semi-ring0 vxd loader based on bb code

.586p                          
.model  flat, stdcall
locals
jumps

extrn ExitProcess:PROC
extrn MessageBoxA:PROC
extrn CreateFileA:PROC
extrn CloseHandle:PROC
extrn GetModuleHandleA:PROC
extrn GetProcAddress:PROC
extrn DeviceIoControl:PROC

Interrupt equ 05h 

.data

szTitle db "Hi",0                 
szMessage db "Have you ever thought of a flag?",0  
handle1 dd ?

.code

start:

	mov ax, ds
	cmp ax, 137h
	jb back2host ; NT checkup but sometimes not really successful
	
	push edx
	sidt [esp-2]
	pop edx
	add edx,(Interrupt*8)+4
	mov ebx,[edx]
	mov bx,word ptr [edx-4]
	
	lea edi,InterruptHandler ; we go there after int 5 :)

	mov [edx-4],di
	ror edi,16
	mov [edx+2],di

	push ds
	push es

	int Interrupt     
	pop es
	pop ds
	
	mov [edx-4],bx
	ror ebx,16
	mov [edx+2],bx

	mov esi, offset result_byte
	mov al, [esi]
	cmp al, 7
	je call_driver
	jmp back2host

call_driver:
	call CreateFileA, offset file1, 0, 0, 0, 0, 4000000h, 0 ; we try to trigger the custom BSoD from the VxD
	mov handle1, eax
	jmp exitpr

back2host:
	call MessageBoxA, 0, offset szMessage, offset szTitle, 0
	call ExitProcess, 0

exitpr:
	call MessageBoxA, 0, offset umsg, offset utitle, 0
	call CloseHandle, handle1
	call ExitProcess, 0



InterruptHandler:
	pushad
	jmp check_date
file1 db '\\.\sysmod.vxd',0 ; sometimes strings contained there won't show up in debuggers or disasms
	umsg db "Isn't it nice",0
	utitle db 'haha',0
	result_byte db 0 ; for the date check
	xor_key dd 0
	key_b0 db 0
	key_b1 db 0
	key_b2 db 0
	key_b3 db 0
	key_pos db 0

check_date: ; the same thing is in the driver! 

	mov al, 09h ; CMOS | RTC, DATE OF MONTH
	out 70h, al
	in al, 71h

	cmp al, 32h ; is the year 2032?
	jne nwrite

	mov al, 07h ; CMOS | RTC, DATE OF MONTH
	out 70h, al
	in al, 71h

	cmp al, 04h ; is the day 4th?
	jne nwrite
	mov result_byte, 7 ; some xor key set handled after the successfful checkup
	mov byte ptr [key_b0],04Eh
	mov byte ptr [key_b1],021h
	mov byte ptr [key_b2],06h
	mov byte ptr [key_b3],04Dh

	jmp exithandler

nwrite:
	nop

exithandler: ; at this point we leave the Ring0
	popad
	iretd

df_decrypt_loop: ; fake func but needed to decrypt the VxD
	mov bl, [key_pos]
	cmp bl, 0
	je df_use_result_byte

	movzx edx, bl
	dec edx

	mov al, byte ptr [key_b0+edx]
	xor byte ptr [esi], al
	jmp df_advance_pos

df_use_result_byte:
	xor byte ptr [esi], 07h

df_advance_pos:
	inc esi
	inc byte ptr [key_pos]
	cmp al, 5
	jb df_skip_reset
	mov byte ptr [key_pos],0
	df_skip_reset:
	dec ecx
	jne df_decrypt_loop

end start
