Android libavc heap overflow

How to reproduce:
1) checkout libavc
2) compile standalone decoder test/decoder/main.c with ASAN
3) run decoder: ./dec -i 1.bin

ASAN log:

==3010==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf4805a00 at pc 0x81502c2 bp 0xffcf0fb8 sp 0xffcf0fb0
WRITE of size 88 at 0xf4805a00 thread T0
    #0 0x81502c1 in ih264d_insert_pic_in_ref_pic_listx /src/android/libavc0117/decoder/ih264d_process_pslice.c:67
    #1 0x8154304 in ih264d_init_ref_idx_lx_p /src/android/libavc0117/decoder/ih264d_process_pslice.c:1076
    #2 0x8104046 in ih264d_parse_pslice /src/android/libavc0117/decoder/ih264d_parse_pslice.c:1977
    #3 0x8118416 in ih264d_parse_decode_slice /src/android/libavc0117/decoder/ih264d_parse_slice.c:1894
    #4 0x8167e80 in ih264d_parse_nal_unit /src/android/libavc0117/decoder/ih264d_parse_headers.c:1116
    #5 0x80e3a60 in ih264d_video_decode /src/android/libavc0117/decoder/ih264d_api.c:2092
    #6 0x80da542 in main /src/android/libavc0117/decoder/t1.c:2852
    #7 0xf7548af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #8 0x80d2bd4 in _start (/src/android/libavc_fuzz/bugs/5/t1a+0x80d2bd4)

0xf4805a00 is located 0 bytes to the right of 22528-byte region [0xf4800200,0xf4805a00)
allocated by thread T0 here:
    #0 0x80bbb21 in __interceptor_memalign (/src/android/libavc_fuzz/bugs/5/t1a+0x80bbb21)
    #1 0x80d2cc7 in ih264a_aligned_malloc /src/android/libavc0117/decoder/t1.c:452
    #2 0x80e10a4 in ih264d_allocate_static_bufs /src/android/libavc0117/decoder/ih264d_api.c:1402
    #3 0x80e1a15 in ih264d_create /src/android/libavc0117/decoder/ih264d_api.c:1503
    #4 0x80d7cc1 in main /src/android/libavc0117/decoder/t1.c:2133
    #5 0xf7548af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-buffer-overflow /src/android/libavc0117/decoder/ih264d_process_pslice.c:67 ih264d_insert_pic_in_ref_pic_listx
Shadow bytes around the buggy address:
  0x3e900af0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3e900b00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3e900b10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3e900b20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3e900b30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x3e900b40:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3e900b50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3e900b60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3e900b70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3e900b80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3e900b90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==3010==ABORTING

