Android libavc heap corrupion bug

How to reproduce:
1) checkout libavc
2) compile standalone decoder from libavc/test/decoder/main.c
3) run: ./dec -i 1.bin

gdb backtrace:
(gdb) bt
#0  0x0806f0ae in ih264d_fill_bs1_16x16mb_bslice (ps_cur_mv_pred=0x8206640, ps_top_mv_pred=0x82055c0, 
    ppv_map_ref_idx_to_poc=0x8167f88, pu4_bs_table=0x81d30b8, ps_leftmost_mv_pred=0x82c6424, 
    ps_left_addr=0x817f420, u4_pic_addrress=0x81d1bb4, i4_ver_mvlimit=4) at ih264d_compute_bs.c:642
#1  0x08070adc in ih264d_compute_bs_mbaff (ps_dec=0x8151480, ps_cur_mb_info=0x81d37bc, u2_mbxn_mb=0)
    at ih264d_compute_bs.c:1711
#2  0x0807f2c5 in ih264d_mv_pred_ref_tfr_nby2_pmb (ps_dec=0x8151480, u1_mb_idx=0 '\000', 
    u1_num_mbs=4 '\004') at ih264d_process_pslice.c:321
#3  0x0805d328 in ih264d_mark_err_slice_skip (ps_dec=0x8151480, num_mb_skip=24, u1_is_idr_slice=0 '\000', 
    u2_frame_num=7, ps_cur_poc=0xfffe9a6c, prev_slice_err=2) at ih264d_parse_pslice.c:1814
#4  0x08064072 in ih264d_parse_decode_slice (u1_is_idr_slice=0 '\000', u1_nal_ref_idc=0 '\000', 
    ps_dec=0x8151480) at ih264d_parse_slice.c:1390
#5  0x0808a433 in ih264d_parse_nal_unit (dec_hdl=0x8151400, ps_dec_op=0xfffe9d78, pu1_buf=0xf7d16080 "8", 
    u4_length=9516) at ih264d_parse_headers.c:1068
#6  0x0804fa2f in ih264d_video_decode (dec_hdl=0x8151400, pv_api_ip=0xfffe9f8c, pv_api_op=0xfffe9d78)
    at ih264d_api.c:2057
#7  0x08051d7c in ih264d_api_function (dec_hdl=0x8151400, pv_api_ip=0xfffe9f8c, pv_api_op=0xfffe9d78)
    at ih264d_api.c:3567
#8  0x0804bd57 in main (argc=3, argv=0xffffd044) at t1.c:2852

