Android libmpeg2 heap overflow 

Tested on android-7.1.2_r3 branch.

How to reproduce:
1) checkout libmpeg2
2) compile standalone decoder test/decoder/main.c with ASAN
3) run decoder using supplied test.cfg

ASAN log:

./t1a > 1.log
=================================================================
==4508==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf51fe890 at pc 0x8114d97 bp 0xffe79a98 sp 0xffe79a90
WRITE of size 8 at 0xf51fe890 thread T0
    #0 0x8114d96 in impeg2_interpolate_sse42 /dist/src/android/libmpeg2/common/x86/impeg2_inter_pred_sse42_intr.c:388
    #1 0x80fb3cd in impeg2d_dec_skip_b_mb /dist/src/android/libmpeg2/decoder/impeg2d_mc.c:698
    #2 0x80fb757 in impeg2d_dec_skip_mbs /dist/src/android/libmpeg2/decoder/impeg2d_mc.c:731
    #3 0x8104642 in impeg2d_dec_pnb_mb_params /dist/src/android/libmpeg2/decoder/impeg2d_pnb_pic.c:301
    #4 0x810532c in impeg2d_dec_p_b_slice /dist/src/android/libmpeg2/decoder/impeg2d_pnb_pic.c:493
    #5 0x80ef58f in impeg2d_dec_slice /dist/src/android/libmpeg2/decoder/impeg2d_dec_hdr.c:843
    #6 0x80efb25 in impeg2d_dec_pic_data_thread /dist/src/android/libmpeg2/decoder/impeg2d_dec_hdr.c:933
    #7 0x80f17d0 in impeg2d_dec_pic_data /dist/src/android/libmpeg2/decoder/impeg2d_dec_hdr.c:1360
    #8 0x80f4b76 in impeg2d_process_video_bit_stream /dist/src/android/libmpeg2/decoder/impeg2d_dec_hdr.c:1790
    #9 0x80f529c in impeg2d_dec_frm /dist/src/android/libmpeg2/decoder/impeg2d_decoder.c:198
    #10 0x80eb557 in impeg2d_api_entity /dist/src/android/libmpeg2/decoder/impeg2d_api_main.c:3379
    #11 0x80d5df5 in main /dist/src/android/libmpeg2/t1.c:2881
    #12 0xf74bcaf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #13 0x80cd6c4 in _start (/dist/src/android/libmpeg2_fuzz/coolbugs/3/t1a+0x80cd6c4)

0xf51fe890 is located 144 bytes to the right of 6144000-byte region [0xf4c22800,0xf51fe800)
allocated by thread T0 here:
    #0 0x80b6611 in __interceptor_memalign (/dist/src/android/libmpeg2_fuzz/coolbugs/3/t1a+0x80b6611)
    #1 0x80d30c6 in main /dist/src/android/libmpeg2/t1.c:2164
    #2 0xf74bcaf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-buffer-overflow /dist/src/android/libmpeg2/common/x86/impeg2_inter_pred_sse42_intr.c:388 impeg2_interpolate_sse42
Shadow bytes around the buggy address:
  0x3ea3fcc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ea3fcd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ea3fce0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ea3fcf0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ea3fd00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x3ea3fd10: fa fa[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ea3fd20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ea3fd30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ea3fd40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ea3fd50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ea3fd60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==4508==ABORTING

