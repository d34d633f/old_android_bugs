Android libhevc heap overflow

How to reproduce:
1) checkout libhevc
2) compile standalone decoder test/decoder/main.c with ASAN
3) run decoder using supplied test.cfg

ASAN trace:

==5214==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf4f0619f at pc 0x81393b6 bp 0xffc51088 sp 0xffc51080
READ of size 1440 at 0xf4f0619f thread T0
    #0 0x81393b5 in ihevcd_copy_pps /home/el/dist/src/android/libhevc1410/decoder/ihevcd_parse_headers.c:1928
    #1 0x812e986 in ihevcd_nal_unit /home/el/dist/src/android/libhevc1410/decoder/ihevcd_nal.c:447
    #2 0x812ac79 in ihevcd_decode /home/el/dist/src/android/libhevc1410/decoder/ihevcd_decode.c:604
    #3 0x80d62b7 in main /home/el/dist/src/android/libhevc1410/t1.c:2224
    #4 0xf7563af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #5 0x80d0a64 in _start (/home/el/dist/src/android/libhevc_fuzz/bugs/t1a+0x80d0a64)

AddressSanitizer can not describe address in more detail (wild memory access suspected).
SUMMARY: AddressSanitizer: heap-buffer-overflow /home/el/dist/src/android/libhevc1410/decoder/ihevcd_parse_headers.c:1928 ihevcd_copy_pps

