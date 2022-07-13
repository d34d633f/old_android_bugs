Android libmpeg2 stack overflow 

Tested on android-7.1.2_r18 branch.

How to reproduce:
1) checkout libmpeg2
2) compile standalone decoder test/decoder/main.c with ASAN

$ cd external/libmpeg2

edit impeg2d_dec_hdr.c, comment out inclusion of cutils/log.h and invocations of android_errorWriteLog.

$ cp test/decoder/main.c t1.c
$ clang -o t1a -m32 -g -fsanitize=address  -fno-omit-frame-pointer -O1 t1.c common/impeg2_buf_mgr.c common/impeg2_disp_mgr.c common/impeg2_format_conv.c common/impeg2_globals.c common/impeg2_idct.c common/impeg2_inter_pred.c common/impeg2_job_queue.c common/impeg2_mem_func.c common/ithread.c decoder/impeg2d_api_main.c decoder/impeg2d_bitstream.c decoder/impeg2d_debug.c decoder/impeg2d_dec_hdr.c decoder/impeg2d_decoder.c decoder/impeg2d_d_pic.c decoder/impeg2d_function_selector_generic.c decoder/impeg2d_globals.c decoder/impeg2d_i_pic.c decoder/impeg2d_mc.c decoder/impeg2d_mv_dec.c decoder/impeg2d_pic_proc.c decoder/impeg2d_pnb_pic.c decoder/impeg2d_vld.c decoder/impeg2d_vld_tables.c decoder/impeg2d_deinterlace.c common/icv_sad.c common/icv_variance.c common/ideint.c common/ideint_cac.c common/ideint_debug.c common/ideint_function_selector_generic.c common/ideint_utils.c  decoder/x86/impeg2d_function_selector.c decoder/x86/impeg2d_function_selector_avx2.c decoder/x86/impeg2d_function_selector_ssse3.c decoder/x86/impeg2d_function_selector_sse42.c common/x86/ideint_function_selector.c common/x86/ideint_function_selector_ssse3.c common/x86/ideint_function_selector_sse42.c common/x86/icv_variance_ssse3.c common/x86/icv_sad_ssse3.c common/x86/ideint_cac_ssse3.c common/x86/ideint_spatial_filter_ssse3.c common/x86/impeg2_idct_recon_sse42_intr.c common/x86/impeg2_inter_pred_sse42_intr.c common/x86/impeg2_mem_func_sse42_intr.c -D_LIB -DMULTICORE -fPIC -DPROFILE_ENABLE -DMD5_DISABLE  -DX86 -DDISABLE_AVX2 -m32 -msse4.2 -mno-avx -DDEFAULT_ARCH=D_ARCH_X86_SSE42 -I./common -I./decoder -I./common/x86 -I./decoder/x86


3) run decoder using supplied test.cfg

Code snip from impeg2d_vlc.c:
<code>
  			   u4_pos                 = pu1_scan[u4_numCoeffs++ & 63];
                            pu1_pos[*pi4_num_coeffs]    = u4_pos;
                            if (1 == lead_zeros)
                                u4_sym_len--;
                            /* flushing */
                            FLUSH_BITS(u4_offset,u4_buf,u4_buf_nxt,u4_sym_len,pu4_buf_aligned)
                            pi2_outAddr[*pi4_num_coeffs]    = u4_level;

                            (*pi4_num_coeffs)++;
</code>

Size of pu1_pos and pi2_outAddr arrays is 64.
Max value of u4_numCoeffs is 64, same for *pi4_num_coeffs.
It will lead to off-by-one stack overflow.

ASAN log:
$./t1a
Using test.cfg as configuration file 
Ittiam Decoder Version number: @(#)Id:MPEG2VDEC_eval Ver:01.00 Released by ITTIAM Build: Jul 10 2017 @ 23:59:16
FrameNum:    1 TimeTaken(microsec):    104 AvgTime:    104 PeakAvgTimeMax:     13 Output:  0 NumBytes:   3015 
FrameNum:    2 TimeTaken(microsec):     78 AvgTime:     91 PeakAvgTimeMax:     22 Output:  0 NumBytes:   2122 
FrameNum:    3 TimeTaken(microsec):    551 AvgTime:    244 PeakAvgTimeMax:     91 Output:  1 NumBytes:   1310 
FrameNum:    4 TimeTaken(microsec):    106 AvgTime:    209 PeakAvgTimeMax:    104 Output:  1 NumBytes:   1599 
FrameNum:    5 TimeTaken(microsec):    107 AvgTime:    189 PeakAvgTimeMax:    118 Output:  1 NumBytes:   4391 
=================================================================
==25435==ERROR: AddressSanitizer: stack-buffer-overflow on address 0xff905f00 at pc 0x8109450 bp 0xff905ce8 sp 0xff905ce0
WRITE of size 1 at 0xff905f00 thread T0
    #0 0x810944f in impeg2d_vld_decode /dist/src/android/libmpeg2_0717/decoder/impeg2d_vld.c:877
    #1 0x8109b00 in impeg2d_vld_inv_quant_mpeg2 /dist/src/android/libmpeg2_0717/decoder/impeg2d_vld.c:386
    #2 0x8106210 in impeg2d_dec_p_b_slice /dist/src/android/libmpeg2_0717/decoder/impeg2d_pnb_pic.c:556
    #3 0x80ef6cf in impeg2d_dec_slice /dist/src/android/libmpeg2_0717/decoder/impeg2d_dec_hdr.c:845
    #4 0x80efc65 in impeg2d_dec_pic_data_thread /dist/src/android/libmpeg2_0717/decoder/impeg2d_dec_hdr.c:935
    #5 0x80f1910 in impeg2d_dec_pic_data /dist/src/android/libmpeg2_0717/decoder/impeg2d_dec_hdr.c:1362
    #6 0x80f49a2 in impeg2d_process_video_bit_stream /dist/src/android/libmpeg2_0717/decoder/impeg2d_dec_hdr.c:1722
    #7 0x80f56b2 in impeg2d_dec_frm /dist/src/android/libmpeg2_0717/decoder/impeg2d_decoder.c:207
    #8 0x80eb588 in impeg2d_api_entity /dist/src/android/libmpeg2_0717/decoder/impeg2d_api_main.c:3380
    #9 0x80d5df5 in main /dist/src/android/libmpeg2_0717/t1.c:2881
    #10 0xf74e5af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #11 0x80cd6c4 in _start (/sec/zdi/0417/mpeg1/t1a+0x80cd6c4)

Address 0xff905f00 is located in stack of thread T0 at offset 256 in frame
    #0 0x810997f in impeg2d_vld_inv_quant_mpeg2 /dist/src/android/libmpeg2_0717/decoder/impeg2d_vld.c:375

  This frame has 3 object(s):
    [32, 160) 'pi2_coeffs'
    [192, 256) 'pi4_pos' <== Memory access at offset 256 overflows this variable
    [288, 292) 'i4_num_coeffs'
HINT: this may be a false positive if your program uses some custom stack unwind mechanism or swapcontext
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow /dist/src/android/libmpeg2_0717/decoder/impeg2d_vld.c:877 impeg2d_vld_decode
Shadow bytes around the buggy address:
  0x3ff20b90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ff20ba0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ff20bb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ff20bc0: f1 f1 f1 f1 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ff20bd0: 00 00 00 00 f2 f2 f2 f2 00 00 00 00 00 00 00 00
=>0x3ff20be0:[f2]f2 f2 f2 04 f4 f4 f4 f3 f3 f3 f3 00 00 00 00
  0x3ff20bf0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ff20c00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ff20c10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ff20c20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x3ff20c30: f1 f1 f1 f1 00 04 f4 f4 f2 f2 f2 f2 00 04 f4 f4
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
==25435==ABORTING

