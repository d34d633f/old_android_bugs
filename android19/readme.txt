Android libhevc out of bound read.
Looks like it is a duplicate of android16 bug.

How to reproduce:
1) checkout libhevc
2) compile standalone decoder test/decoder/main.c
3) run decoder using supplied test.cfg

ASAN trace:
==20249==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf5501f78 at pc 0x80a55f6 bp 0xffcad8e8 sp 0xffcad4cc
READ of size 1440 at 0xf5501f78 thread T0
    #0 0x80a55f5 in __interceptor_memcpy (/android/libhevc_fuzz/t1a+0x80a55f5)
    #1 0x813925f in ihevcd_copy_pps /android/libhevc1410/decoder/ihevcd_parse_headers.c:1928
    #2 0x812e986 in ihevcd_nal_unit /android/libhevc1410/decoder/ihevcd_nal.c:447
    #3 0x812ac79 in ihevcd_decode /android/libhevc1410/decoder/ihevcd_decode.c:604
    #4 0x80d62b7 in main /android/libhevc1410/t1.c:2224
    #5 0xf74c3af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #6 0x80d0a64 in _start (/android/libhevc_fuzz/t1a+0x80d0a64)

0xf5501f78 is located 0 bytes to the right of 7800-byte region [0xf5500100,0xf5501f78)
allocated by thread T0 here:
    #0 0x80b99b1 in __interceptor_memalign (/android/libhevc_fuzz/t1a+0x80b99b1)
    #1 0x80d0b57 in ihevca_aligned_malloc /android/libhevc1410/t1.c:449
    #2 0x81212dc in ihevcd_allocate_dynamic_bufs /android/libhevc1410/decoder/ihevcd_api.c:1476
    #3 0x812b2c9 in ihevcd_decode /android/libhevc1410/decoder/ihevcd_decode.c:671
    #4 0x80d62b7 in main /android/libhevc1410/t1.c:2224
    #5 0xf74c3af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 __interceptor_memcpy


