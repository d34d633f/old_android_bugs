Android libhevc overflow

How to reproduce:
1) download libhevc src (repo sync external/libhevc)
2) compile standalone decoder with ASAN
$ cd libhevc
$ cp test/decoder/main.c t1.c
$ cp test/decoder/test.cfg .


$ /tmp/t1a
Using test.cfg as configuration file 
0
42
14
360
468
=================================================================
==4222==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf5c02e78 at pc 0x813a75f bp 0xffe9f7e8 sp 0xffe9f7e0
WRITE of size 1 at 0xf5c02e78 thread T0
    #0 0x813a75e in ihevcd_parse_pps //android/libhevc1117/decoder/ihevcd_parse_headers.c:1961
    #1 0x812f8b0 in ihevcd_nal_unit //android/libhevc1117/decoder/ihevcd_nal.c:444
    #2 0x812b96e in ihevcd_decode //android/libhevc1117/decoder/ihevcd_decode.c:645
    #3 0x80d64c5 in main //android/libhevc1117/t1.c:2218
    #4 0xf74cbaf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #5 0x80d0c54 in _start (/tmp/t1a+0x80d0c54)

0xf5c02e78 is located 66 bytes to the right of 3510-byte region [0xf5c02080,0xf5c02e36)
allocated by thread T0 here:
    #0 0x80b9ba1 in __interceptor_memalign (/tmp/t1a+0x80b9ba1)
    #1 0x80d0d47 in ihevca_aligned_malloc //android/libhevc1117/t1.c:445
    #2 0x8121a2c in ihevcd_allocate_dynamic_bufs //android/libhevc1117/decoder/ihevcd_api.c:1508
    #3 0x812bf62 in ihevcd_decode //android/libhevc1117/decoder/ihevcd_decode.c:712
    #4 0x80d64c5 in main //android/libhevc1117/t1.c:2218
    #5 0xf74cbaf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-buffer-overflow //android/libhevc1117/decoder/ihevcd_parse_headers.c:1961 ihevcd_parse_pps
Shadow bytes around the buggy address:
  0x3eb80570: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3eb80580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3eb80590: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3eb805a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3eb805b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x3eb805c0: 00 00 00 00 00 00 06 fa fa fa fa fa fa fa fa[fa]
  0x3eb805d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3eb805e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3eb805f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3eb80600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3eb80610: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==4222==ABORTING


