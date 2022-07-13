Android libavc memcpy bug

How to reproduce:
1) checkout libavc
2) compile standalone decoder from libavc/test/decoder/main.c
3) run: ./dec -i 1.bin

gdb backtrace:

Program received signal SIGSEGV, Segmentation fault.
__memcpy_ssse3_rep () at ../sysdeps/i386/i686/multiarch/memcpy-ssse3-rep.S:1092
1092	../sysdeps/i386/i686/multiarch/memcpy-ssse3-rep.S: No such file or directory.
(gdb) bt
#0  __memcpy_ssse3_rep () at ../sysdeps/i386/i686/multiarch/memcpy-ssse3-rep.S:1092
#1  0x08061324 in ih264d_mvpred_mbaff (ps_dec=0x8151480, ps_cur_mb_info=0x8210680, ps_mv_nmb=0xf7cb4a00, 
    ps_mv_ntop=0xf7cb2990, ps_mv_final_pred=0xfffe98b4, u1_sub_mb_num=0 '\000', uc_mb_part_width=4 '\004', 
    u1_lx_start=0 '\000', u1_lxend=1 '\001', u1_mb_mc_mode=255 '\377') at ih264d_mvpred.c:946
#2  0x0807ede2 in ih264d_mv_pred_ref_tfr_nby2_pmb (ps_dec=0x8151480, u1_mb_idx=0 '\000', u1_num_mbs=4 '\004')
    at ih264d_process_pslice.c:190
#3  0x0805d328 in ih264d_mark_err_slice_skip (ps_dec=0x8151480, num_mb_skip=12, u1_is_idr_slice=0 '\000', 
    u2_frame_num=9, ps_cur_poc=0xfffe9a7c, prev_slice_err=2) at ih264d_parse_pslice.c:1814
#4  0x08064072 in ih264d_parse_decode_slice (u1_is_idr_slice=0 '\000', u1_nal_ref_idc=0 '\000', ps_dec=0x8151480)
    at ih264d_parse_slice.c:1390
#5  0x0808a433 in ih264d_parse_nal_unit (dec_hdl=0x8151400, ps_dec_op=0xfffe9d88, pu1_buf=0xf7d11080 "\022", 
    u4_length=4735) at ih264d_parse_headers.c:1068
#6  0x0804fa2f in ih264d_video_decode (dec_hdl=0x8151400, pv_api_ip=0xfffe9f9c, pv_api_op=0xfffe9d88)
    at ih264d_api.c:2057
#7  0x08051d7c in ih264d_api_function (dec_hdl=0x8151400, pv_api_ip=0xfffe9f9c, pv_api_op=0xfffe9d88)
    at ih264d_api.c:3567
#8  0x0804bd57 in main (argc=3, argv=0xffffd054) at t1.c:2852


