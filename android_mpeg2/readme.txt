Android libmpeg2 out of bounds read 

Tested on android-7.1.2_r3 branch.

How to reproduce:
1) checkout libmpeg2
2) compile standalone decoder test/decoder/main.c with ASAN
3) run decoder using supplied test.cfg

ASAN log:

$ ./t1a > 1.log

ASAN:SIGSEGV
=================================================================
==18158==ERROR: AddressSanitizer: SEGV on unknown address 0x00047a70 (pc 0x08115952 sp 0xffa70480 bp 0xffa704a8 T0)
    #0 0x8115951 in impeg2_mc_fullx_halfy_8x8_sse42 /dist/src/android/libmpeg2/common/x86/impeg2_inter_pred_sse42_intr.c:802:14
    #1 0x80fc533 in impeg2d_mc_fullx_halfy /dist/src/android/libmpeg2/decoder/impeg2d_mc.c:1098
    #2 0x80f7ab4 in impeg2d_motion_comp /dist/src/android/libmpeg2/decoder/impeg2d_mc.c:114
    #3 0x80f8826 in impeg2d_mc_fld_dual_prime /dist/src/android/libmpeg2/decoder/impeg2d_mc.c:343
    #4 0x81055da in impeg2d_dec_p_b_slice /dist/src/android/libmpeg2/decoder/impeg2d_pnb_pic.c:535
    #5 0x80ef58f in impeg2d_dec_slice /dist/src/android/libmpeg2/decoder/impeg2d_dec_hdr.c:843
    #6 0x80efb25 in impeg2d_dec_pic_data_thread /dist/src/android/libmpeg2/decoder/impeg2d_dec_hdr.c:933
    #7 0x80f17d0 in impeg2d_dec_pic_data /dist/src/android/libmpeg2/decoder/impeg2d_dec_hdr.c:1360
    #8 0x80f47e9 in impeg2d_process_video_bit_stream /dist/src/android/libmpeg2/decoder/impeg2d_dec_hdr.c:1720
    #9 0x80f529c in impeg2d_dec_frm /dist/src/android/libmpeg2/decoder/impeg2d_decoder.c:198
    #10 0x80eb557 in impeg2d_api_entity /dist/src/android/libmpeg2/decoder/impeg2d_api_main.c:3379
    #11 0x80d5df5 in main /dist/src/android/libmpeg2/t1.c:2881
    #12 0xf74c2af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #13 0x80cd6c4 in _start (/dist/src/android/libmpeg2_fuzz/t1a+0x80cd6c4)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV /dist/src/android/libmpeg2/common/x86/impeg2_inter_pred_sse42_intr.c:802 impeg2_mc_fullx_halfy_8x8_sse42
==18158==ABORTING
