Android libavc heap overflow bug

How to reproduce:
1) checkout libavc
2) compile standalone decoder test/decoder/main.c with ASAN
3) run decoder: ./dec -i 1.bin


ASAN trace:
==10463==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf4002da3 at pc 0x8395a4e bp 0xff8a3ab8 sp 0xff8a3ab0
WRITE of size 1 at 0xf4002da3 thread T0
    #0 0x8395a4d in ih264d_set_deblocking_parameters /android/libavc1410/decoder/ih264d_deblocking.c:1241
    #1 0x81e2782 in ih264d_mark_err_slice_skip /android/libavc1410/decoder/ih264d_parse_pslice.c:1776
    #2 0x82490e8 in ih264d_parse_decode_slice /android/libavc1410/decoder/ih264d_parse_slice.c:1391
    #3 0x8476023 in ih264d_parse_nal_unit /android/libavc1410/decoder/ih264d_parse_headers.c:1116
    #4 0x8111734 in ih264d_video_decode /android/libavc1410/decoder/ih264d_api.c:2059
    #5 0x813092b in ih264d_api_function /android/libavc1410/decoder/ih264d_api.c:3573
    #6 0x80ef6f7 in main /android/libavc1410/decoder/t1.c:2852
    #7 0xf7553af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #8 0x80d2b74 in _start (/android/libavc_fuzz/debug/t1+0x80d2b74)

0xf4002da3 is located 3 bytes to the right of 5280-byte region [0xf4001900,0xf4002da0)
allocated by thread T0 here:
    #0 0x80bbac1 in __interceptor_memalign (/android/libavc_fuzz/debug/t1+0x80bbac1)
    #1 0x80d2f18 in ih264a_aligned_malloc /android/libavc1410/decoder/t1.c:452
    #2 0x826fdfd in ih264d_allocate_dynamic_bufs /android/libavc1410/decoder/ih264d_utils.c:1973
    #3 0x8266b06 in ih264d_init_pic /android/libavc1410/decoder/ih264d_utils.c:825
    #4 0x8230708 in ih264d_start_of_pic /android/libavc1410/decoder/ih264d_parse_slice.c:338
    #5 0x824e23e in ih264d_parse_decode_slice /android/libavc1410/decoder/ih264d_parse_slice.c:1587
    #6 0x8476023 in ih264d_parse_nal_unit /android/libavc1410/decoder/ih264d_parse_headers.c:1116
    #7 0x8111734 in ih264d_video_decode /android/libavc1410/decoder/ih264d_api.c:2059
    #8 0x813092b in ih264d_api_function /android/libavc1410/decoder/ih264d_api.c:3573
    #9 0x80ef6f7 in main /android/libavc1410/decoder/t1.c:2852
    #10 0xf7553af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-buffer-overflow /android/libavc1410/decoder/ih264d_deblocking.c:1241 ih264d_set_deblocking_parameters

