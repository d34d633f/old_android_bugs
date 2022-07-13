Android libavc  out of bounds read 

Tested on android-7.1.2_r12 branch.

How to reproduce:
1) checkout libavc
2) compile standalone decoder test/decoder/main.c with ASAN
3) run decoder: ./dec -i 1.bin

ASAN LOG:

$ ./t1a -i 1.bin
100
Ittiam Decoder Version number: @(#)Id:H264VDEC_production Ver:05.00 Released by ITTIAM Build: Jun 27 2017 @ 11:19:16
2743
Error in video Frame decode : ret 1 Error 95
695
442
499
=================================================================
==27470==ERROR: AddressSanitizer: global-buffer-overflow on address 0x081d3bab at pc 0x8148f51 bp 0xffd30558 sp 0xffd30550
READ of size 1 at 0x081d3bab thread T0
    #0 0x8148f50 in ih264d_deblock_mb_mbaff /dist/src/android/libavc0617/decoder/ih264d_deblocking.c:1710
    #1 0x814767d in ih264d_deblock_picture_mbaff /dist/src/android/libavc0617/decoder/ih264d_deblocking.c:802
    #2 0x8113b90 in ih264d_deblock_display /dist/src/android/libavc0617/decoder/ih264d_parse_slice.c:917
    #3 0x80e5696 in ih264d_video_decode /dist/src/android/libavc0617/decoder/ih264d_api.c:2321
    #4 0x80da6b0 in main /dist/src/android/libavc0617/decoder/t1.c:2875
    #5 0xf74afaf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #6 0x80d2bd4 in _start (/sec/zdi/0617/avc11/t1a+0x80d2bd4)

0x081d3bab is located 21 bytes to the left of global variable 'gau1_ih264d_beta_table' from 'ih264d_tables.c' (0x81d3bc0) of size 76
0x081d3bab is located 31 bytes to the right of global variable 'gau1_ih264d_alpha_table' from 'ih264d_tables.c' (0x81d3b40) of size 76
SUMMARY: AddressSanitizer: global-buffer-overflow /dist/src/android/libavc0617/decoder/ih264d_deblocking.c:1710 ih264d_deblock_mb_mbaff
Shadow bytes around the buggy address:
  0x2103a720: 00 00 00 00 00 04 f9 f9 f9 f9 f9 f9 00 04 f9 f9
  0x2103a730: f9 f9 f9 f9 00 00 00 00 00 00 00 00 00 00 00 00
  0x2103a740: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x2103a750: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x2103a760: 00 04 f9 f9 f9 f9 f9 f9 00 00 00 00 00 00 00 00
=>0x2103a770: 00 04 f9 f9 f9[f9]f9 f9 00 00 00 00 00 00 00 00
  0x2103a780: 00 04 f9 f9 f9 f9 f9 f9 00 00 00 00 00 00 00 00
  0x2103a790: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x2103a7a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x2103a7b0: 00 00 00 00 f9 f9 f9 f9 f9 f9 f9 f9 00 00 00 00
  0x2103a7c0: 00 00 00 00 00 04 f9 f9 f9 f9 f9 f9 00 00 00 00
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
==27470==ABORTING

