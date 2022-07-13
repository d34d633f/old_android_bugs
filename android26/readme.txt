Android libavc out of bounds read bug

How to reproduce:
1) checkout libavc
2) compile standalone decoder test/decoder/main.c with ASAN
3) run decoder: ./dec -i 1.bin


ASAN trace:
==19261==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf5fff2e0 at pc 0x8396e36 bp 0xffcd8c58 sp 0xffcd8c50
READ of size 16 at 0xf5fff2e0 thread T0
    #0 0x8396e35 in ih264d_copy_intra_pred_line libavc/decoder/ih264d_deblocking.c:1288
    #1 0x83cdf92 in ih264d_decode_recon_tfr_nmb libavc/decoder/ih264d_process_pslice.c:442
    #2 0x81e46b7 in ih264d_mark_err_slice_skip libavc/decoder/ih264d_parse_pslice.c:1847
    #3 0x82490e8 in ih264d_parse_decode_slice libavc/decoder/ih264d_parse_slice.c:1391
    #4 0x8476023 in ih264d_parse_nal_unit libavc/decoder/ih264d_parse_headers.c:1116
    #5 0x8111734 in ih264d_video_decode libavc/decoder/ih264d_api.c:2059
    #6 0x813092b in ih264d_api_function libavc/decoder/ih264d_api.c:3573
    #7 0x80ef6f7 in main libavc/decoder/t1.c:2852
    #8 0xf754caf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #9 0x80d2b74 in _start (/tmp/t1+0x80d2b74)

0xf5fff2e0 is located 736 bytes to the right of 645120-byte region [0xf5f61800,0xf5fff000)
allocated by thread T0 here:
    #0 0x80bbac1 in __interceptor_memalign (/tmp/t1+0x80bbac1)
    #1 0x80d2f18 in ih264a_aligned_malloc libavc/decoder/t1.c:452
    #2 0x8273402 in ih264d_allocate_dynamic_bufs libavc/decoder/ih264d_utils.c:2087
    #3 0x8266b06 in ih264d_init_pic libavc/decoder/ih264d_utils.c:825
    #4 0x8230708 in ih264d_start_of_pic libavc/decoder/ih264d_parse_slice.c:338
    #5 0x824e23e in ih264d_parse_decode_slice libavc/decoder/ih264d_parse_slice.c:1587
    #6 0x8476023 in ih264d_parse_nal_unit libavc/decoder/ih264d_parse_headers.c:1116
    #7 0x8111734 in ih264d_video_decode libavc/decoder/ih264d_api.c:2059
    #8 0x813092b in ih264d_api_function libavc/decoder/ih264d_api.c:3573
    #9 0x80ef6f7 in main libavc/decoder/t1.c:2852
    #10 0xf754caf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-buffer-overflow libavc/decoder/ih264d_deblocking.c:1288 ih264d_copy_intra_pred_line

