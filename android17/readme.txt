Android libhevc out of bound read.

How to reproduce:
1) checkout libhevc
2) compile standalone decoder test/decoder/main.c with ASAN
3) run decoder using supplied test.cfg


ASAN trace:
==1240==ERROR: AddressSanitizer: stack-buffer-overflow on address 0xffa289a0 at pc 0x81ce176 bp 0xffa284a8 sp 0xffa284a0
READ of size 8 at 0xffa289a0 thread T0
    #0 0x81ce175 in ihevc_sao_band_offset_chroma_ssse3 /android/libhevc1410/common/x86/ihevc_sao_ssse3_intr.c:470
    #1 0x818d3f0 in ihevcd_sao_shift_ctb /android/libhevc1410/decoder/ihevcd_sao.c:3037
    #2 0x815bbf9 in ihevcd_process /android/libhevc1410/decoder/ihevcd_process_slice.c:1144
    #3 0x814c1ca in ihevcd_parse_slice_data /android/libhevc1410/decoder/ihevcd_parse_slice.c:3234
    #4 0x812e713 in ihevcd_nal_unit /android/libhevc1410/decoder/ihevcd_nal.c:405
    #5 0x812ac79 in ihevcd_decode /android/libhevc1410/decoder/ihevcd_decode.c:604
    #6 0x80d843b in main /android/libhevc1410/t1.c:2759
    #7 0xf757aaf2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #8 0x80d0a64 in _start (/android/libhevc_fuzz/debug/t1a+0x80d0a64)

Address 0xffa289a0 is located in stack of thread T0 at offset 544 in frame
    #0 0x817e77f in ihevcd_sao_shift_ctb /android/libhevc1410/decoder/ihevcd_sao.c:527


