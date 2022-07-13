Android libavc invalid ptr free

How to reproduce:
1) checkout libavc
2) compile standalone decoder test/decoder/main.c with ASAN
3) run decoder: ./dec -i 1.bin


ASAN trace:

==1466==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0xf3c00800 in thread T0
    #0 0x80bb611 in free (/android/libavc_fuzz/t1a+0x80bb611)
    #1 0x80d2cb0 in ih264a_aligned_free /android/libavc1410/decoder/t1.c:458
    #2 0x811d0bc in ih264d_free_dynamic_bufs /android/libavc1410/decoder/ih264d_utils.c:2197
    #3 0x80e8ac9 in ih264d_delete /android/libavc1410/decoder/ih264d_api.c:3104
    #4 0x80e9bf2 in ih264d_api_function /android/libavc1410/decoder/ih264d_api.c:3568
    #5 0x80db09c in main /android/libavc1410/decoder/t1.c:3106
    #6 0xf7579af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #7 0x80d2ba4 in _start (/android/libavc1410/t1a+0x80d2ba4)

This testcase also trigger another out of bound read bug:
==1744==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf3bff410 at pc 0x81a2482 bp 0xffd9ce18 sp 0xffd9ce10
READ of size 16 at 0xf3bff410 thread T0
    #0 0x81a2481 in ih264_weighted_pred_chroma_sse42 /dist/src/android/libavc1410/decoder/common/x86/ih264_weighted_pred_sse42.c:659:49
    #1 0x80ee86f in ih264d_motion_compensate_mp /dist/src/android/libavc1410/decoder/ih264d_inter_pred.c:1306
    #2 0x81513d4 in ih264d_decode_recon_tfr_nmb /dist/src/android/libavc1410/decoder/ih264d_process_pslice.c:413
    #3 0x8101a97 in ih264d_mark_err_slice_skip /dist/src/android/libavc1410/decoder/ih264d_parse_pslice.c:1847
    #4 0x8114752 in ih264d_parse_decode_slice /dist/src/android/libavc1410/decoder/ih264d_parse_slice.c:1391
    #5 0x8167260 in ih264d_parse_nal_unit /dist/src/android/libavc1410/decoder/ih264d_parse_headers.c:1116
    #6 0x80e3a20 in ih264d_video_decode /dist/src/android/libavc1410/decoder/ih264d_api.c:2059
    #7 0x80da512 in main /dist/src/android/libavc1410/decoder/t1.c:2852
    #8 0xf7501af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #9 0x80d2ba4 in _start (/dist/src/android/libavc_fuzz/t1a+0x80d2ba4)

0xf3bff410 is located 16 bytes to the right of 2755584-byte region [0xf395e800,0xf3bff400)
allocated by thread T0 here:
    #0 0x80bbaf1 in __interceptor_memalign (/dist/src/android/libavc_fuzz/t1a+0x80bbaf1)
    #1 0x80d2c97 in ih264a_aligned_malloc /dist/src/android/libavc1410/decoder/t1.c:452
    #2 0x811c357 in ih264d_allocate_dynamic_bufs /dist/src/android/libavc1410/decoder/ih264d_utils.c:2087
    #3 0x811a3ce in ih264d_init_pic /dist/src/android/libavc1410/decoder/ih264d_utils.c:825
    #4 0x810e739 in ih264d_start_of_pic /dist/src/android/libavc1410/decoder/ih264d_parse_slice.c:338
    #5 0x8115a21 in ih264d_parse_decode_slice /dist/src/android/libavc1410/decoder/ih264d_parse_slice.c:1587
    #6 0x8167260 in ih264d_parse_nal_unit /dist/src/android/libavc1410/decoder/ih264d_parse_headers.c:1116
    #7 0x80e3a20 in ih264d_video_decode /dist/src/android/libavc1410/decoder/ih264d_api.c:2059
    #8 0x80da512 in main /dist/src/android/libavc1410/decoder/t1.c:2852
    #9 0xf7501af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-buffer-overflow /dist/src/android/libavc1410/decoder/common/x86/ih264_weighted_pred_sse42.c:659 ih264_weighted_pred_chroma_sse42

