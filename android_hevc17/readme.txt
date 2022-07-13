Android libhevc out of bounds read

Tested on android-8.1.0_r1

How to reproduce:
1) download libhevc src (repo sync external/libhevc)
2) compile standalone decoder with ASAN
$ cd libhevc
$ cp test/decoder/main.c t1.c
$ cp test/decoder/test.cfg .

$ ./t1a
Using test.cfg as configuration file 
0
101
Ittiam Decoder Version number: @(#)Id:HEVCDEC_production Ver:05.00 Released by ITTIAM Build: Dec  6 2017 @ 15:25:58
16701
=================================================================
==3338==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf56fe7fc at pc 0x81302af bp 0xffb72278 sp 0xffb72270
READ of size 4 at 0xf56fe7fc thread T0
    #0 0x81302ae in ihevcd_bits_seek /libhevc1217/decoder/ihevcd_bitstream.c:254
    #1 0x8156a46 in ihevcd_cabac_decode_terminate /libhevc1217/decoder/ihevcd_cabac.c:407
    #2 0x814cb0c in ihevcd_parse_slice_data /libhevc1217/decoder/ihevcd_parse_slice.c:2797
    #3 0x812f68e in ihevcd_nal_unit /libhevc1217/decoder/ihevcd_nal.c:406
    #4 0x812b99e in ihevcd_decode /libhevc1217/decoder/ihevcd_decode.c:645
    #5 0x80d86f3 in main /libhevc1217/t1.c:2753
    #6 0xf758baf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #7 0x80d0c74 in _start (/cloudfuzz/1217/1/t1a+0x80d0c74)

0xf56fe7fc is located 4 bytes to the left of 1048592-byte region [0xf56fe800,0xf57fe810)
allocated by thread T0 here:
    #0 0x80b9bc1 in __interceptor_memalign (/cloudfuzz/1217/1/t1a+0x80b9bc1)
    #1 0x80d0d67 in ihevca_aligned_malloc /libhevc1217/t1.c:445
    #2 0x811ffbc in ihevcd_allocate_static_bufs /libhevc1217/decoder/ihevcd_api.c:1218
    #3 0x8123e8b in ihevcd_create /libhevc1217/decoder/ihevcd_api.c:2092
    #4 0x80d5bfe in main /libhevc1217/t1.c:2065
    #5 0xf758baf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-buffer-overflow /libhevc1217/decoder/ihevcd_bitstream.c:254 ihevcd_bits_seek
Shadow bytes around the buggy address:
  0x3eadfca0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3eadfcb0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3eadfcc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3eadfcd0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3eadfce0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x3eadfcf0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa[fa]
  0x3eadfd00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3eadfd10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3eadfd20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3eadfd30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3eadfd40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==3338==ABORTING

