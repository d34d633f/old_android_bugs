Android libhevc overflows

Corrupted bitstream actually triggers two bugs in libhevc (out of bounds read and stack overflow).

How to reproduce:
1) download libavc src (repo sync external/libavc)
2) compile standalone decoder with and without ASAN
$ cd libhevc
$ cp test/decoder/main.c t1.c
$ cp test/decoder/test.cfg .

If we compile decoder without ASAN and run undef gdb:
$ gdb -q ./t1 
(gdb) r
Starting program: //dist/src/android/libhevc_fuzz/bugs0117_5/4/t1 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Using test.cfg as configuration file 
0
75
Ittiam Decoder Version number: @(#)Id:HEVCDEC_production Ver:05.00 Released by ITTIAM Build: Jan 31 2017 @ 14:49:09
*** stack smashing detected ***: //dist/src/android/libhevc_fuzz/bugs0117_5/4/t1 terminated

Program received signal SIGABRT, Aborted.
0xf7fdbc90 in __kernel_vsyscall ()
(gdb) bt
#0  0xf7fdbc90 in __kernel_vsyscall ()
#1  0xf7e1c687 in __GI_raise (sig=sig@entry=6) at ../nptl/sysdeps/unix/sysv/linux/raise.c:56
#2  0xf7e1fab3 in __GI_abort () at abort.c:89
#3  0xf7e56fd3 in __libc_message (do_abort=do_abort@entry=1, fmt=fmt@entry=0xf7f5145b "*** %s ***: %s terminated\n")
    at ../sysdeps/posix/libc_fatal.c:175
#4  0xf7ee9b8b in __GI___fortify_fail (msg=<optimized out>, msg@entry=0xf7f51443 "stack smashing detected")
    at fortify_fail.c:38
#5  0xf7ee9b1a in __stack_chk_fail () at stack_chk_fail.c:28
#6  0x08076d5e in ihevcd_iquant_itrans_recon_ctb (ps_proc=0x80808080) at decoder/ihevcd_iquant_itrans_recon_ctb.c:1159
#7  0x80808080 in ?? ()
#8  0x80808080 in ?? ()
#9  0x80808080 in ?? ()
#10 0x80808080 in ?? ()
#11 0x80808080 in ?? ()
#12 0x80808080 in ?? ()
#13 0x80808080 in ?? ()
#14 0x80808080 in ?? ()
#15 0x80808080 in ?? ()
#16 0x80808080 in ?? ()
#17 0x80808080 in ?? ()
#18 0x80808080 in ?? ()
#19 0x80808080 in ?? ()
#20 0x80808080 in ?? ()
#21 0x80808080 in ?? ()
#22 0x80808080 in ?? ()
#23 0x80808080 in ?? ()
#24 0x80808080 in ?? ()
#25 0x80808080 in ?? ()
#26 0x80808080 in ?? ()
#27 0x80808080 in ?? ()


Compile with ASAN and run it again:
$./t1a
Using test.cfg as configuration file 
0
75
Ittiam Decoder Version number: @(#)Id:HEVCDEC_production Ver:05.00 Released by ITTIAM Build: Jan 31 2017 @ 14:48:37
=================================================================
==8739==ERROR: AddressSanitizer: global-buffer-overflow on address 0x08224994 at pc 0x8151483 bp 0xff9e58b8 sp 0xff9e58b0
READ of size 1 at 0x08224994 thread T0
    #0 0x8151482 in ihevcd_parse_residual_coding //dist/src/android/libhevc_test/decoder/ihevcd_parse_residual.c:378
    #1 0x813fe5b in ihevcd_parse_transform_tree //dist/src/android/libhevc_test/decoder/ihevcd_parse_slice.c:325
    #2 0x8143865 in ihevcd_parse_coding_unit //dist/src/android/libhevc_test/decoder/ihevcd_parse_slice.c:1597
    #3 0x81448e8 in ihevcd_parse_coding_quadtree //dist/src/android/libhevc_test/decoder/ihevcd_parse_slice.c:1848
    #4 0x8148b91 in ihevcd_parse_slice_data //dist/src/android/libhevc_test/decoder/ihevcd_parse_slice.c:2576
    #5 0x812ef23 in ihevcd_nal_unit //dist/src/android/libhevc_test/decoder/ihevcd_nal.c:405
    #6 0x812b449 in ihevcd_decode //dist/src/android/libhevc_test/decoder/ihevcd_decode.c:604
    #7 0x80d8523 in main //dist/src/android/libhevc_test/t1.c:2753
    #8 0xf74ebaf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #9 0x80d0aa4 in _start (//dist/src/android/libhevc_fuzz/bugs0117_5/4/t1a+0x80d0aa4)

0x08224994 is located 44 bytes to the left of global variable 'gau1_ihevc_chroma_qp_scale' from 'common/ihevc_common_tables.c' (0x82249c0) of size 58
0x08224994 is located 8 bytes to the right of global variable 'gau1_ihevc_scan2x2' from 'common/ihevc_common_tables.c' (0x8224980) of size 12
SUMMARY: AddressSanitizer: global-buffer-overflow //dist/src/android/libhevc_test/decoder/ihevcd_parse_residual.c:378 ihevcd_parse_residual_coding
Shadow bytes around the buggy address:
  0x210448e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x210448f0: f9 f9 f9 f9 00 00 00 00 00 00 f9 f9 f9 f9 f9 f9
  0x21044900: 00 04 f9 f9 f9 f9 f9 f9 00 00 00 00 00 00 00 00
  0x21044910: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x21044920: f9 f9 f9 f9 00 00 00 00 00 00 f9 f9 f9 f9 f9 f9
=>0x21044930: 00 04[f9]f9 f9 f9 f9 f9 00 00 00 00 00 00 00 02
  0x21044940: f9 f9 f9 f9 00 00 00 00 00 00 00 00 00 00 02 f9
  0x21044950: f9 f9 f9 f9 00 00 00 00 00 00 00 00 01 f9 f9 f9
  0x21044960: f9 f9 f9 f9 00 00 00 00 f9 f9 f9 f9 00 00 00 00
  0x21044970: 00 00 00 00 00 00 00 00 00 00 00 00 00 04 f9 f9
  0x21044980: f9 f9 f9 f9 00 00 00 00 00 00 00 f9 f9 f9 f9 f9
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
==8739==ABORTING

