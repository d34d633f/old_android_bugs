Android libhevc overflow

How to reproduce:
1) download libhevc src (repo sync external/libhevc)
2) compile standalone decoder with ASAN
$ cd libhevc
$ cp test/decoder/main.c t1.c
$ cp test/decoder/test.cfg .


Source code:

IHEVCD_ERROR_T ihevcd_parse_user_data_registered_itu_t_t35(codec_t *ps_codec,
                                                           UWORD32 u4_payload_size)
{
    parse_ctxt_t *ps_parse = &ps_codec->s_parse;
    bitstrm_t *ps_bitstrm = &ps_parse->s_bitstrm;
    UWORD32 value;
    user_data_registered_itu_t_t35_t *ps_user_data_registered_itu_t_t35;
    UWORD32 i;
    UWORD32 j = 0;

    ps_parse->s_sei_params.i1_user_data_registered_present_flag = 1;
    ps_user_data_registered_itu_t_t35 =
                    &ps_parse->s_sei_params.as_user_data_registered_itu_t_t35[ps_parse->s_sei_params.i
4_sei_user_data_cnt];
[1]  ps_parse->s_sei_params.i4_sei_user_data_cnt++;

    ps_user_data_registered_itu_t_t35->i4_payload_size = u4_payload_size;

    if(u4_payload_size > MAX_USERDATA_PAYLOAD)
    {
        u4_payload_size = MAX_USERDATA_PAYLOAD;
    }
    ps_user_data_registered_itu_t_t35->i4_valid_payload_size = u4_payload_size;

    BITS_PARSE("itu_t_t35_country_code", value, ps_bitstrm, 8);
    ps_user_data_registered_itu_t_t35->u1_itu_t_t35_country_code = value;

    if(0xFF != ps_user_data_registered_itu_t_t35->u1_itu_t_t35_country_code)
    {
        i = 1;
    }
    else
    {
        BITS_PARSE("itu_t_t35_country_code_extension_byte", value, ps_bitstrm,
                   8);
        ps_user_data_registered_itu_t_t35->u1_itu_t_t35_country_code_extension_byte =
                        value;

        i = 2;
    }

    do
    {
        BITS_PARSE("itu_t_t35_payload_byte", value, ps_bitstrm, 8);
        ps_user_data_registered_itu_t_t35->u1_itu_t_t35_payload_byte[j++] =
                        value;

        i++;
    }while(i < u4_payload_size);

...
}

The problem here is that ps_parse->s_sei_params.i4_sei_user_data_cnt variable is incremented on line #1 and it is not verified against the size of ps_parse->s_sei_params.as_user_data_registered_itu_t_t35 array. So repeated calls to ihevcd_parse_user_data_registered_itu_t_t35() will overflow this array.

ASAN LOG:

./t1a
Using test.cfg as configuration file 
0
64
0
Ittiam Decoder Version number: @(#)Id:HEVCDEC_production Ver:05.00 Released by ITTIAM Build: Sep 15 2017 @ 22:06:26
=================================================================
==4578==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf580b5fc at pc 0x813c3f3 bp 0xffd93828 sp 0xffd93820
WRITE of size 4 at 0xf580b5fc thread T0
    #0 0x813c3f2 in ihevcd_parse_user_data_registered_itu_t_t35 /src/android/libhevc0917/decoder/ihevcd_parse_headers.c:2505
    #1 0x813c54b in ihevcd_parse_sei_payload /src/android/libhevc0917/decoder/ihevcd_parse_headers.c:2594
    #2 0x813c94e in ihevcd_parse_sei /src/android/libhevc0917/decoder/ihevcd_parse_headers.c:2757
    #3 0x812f724 in ihevcd_nal_unit /src/android/libhevc0917/decoder/ihevcd_nal.c:461
    #4 0x812b8e5 in ihevcd_decode /src/android/libhevc0917/decoder/ihevcd_decode.c:644
    #5 0x80d86d3 in main /src/android/libhevc0917/t1.c:2753
    #6 0xf74d1af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #7 0x80d0c54 in _start (/src/android/libhevc_fuzz/t1a+0x80d0c54)

0xf580b5fc is located 220 bytes to the right of 45344-byte region [0xf5800400,0xf580b520)
allocated by thread T0 here:
    #0 0x80b9ba1 in __interceptor_memalign (/src/android/libhevc_fuzz/t1a+0x80b9ba1)
    #1 0x80d0d47 in ihevca_aligned_malloc /src/android/libhevc0917/t1.c:445
    #2 0x811fd00 in ihevcd_allocate_static_bufs /src/android/libhevc0917/decoder/ihevcd_api.c:1177
    #3 0x8123e6b in ihevcd_create /src/android/libhevc0917/decoder/ihevcd_api.c:2092
    #4 0x80d5bde in main /src/android/libhevc0917/t1.c:2065
    #5 0xf74d1af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-buffer-overflow /src/android/libhevc0917/decoder/ihevcd_parse_headers.c:2505 ihevcd_parse_user_data_registered_itu_t_t35
Shadow bytes around the buggy address:
  0x3eb01660: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3eb01670: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3eb01680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3eb01690: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3eb016a0: 00 00 00 00 fa fa fa fa fa fa fa fa fa fa fa fa
=>0x3eb016b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa[fa]
  0x3eb016c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3eb016d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3eb016e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3eb016f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3eb01700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==4578==ABORTING

