Android libavc use-after-free bug

How to reproduce:
1) checkout libavc
2) compile standalone decoder test/decoder/main.c with ASAN
3) run decoder: ./dec -i 1.bin

ASAN trace:
==10446==ERROR: AddressSanitizer: heap-use-after-free on address 0xf5d6d800 at pc 0x82c0874 bp 0xffd7b218 sp 0xffd7b210
READ of size 1 at 0xf5d6d800 thread T0
    #0 0x82c0873 in ih264d_one_to_one /android/libavc1410/decoder/ih264d_process_bslice.c:1601
    #1 0x829a433 in ih264d_decode_spatial_direct /android/libavc1410/decoder/ih264d_process_bslice.c:220
    #2 0x8331a2b in ih264d_mv_pred_ref_tfr_nby2_bmb /android/libavc1410/decoder/ih264d_parse_bslice.c:1025
    #3 0x81cf2a5 in ih264d_parse_inter_slice_data_cabac /android/libavc1410/decoder/ih264d_parse_pslice.c:1045
    #4 0x8343e51 in ih264d_parse_bslice /android/libavc1410/decoder/ih264d_parse_bslice.c:1702
    #5 0x8255022 in ih264d_parse_decode_slice /android/libavc1410/decoder/ih264d_parse_slice.c:1902
    #6 0x8476023 in ih264d_parse_nal_unit /android/libavc1410/decoder/ih264d_parse_headers.c:1116
    #7 0x8111734 in ih264d_video_decode /android/libavc1410/decoder/ih264d_api.c:2059
    #8 0x813092b in ih264d_api_function /android/libavc1410/decoder/ih264d_api.c:3573
    #9 0x80ef6f7 in main /android/libavc1410/decoder/t1.c:2852
    #10 0xf754aaf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #11 0x80d2b74 in _start (/android/libavc_fuzz/debug/t1+0x80d2b74)

0xf5d6d800 is located 0 bytes inside of 595584-byte region [0xf5d6d800,0xf5dfee80)
freed by thread T0 here:
    #0 0x80bb5e1 in free (/android/libavc_fuzz/debug/t1+0x80bb5e1)
    #1 0x80d31c1 in ih264a_aligned_free /android/libavc1410/decoder/t1.c:458
    #2 0x82797dd in ih264d_free_dynamic_bufs /android/libavc1410/decoder/ih264d_utils.c:2239
    #3 0x80f4a87 in ih264d_init_decoder /android/libavc1410/decoder/ih264d_api.c:931
    #4 0x8128548 in ih264d_reset /android/libavc1410/decoder/ih264d_api.c:3140
    #5 0x8129461 in ih264d_ctl /android/libavc1410/decoder/ih264d_api.c:3201
    #6 0x8130f43 in ih264d_api_function /android/libavc1410/decoder/ih264d_api.c:3595
    #7 0x80eff1f in main /android/libavc1410/decoder/t1.c:2918
    #8 0xf754aaf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

previously allocated by thread T0 here:
    #0 0x80bbac1 in __interceptor_memalign (/android/libavc_fuzz/debug/t1+0x80bbac1)
    #1 0x80d2f18 in ih264a_aligned_malloc /android/libavc1410/decoder/t1.c:452
    #2 0x827281c in ih264d_allocate_dynamic_bufs /android/libavc1410/decoder/ih264d_utils.c:2054
    #3 0x8266b06 in ih264d_init_pic /android/libavc1410/decoder/ih264d_utils.c:825
    #4 0x8230708 in ih264d_start_of_pic /android/libavc1410/decoder/ih264d_parse_slice.c:338
    #5 0x824e23e in ih264d_parse_decode_slice /android/libavc1410/decoder/ih264d_parse_slice.c:1587
    #6 0x8476023 in ih264d_parse_nal_unit /android/libavc1410/decoder/ih264d_parse_headers.c:1116
    #7 0x8111734 in ih264d_video_decode /android/libavc1410/decoder/ih264d_api.c:2059
    #8 0x813092b in ih264d_api_function /android/libavc1410/decoder/ih264d_api.c:3573
    #9 0x80ef6f7 in main /android/libavc1410/decoder/t1.c:2852
    #10 0xf754aaf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-use-after-free /android/libavc1410/decoder/ih264d_process_bslice.c:1601 ih264d_one_to_one

