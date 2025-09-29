.586
.model flat, stdcall
extern MessageBoxA@16:near ; masm unfortunately...

includelib user32.lib

data segment
		header db "Final Stage",0
		msg db "Welcome to the Final Stage!",0
		bytes db 16h, 33h, 31h, 18h, 36h, 26h, 23h, 36h, 11h, 72h, 2Fh, 29h, 2Bh, 11h, 00h, 55h, 3Dh, 15h, 70h, 33h, 23h, 2Bh, 44h, 1Ch, 3Ah, 20h, 1Ch, 1Ch, 27h, 60h, 06h, 18h, 47h, 18h

		; let's leave several invalid XOR keys here :)
		; hopefully everyone realizes the only obvious option to solve it is XOR?
		; since we don't have much of code here... hoho

		blabla1 db 043h,061h,050h,074h,075h,072h,065h,04Dh,065h, 0
		blabla2 db 043h,061h,050h,074h,055h,072h,065h,04Dh,065h, 0
		blabla3 db 043h,061h,050h,074h,075h,072h,045h,04Dh,065h, 0
		blabla4 db 0A3h,01Bh,05Ch,07Dh,03Eh,02Ah,0FFh,010h,067h, 0
		blabla5 db 011h,022h,033h,044h,055h,066h,077h,088h,099h, 0
		blabla6 db 043h,041h,050h,074h,075h,072h,065h,04Dh,065h, 0
		blabla7 db 04Ch,041h,055h,054h,05Dh,02Bh,03Ch,07Fh,06Ah, 0
		blabla8 db 0A1h,0B2h,0C3h,0D4h,0E5h,0F6h,017h,028h,039h, 0
		blabla9 db 043h,061h,070h,074h,075h,072h,065h,04Dh,065h, 0
		blabla10 db 0FFh,0ECh,0A7h,022h,05Dh,013h,02Bh,04Dh,06Fh,07Ch, 0
		blabla11 db 055h,08Bh,0ECh,83h,0ECh,10h,6Ah,0Ch,68h,10h,00h, 0
		blabla12 db 090h,90h,90h,0CCh,0CCh,8Bh,45h,0Ch,89h,45h,04h, 0
		blabla13 db 0B8h,04h,00h,00h,00h,0CDh,021h,90h,90h,0
		blabla14 db 63h,61h,70h,74h,75h,72h,65h,6Dh,65h, 0
		blabla15 db 43h,41h,50h,54h,55h,52h,45h,4Dh,45h, 0
		blabla16 db 43h,41h,50h,74h,75h,72h,65h,6Dh,65h, 0
		
data ends

code segment
start:
	push 0
	push offset header
	push offset msg
	push 0
	call MessageBoxA@16
	
	ret
code ends
end start