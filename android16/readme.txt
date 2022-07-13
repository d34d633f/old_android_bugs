Android libhevc out of bounds read bug

How to reproduce:
1) checkout libhevc
2) compile standalone decoder test/decoder/main.c with ASAN
3) run decoder using supplied test.cfg

ASAN trace:
==18632==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf511762f at pc 0x81393b6 bp 0xffd64be8 sp 0xffd64be0
READ of size 1584 at 0xf511762f thread T0
    #0 0x81393b5 in ihevcd_copy_pps /android/libhevc1410/decoder/ihevcd_parse_headers.c:1928
    #1 0x812e986 in ihevcd_nal_unit /android/libhevc1410/decoder/ihevcd_nal.c:447
    #2 0x812ac79 in ihevcd_decode /android/libhevc1410/decoder/ihevcd_decode.c:604
    #3 0x80d62b7 in main /android/libhevc1410/t1.c:2224
    #4 0xf753faf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #5 0x80d0a64 in _start (/android/libhevc_fuzz/t1a+0x80d0a64)

0xf511762f is located 143 bytes to the right of 93600-byte region [0xf5100800,0xf51175a0)
allocated by thread T0 here:
    #0 0x80b99b1 in __interceptor_memalign (/android/libhevc_fuzz/t1a+0x80b99b1)
    #1 0x80d0b57 in ihevca_aligned_malloc /android/libhevc1410/t1.c:449
    #2 0x81212dc in ihevcd_allocate_dynamic_bufs /android/libhevc1410/decoder/ihevcd_api.c:1476
    #3 0x812b2c9 in ihevcd_decode /android/libhevc1410/decoder/ihevcd_decode.c:671
    #4 0x80d62b7 in main /android/libhevc1410/t1.c:2224
    #5 0xf753faf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-buffer-overflow /android/libhevc1410/decoder/ihevcd_parse_headers.c:1928 ihevcd_copy_pps

