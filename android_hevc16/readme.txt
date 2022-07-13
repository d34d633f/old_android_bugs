Android libhevc overflow

How to reproduce:
1) download libhevc src (repo sync external/libhevc)
2) compile standalone decoder with and without ASAN
$ cd libhevc
$ cp test/decoder/main.c t1.c
$ cp test/decoder/test.cfg .

$ ./t1a
Using test.cfg as configuration file 
0
515
Ittiam Decoder Version number: @(#)Id:HEVCDEC_production Ver:05.00 Released by ITTIAM Build: Nov 16 2017 @ 05:36:42
7150
6818
9672
10313
11681
8649
11955
13262
8140
5863
3373
13779
8026
8263
7284
27560
3783
6236
10697
8920
9539
13999
12697
11770
8797
3598
ASAN:DEADLYSIGNAL
=================================================================
==26860==ERROR: AddressSanitizer: SEGV on unknown address 0x90f3238d (pc 0x081a83b4 bp 0xffd67dc8 sp 0xffd67db0 T0)
==26860==The signal is caused by a WRITE memory access.
    #0 0x81a83b3 in ihevc_dpb_mgr_insert_ref /tt/common/ihevc_dpb_mgr.c:156:42
    #1 0x81b9317 in ihevcd_decode /tt/decoder/ihevcd_decode.c:873:9
    #2 0x815f73e in main /tt/t1.c:2753:19
    #3 0xf74a6275 in __libc_start_main (/lib/i386-linux-gnu/libc.so.6+0x18275)
    #4 0x8066de7 in _start (/tt/t1a+0x8066de7)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV /tt/common/ihevc_dpb_mgr.c:156:42 in ihevc_dpb_mgr_insert_ref
==26860==ABORTING
