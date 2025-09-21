.386

include vmm.inc
include vwin32.inc
include shell.inc

DECLARE_VIRTUAL_DEVICE SYSMOD,1,0, SYSMOD_Control,\
UNDEFINED_DEVICE_ID, UNDEFINED_INIT_ORDER

Begin_control_dispatch SYSMOD
        Control_Dispatch Sys_Dynamic_Device_Init, Sysmodal
        Control_Dispatch w32_DeviceIoControl, OnDeviceIoControl
End_control_dispatch SYSMOD

VxD_PAGEABLE_DATA_SEG
        pmsg 	db 'They say assembly is dead.',0Dh, 0Ah
				db 'Yet here I am. Poking into the Ring0.',0Dh, 0Ah
				db 'Each old driver had a secret, and crashing the machine was just an ordinary art.',0Dh,0Ah,0Dh,0Ah 
				db 'The key was ASSEMBLY, it is, still..',0Dh,0Ah
				db 00h
				
		ptitle  db 0CCh, 0EBh, 0F8h, 0F5h, 0DAh, 0CDh, 0DFh, 0E2h, 0EEh ; our encrypted flag is in here
	            db 0AAh, 0F5h, 0FAh, 0A9h, 0F4h, 0AAh, 0C6h, 0ABh, 0C6h ; but the decryption is very simple
		        db 0EDh, 0F1h, 0AAh, 0C6h, 0EBh, 0A8h, 0F7h, 0FEh, 0A9h 
		        db 0E4h, 099h, 0
	ptitle_len dd 29

VxD_PAGEABLE_DATA_ENDS

VxD_PAGEABLE_CODE_SEG
BeginProc OnDeviceIoControl ; to be triggered by the loader :)
        assume esi:ptr DIOCParams
        .if [esi].dwIoControlCode==DIOC_Open
                xor eax, eax
        .endif
     ret
EndProc OnDeviceIoControl

BeginProc Sysmodal
	lea edi, ptitle
	mov bl, 99h ; just xor with 99h key
	jmp check_date

	result_byte db 0

check_date:
	mov al, 09h ; CMOS | RTC, YEAR CHECK
	out 70h, al
	in al, 71h
	
	cmp al, 32h ; same with the loader, is the year 2032?
	jne exitpr
	
	mov al, 07h ; CMOS | RTC, DAY CHECK
	out 70h, al
	in al, 71h

	cmp al, 04h ; is the day 4th?
	jne exitpr

decrypt_loop: ; simple xor routine
	mov al, [edi]
	xor al, bl
	mov [edi], al
	cmp al, 0
	je decrypt_done
	inc edi
	jmp decrypt_loop

decrypt_done:
        mov edi, offset ptitle
        mov ecx, offset pmsg
        mov eax, MB_OK
        VMMCall Get_Sys_VM_Handle ; get VM handle in EBX to...
        VxDCall SHELL_SYSMODAL_Message ; trigger custom BSoD

exitpr:
        clc
        ret
EndProc Sysmodal

VxD_PAGEABLE_CODE_ENDS

end
