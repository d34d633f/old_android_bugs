Android libhevc overflow

How to reproduce:
1) download libhevc src (repo sync external/libhevc)
2) compile standalone decoder with and without ASAN
$ cd libhevc
$ cp test/decoder/main.c t1.c
$ cp test/decoder/test.cfg .

ASAN LOG:
$ ./t1a
Using test.cfg as configuration file 
0
515
Ittiam Decoder Version number: @(#)Id:HEVCDEC_production Ver:05.00 Released by ITTIAM Build: Sep 15 2017 @ 22:06:26
7150
6818
9672
21994
16945
13595
8265
4212
15367
8065
8892
6731
24803
9279
10019
10697
8920
9539
13999
12697
11770
8797
3598
16551
5591
7344
8112
8171
21137
1599
10273
12470
10001
ASAN:SIGSEGV
=================================================================
==20638==ERROR: AddressSanitizer: SEGV on unknown address 0x8dcefed0 (pc 0xf769de6d sp 0xffa52e74 bp 0xffa52eb8 T0)
    #0 0xf769de6c (/lib/i386-linux-gnu/libc.so.6+0x12ee6c)
    #1 0x80a5b8b in __interceptor_memset (/android/libhevc_fuzz/bugs/31/t1a+0x80a5b8b)
    #2 0x817447f in ihevcd_unpack_coeffs /android/libhevc0917/decoder/ihevcd_iquant_itrans_recon_ctb.c:248
    #3 0x8176b22 in ihevcd_iquant_itrans_recon_ctb /android/libhevc0917/decoder/ihevcd_iquant_itrans_recon_ctb.c:839
    #4 0x815ed13 in ihevcd_process /android/libhevc0917/decoder/ihevcd_process_slice.c:962
    #5 0x81501de in ihevcd_parse_slice_data /android/libhevc0917/decoder/ihevcd_parse_slice.c:3369
    #6 0x812f6de in ihevcd_nal_unit /android/libhevc0917/decoder/ihevcd_nal.c:406
    #7 0x812b8e5 in ihevcd_decode /android/libhevc0917/decoder/ihevcd_decode.c:644
    #8 0x80d86d3 in main /android/libhevc0917/t1.c:2753
    #9 0xf7588af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #10 0x80d0c54 in _start (/android/libhevc_fuzz/bugs/31/t1a+0x80d0c54)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV ??:0 ??
==20638==ABORTING

