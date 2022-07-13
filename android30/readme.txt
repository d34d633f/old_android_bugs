Android libhevc heap overflow

How to reproduce:
1) checkout libhevc
2) compile standalone decoder test/decoder/main.c with ASAN
3) run decoder using supplied test.cfg

ASAN trace:
==20453==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf4f02bb4 at pc 0x8138e7a bp 0xffbf88a8 sp 0xffbf88a0
WRITE of size 1 at 0xf4f02bb4 thread T0
    #0 0x8138e79 in ihevcd_parse_pps /dist/src/android/libhevc1410/decoder/ihevcd_parse_headers.c:1780
    #1 0x812e91f in ihevcd_nal_unit /dist/src/android/libhevc1410/decoder/ihevcd_nal.c:443
    #2 0x812ac79 in ihevcd_decode /dist/src/android/libhevc1410/decoder/ihevcd_decode.c:604
    #3 0x80d62b7 in main /dist/src/android/libhevc1410/t1.c:2224
    #4 0xf7558af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #5 0x80d0a64 in _start (/dist/src/android/libhevc_fuzz/bugs/t1a+0x80d0a64)

0xf4f02bb4 is located 12 bytes to the right of 10920-byte region [0xf4f00100,0xf4f02ba8)
allocated by thread T0 here:
    #0 0x80b99b1 in __interceptor_memalign (/dist/src/android/libhevc_fuzz/bugs/t1a+0x80b99b1)
    #1 0x80d0b57 in ihevca_aligned_malloc /dist/src/android/libhevc1410/t1.c:449
    #2 0x81212dc in ihevcd_allocate_dynamic_bufs /dist/src/android/libhevc1410/decoder/ihevcd_api.c:1476
    #3 0x812b2c9 in ihevcd_decode /dist/src/android/libhevc1410/decoder/ihevcd_decode.c:671
    #4 0x80d62b7 in main /dist/src/android/libhevc1410/t1.c:2224
    #5 0xf7558af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-buffer-overflow /dist/src/android/libhevc1410/decoder/ihevcd_parse_headers.c:1780 ihevcd_parse_pps


