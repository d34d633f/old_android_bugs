Android libhevc out of bounds read

How to reproduce:
1) checkout libhevc
2) compile standalone decoder test/decoder/main.c with and without ASAN 
3) run decoder using supplied test.cfg

1. run decoder (without ASAN)
$ gdb -q ./t1
Reading symbols from ./t1...done.
(gdb) r
Starting program: /dist/src/android/libhevc_fuzz/coolbugs/6/t1 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Using test.cfg as configuration file 
0
95
Ittiam Decoder Version number: @(#)Id:HEVCDEC_production Ver:05.00 Released by ITTIAM Build: Apr 27 2017 @ 10:56:53
7393
2603
1656
6279
4644
4012
1465
5007

Program received signal SIGSEGV, Segmentation fault.
0x00000000 in ?? ()
(gdb) bt
#0  0x00000000 in ?? ()
#1  0x08076a5d in ihevcd_iquant_itrans_recon_ctb (ps_proc=ps_proc@entry=0x80d5a34)
    at decoder/ihevcd_iquant_itrans_recon_ctb.c:1055
#2  0x0806fff5 in ihevcd_process (ps_proc=ps_proc@entry=0x80d5a34)
    at decoder/ihevcd_process_slice.c:962
#3  0x0806c29d in ihevcd_parse_slice_data (ps_codec=ps_codec@entry=0x80d5480)
    at decoder/ihevcd_parse_slice.c:3244
#4  0x08062f8e in ihevcd_nal_unit (ps_codec=ps_codec@entry=0x80d5480) at decoder/ihevcd_nal.c:405
#5  0x0806278a in ihevcd_decode (ps_codec_obj=<optimized out>, ps_codec_obj@entry=0x80d5400, 
    pv_api_ip=<optimized out>, pv_api_ip@entry=0xfffea2b0, pv_api_op=<optimized out>, 
    pv_api_op@entry=0xfffea098) at decoder/ihevcd_decode.c:604
#6  0x08062018 in ihevcd_cxa_api_function (ps_handle=<optimized out>, ps_handle@entry=0x80d5400, 
    pv_api_ip=pv_api_ip@entry=0xfffea2b0, pv_api_op=pv_api_op@entry=0xfffea098)
    at decoder/ihevcd_api.c:3552
#7  0x0804b2ab in main (argc=1, argv=0xffffd004) at t1.c:2753

Quick look at the code shows that it tries to dereference incorrect function ptr
From decoder/ihevcd_iquant_itrans_recon_ctb.c:
			...
			...
			{
                            tu_t *ps_tu_tmp = ps_tu;
[1]                         while(!ps_tu_tmp->b1_first_tu_in_cu)
                            {
                                ps_tu_tmp--;
                            }
[2]                         u1_luma_pred_mode_first_tu = ps_tu_tmp->b6_luma_intra_mode;
                        }
                        if(4 == u1_chroma_pred_mode)
                            u1_chroma_pred_mode = u1_luma_pred_mode_first_tu;
			....


                        chroma_pred_func_idx =
[3]                                        g_i4_ip_funcs[u1_chroma_pred_mode];

[4]                     ps_codec->apf_intra_pred_chroma[chroma_pred_func_idx](au1_ref_sub_out, 1, pu1_pred_orig, pred_strd, trans_size, u1_chroma_pred_mode);
                    

Seems like loop on #1 incorrectly decrements ps_tu_tmp variable.
After the loop it points to a memory before original ps_tu.
It will lead to incorrect value of u1_luma_pred_mode_first_tu variable, see line #2.
One line #3 u1_chrome_pred_mode is used to look up function ptr index.

----------------------------
It we run a decoder compiled with ASAN, we will get two out of bounds read bugs:

1) first bug
$ ./t1a

Using test.cfg as configuration file 
0
95
Ittiam Decoder Version number: @(#)Id:HEVCDEC_production Ver:05.00 Released by ITTIAM Build: Apr 27 2017 @ 10:56:39
=================================================================
==7545==ERROR: AddressSanitizer: stack-buffer-overflow on address 0xffb10eb8 at pc 0x81f1a72 bp 0xffb107d8 sp 0xffb107d0
READ of size 16 at 0xffb10eb8 thread T0
    #0 0x81f1a71 in ihevc_intra_pred_ref_filtering_ssse3 /dist/src/android/libhevc0417/common/x86/ihevc_intra_pred_filters_ssse3_intr.c:535
    #1 0x81729d6 in ihevcd_iquant_itrans_recon_ctb /dist/src/android/libhevc0417/decoder/ihevcd_iquant_itrans_recon_ctb.c:987
    #2 0x815b3a3 in ihevcd_process /dist/src/android/libhevc0417/decoder/ihevcd_process_slice.c:962
    #3 0x814caba in ihevcd_parse_slice_data /dist/src/android/libhevc0417/decoder/ihevcd_parse_slice.c:3244
    #4 0x812ef23 in ihevcd_nal_unit /dist/src/android/libhevc0417/decoder/ihevcd_nal.c:405
    #5 0x812b449 in ihevcd_decode /dist/src/android/libhevc0417/decoder/ihevcd_decode.c:604
    #6 0x80d8523 in main /dist/src/android/libhevc0417/t1.c:2753
    #7 0xf7586af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #8 0x80d0aa4 in _start (/dist/src/android/libhevc_fuzz/coolbugs/6/t1a+0x80d0aa4)

2) second bug

$ ./t1a
Using test.cfg as configuration file 
0
95
Ittiam Decoder Version number: @(#)Id:HEVCDEC_production Ver:05.00 Released by ITTIAM Build: Apr 27 2017 @ 11:06:08
7393
2603
1656
6279
4644
4012
1465
5007
=================================================================
==7813==ERROR: AddressSanitizer: stack-buffer-overflow on address 0xfff65db4 at pc 0x80e44a7 bp 0xfff65d38 sp 0xfff65d30
READ of size 4 at 0xfff65db4 thread T0
    #0 0x80e44a6 in ihevc_intra_pred_chroma_ref_substitution /dist/src/android/libhevc0417/common/ihevc_chroma_intra_pred_filters.c:239
    #1 0x8172ab0 in ihevcd_iquant_itrans_recon_ctb /dist/src/android/libhevc0417/decoder/ihevcd_iquant_itrans_recon_ctb.c:1046
    #2 0x815b3a3 in ihevcd_process /dist/src/android/libhevc0417/decoder/ihevcd_process_slice.c:962
    #3 0x814caba in ihevcd_parse_slice_data /dist/src/android/libhevc0417/decoder/ihevcd_parse_slice.c:3244
    #4 0x812ef23 in ihevcd_nal_unit /dist/src/android/libhevc0417/decoder/ihevcd_nal.c:405
    #5 0x812b449 in ihevcd_decode /dist/src/android/libhevc0417/decoder/ihevcd_decode.c:604
    #6 0x80d8523 in main /dist/src/android/libhevc0417/t1.c:2753
    #7 0xf74bdaf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #8 0x80d0aa4 in _start (/dist/src/android/libhevc_fuzz/coolbugs/6/t1a+0x80d0aa4)

Address 0xfff65db4 is located in stack of thread T0 at offset 52 in frame
    #0 0x80e379f in ihevc_intra_pred_chroma_ref_substitution /dist/src/android/libhevc0417/common/ihevc_chroma_intra_pred_filters.c:143

  This frame has 1 object(s):
    [32, 52) 'a_nbr_flag' <== Memory access at offset 52 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism or swapcontext
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow /dist/src/android/libhevc0417/common/ihevc_chroma_intra_pred_filters.c:239 ihevc_intra_pred_chroma_ref_substitution
Shadow bytes around the buggy address:
  0x3ffecb60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ffecb70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ffecb80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ffecb90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ffecba0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x3ffecbb0: f1 f1 f1 f1 00 00[04]f4 f3 f3 f3 f3 00 00 00 00
  0x3ffecbc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ffecbd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ffecbe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ffecbf0: 00 00 00 00 00 00 00 00 f1 f1 f1 f1 00 00 00 00
  0x3ffecc00: 00 00 00 00 00 f4 f4 f4 f2 f2 f2 f2 04 f4 f4 f4
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
==7813==ABORTING

