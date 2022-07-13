Android libavc heap corrupion bug

How to reproduce:
1) checkout libavc
2) compile standalone decoder from libavc/test/decoder/main.c
3) run: ./dec -i 1.bin

gdb backtrace:
(gdb) bt
#0  0x0806fde5 in ih264d_compute_bs_non_mbaff (ps_dec=0x8151480, ps_cur_mb_info=0x81d4e00, u2_mbxn_mb=0)
    at ih264d_compute_bs.c:1269
#1  0x0807f2c5 in ih264d_mv_pred_ref_tfr_nby2_pmb (ps_dec=0x8151480, u1_mb_idx=0 '\000', u1_num_mbs=11 '\v')
    at ih264d_process_pslice.c:321
#2  0x0805d328 in ih264d_mark_err_slice_skip (ps_dec=0x8151480, num_mb_skip=99, u1_is_idr_slice=0 '\000', 
    u2_frame_num=10, ps_cur_poc=0xfffe9bac, prev_slice_err=2) at ih264d_parse_pslice.c:1814
#3  0x0804fe1c in ih264d_video_decode (dec_hdl=0x8151400, pv_api_ip=0xfffe9f8c, pv_api_op=0xfffe9d78)
    at ih264d_api.c:2139
#4  0x08051d7c in ih264d_api_function (dec_hdl=0x8151400, pv_api_ip=0xfffe9f8c, pv_api_op=0xfffe9d78)
    at ih264d_api.c:3567
#5  0x0804bd57 in main (argc=3, argv=0xffffd044) at t1.c:2852

