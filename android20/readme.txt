Android libavc heap corrupion bug

How to reproduce:
1) checkout libavc
2) compile standalone decoder from libavc/test/decoder/main.c
3) run: ./dec -i 1.bin

gdb backtrace:

*** Error in `/android/libavc/decoder/fuzz/t1': double free or corruption (out): 0xf7778080 ***

Program received signal SIGABRT, Aborted.
0xf7fdbc90 in __kernel_vsyscall ()
(gdb) x/10wx 0xf7778080
0xf7778080:	0x01010101	0x01010101	0x01010101	0x01010101
0xf7778090:	0x01010101	0x01010101	0x01010101	0x01010101
0xf77780a0:	0x01010101	0x01010101


