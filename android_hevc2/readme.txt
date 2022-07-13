Android libhevc overflow

How to reproduce:
1) download libhevc src (repo sync external/libhevc)
2) compile standalone decoder with ASAN
$ cd libhevc
$ cp test/decoder/main.c t1.c
$ cp test/decoder/test.cfg .


Source code:
IHEVCD_ERROR_T ihevcd_parse_pic_timing_sei(codec_t *ps_codec, sps_t *ps_sps)
{
...
...
            UEV_PARSE("num_decoding_units_minus1", value, ps_bitstrm);
[1]         ps_pic_timing->u4_num_decoding_units_minus1 = value;

            BITS_PARSE("du_common_cpb_removal_delay_flag", value, ps_bitstrm, 1);
            ps_pic_timing->u1_du_common_cpb_removal_delay_flag = value;

            if(ps_pic_timing->u1_du_common_cpb_removal_delay_flag)
            {
                BITS_PARSE("du_common_cpb_removal_delay_increment_minus1",
                           value,
                           ps_bitstrm,
                           (ps_vui_hdr->u1_du_cpb_removal_delay_increment_length_minus1
                                           + 1));
                ps_pic_timing->u4_du_common_cpb_removal_delay_increment_minus1 =
                                value;
            }

[2]         for(i = 0; i <= ps_pic_timing->u4_num_decoding_units_minus1; i++)
            {
                UEV_PARSE("num_nalus_in_du_minus1", value, ps_bitstrm);
                ps_pic_timing->au4_num_nalus_in_du_minus1[i] = value;
...
}

The problem is that ps_pic_timing->u4_num_decoding_units_minus1 is not verified against the size of 
ps_pic_timing->au4_num_nalus_in_du_minus1 array, so on line #2 heap overflow will occur.

ASAN LOG:

Asan does not catch the overflow itself, bad free is the result of overflow.

$ ./t1a
Using test.cfg as configuration file 
0
64
0
Ittiam Decoder Version number: @(#)Id:HEVCDEC_production Ver:05.00 Released by ITTIAM Build: Sep 15 2017 @ 22:06:26
20512
=================================================================
==3328==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x31323334 in thread T0
    #0 0x80b96c1 in free (/src/android/libhevc_fuzz/t1a+0x80b96c1)
    #1 0x80d0d60 in ihevca_aligned_free /src/android/libhevc0917/t1.c:451
    #2 0x811f267 in ihevcd_free_dynamic_bufs /src/android/libhevc0917/decoder/ihevcd_api.c:2038
    #3 0x8123fe9 in ihevcd_delete /src/android/libhevc0917/decoder/ihevcd_api.c:2145
    #4 0x8128e42 in ihevcd_cxa_api_function /src/android/libhevc0917/decoder/ihevcd_api.c:3553
    #5 0x80d9342 in main /src/android/libhevc0917/t1.c:2999
    #6 0xf74eeaf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #7 0x80d0c54 in _start (/src/android/libhevc_fuzz/t1a+0x80d0c54)

AddressSanitizer can not describe address in more detail (wild memory access suspected).
SUMMARY: AddressSanitizer: bad-free ??:0 free
==3328==ABORTING

