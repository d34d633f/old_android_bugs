Android libmpeg2 heap overflow 

Tested on android-7.1.2_r12 branch.

How to reproduce:
1) checkout libmpeg2
2) compile standalone decoder test/decoder/main.c with ASAN
3) run decoder using supplied test.cfg

ASAN log:

$ ./t1a > 1.log

==27795==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf4640850 at pc 0x8113d4d bp 0xff8f2728 sp 0xff8f2720
WRITE of size 8 at 0xf4640850 thread T0
    #0 0x8113d4c in impeg2_copy_mb_sse42 /dist/src/android/libmpeg2_0617/common/x86/impeg2_inter_pred_sse42_intr.c:171
    #1 0x80f98ea in impeg2d_dec_skip_p_mb /dist/src/android/libmpeg2_0617/decoder/impeg2d_mc.c:555
    #2 0x80fb9e8 in impeg2d_dec_skip_mbs /dist/src/android/libmpeg2_0617/decoder/impeg2d_mc.c:735
    #3 0x8103e55 in impeg2d_dec_p_mb_params /dist/src/android/libmpeg2_0617/decoder/impeg2d_pnb_pic.c:109
    #4 0x810550a in impeg2d_dec_p_b_slice /dist/src/android/libmpeg2_0617/decoder/impeg2d_pnb_pic.c:495
    #5 0x80ef6cf in impeg2d_dec_slice /dist/src/android/libmpeg2_0617/decoder/impeg2d_dec_hdr.c:845
    #6 0x80efc65 in impeg2d_dec_pic_data_thread /dist/src/android/libmpeg2_0617/decoder/impeg2d_dec_hdr.c:935
    #7 0x80f1910 in impeg2d_dec_pic_data /dist/src/android/libmpeg2_0617/decoder/impeg2d_dec_hdr.c:1362
    #8 0x80f4929 in impeg2d_process_video_bit_stream /dist/src/android/libmpeg2_0617/decoder/impeg2d_dec_hdr.c:1722
    #9 0x80f551c in impeg2d_dec_frm /dist/src/android/libmpeg2_0617/decoder/impeg2d_decoder.c:205
    #10 0x80eb588 in impeg2d_api_entity /dist/src/android/libmpeg2_0617/decoder/impeg2d_api_main.c:3380
    #11 0x80d5df5 in main /dist/src/android/libmpeg2_0617/t1.c:2881
    #12 0xf758faf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #13 0x80cd6c4 in _start (/sec/zdi/0617/mpeg5/t1a+0x80cd6c4)

0xf4640850 is located 80 bytes to the right of 6144000-byte region [0xf4064800,0xf4640800)
allocated by thread T0 here:
    #0 0x80b6611 in __interceptor_memalign (/sec/zdi/0617/mpeg5/t1a+0x80b6611)
    #1 0x80d30c6 in main /dist/src/android/libmpeg2_0617/t1.c:2164
    #2 0xf758faf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-buffer-overflow /dist/src/android/libmpeg2_0617/common/x86/impeg2_inter_pred_sse42_intr.c:171 impeg2_copy_mb_sse42
Shadow bytes around the buggy address:
  0x3e8c80b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3e8c80c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3e8c80d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3e8c80e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3e8c80f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x3e8c8100: fa fa fa fa fa fa fa fa fa fa[fa]fa fa fa fa fa
  0x3e8c8110: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3e8c8120: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3e8c8130: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3e8c8140: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3e8c8150: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==27795==ABORTING

