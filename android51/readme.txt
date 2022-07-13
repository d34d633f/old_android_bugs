Android libhevc out of bounds read

How to reproduce:
1) checkout libhevc
2) compile standalone decoder test/decoder/main.c with ASAN 
3) run decoder using supplied test.cfg

Run decoder:

$ ./t1a
Using test.cfg as configuration file 
0
262144
=================================================================
==8373==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf615a800 at pc 0x812ea83 bp 0xffe8f088 sp 0xffe8f080
READ of size 1 at 0xf615a800 thread T0
    #0 0x812ea82 in ihevcd_nal_remv_emuln_bytes /dist/src/android/libhevc0517/decoder/ihevcd_nal.c:199
    #1 0x812b270 in ihevcd_decode /dist/src/android/libhevc0517/decoder/ihevcd_decode.c:585
    #2 0x80d6315 in main /dist/src/android/libhevc0517/t1.c:2218
    #3 0xf758daf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #4 0x80d0aa4 in _start (/dist/src/android/libhevc_fuzz/t1a+0x80d0aa4)

0xf615a800 is located 0 bytes to the right of 262144-byte region [0xf611a800,0xf615a800)
allocated by thread T0 here:
    #0 0x80b96d1 in __interceptor_malloc (/dist/src/android/libhevc_fuzz/t1a+0x80b96d1)
    #1 0x80d6020 in main /dist/src/android/libhevc0517/t1.c:2173
    #2 0xf758daf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-buffer-overflow /dist/src/android/libhevc0517/decoder/ihevcd_nal.c:199 ihevcd_nal_remv_emuln_bytes
Shadow bytes around the buggy address:
  0x3ec2b4b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ec2b4c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ec2b4d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ec2b4e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ec2b4f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x3ec2b500:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ec2b510: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ec2b520: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ec2b530: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ec2b540: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ec2b550: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:     fa
  Heap right redzone:    fb
  Freed heap region:     fd
  Stack left redzone:    f1
  Stack mid redzone:     f2
  Stack right redzone:   f3
  Stack partial redzone: f4
  Stack after return:    f5
  Stack use after scope: f8
  Global redzone:        f9
  Global init order:     f6
  Poisoned by user:      f7
  ASan internal:         fe
==8373==ABORTING

