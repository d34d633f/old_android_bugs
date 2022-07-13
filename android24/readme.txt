Android libavc heap corruption bug

How to reproduce:
1) checkout libavc
2) compile standalone decoder test/decoder/main.c
3) run decoder: ./dec -i 1.bin

gdb trace:
Program terminated with signal SIGSEGV, Segmentation fault.
#0  0x0806fbf9 in ih264d_compute_bs_non_mbaff (ps_dec=0x9dd5480, ps_cur_mb_info=0x9e208f8, 
    u2_mbxn_mb=2) at ih264d_compute_bs.c:1214
1214	            ppv_top_mv_pred_addr[0] = apv_map_ref_idx_to_poc[p1_refTop0[0]];
(gdb) bt
#0  0x0806fbf9 in ih264d_compute_bs_non_mbaff (ps_dec=0x9dd5480, ps_cur_mb_info=0x9e208f8, 
    u2_mbxn_mb=2) at ih264d_compute_bs.c:1214
#1  0x0807f2c5 in ih264d_mv_pred_ref_tfr_nby2_pmb (ps_dec=0x9dd5480, u1_mb_idx=0 '\000', 
    u1_num_mbs=45 '-') at ih264d_process_pslice.c:321
#2  0x0805d328 in ih264d_mark_err_slice_skip (ps_dec=0x9dd5480, num_mb_skip=1350, 
    u1_is_idr_slice=0 '\000', u2_frame_num=6, ps_cur_poc=0xffc72fec, prev_slice_err=2)
    at ih264d_parse_pslice.c:1814
#3  0x0804fe1c in ih264d_video_decode (dec_hdl=0x9dd5400, pv_api_ip=0xffc733cc, 
    pv_api_op=0xffc731b8) at ih264d_api.c:2139
#4  0x08051d7c in ih264d_api_function (dec_hdl=0x9dd5400, pv_api_ip=0xffc733cc, 
    pv_api_op=0xffc731b8) at ih264d_api.c:3567
#5  0x0804bd57 in main (argc=3, argv=0xffc86484) at t1.c:2852
(gdb) x/10i $pc
=> 0x806fbf9 <ih264d_compute_bs_non_mbaff+396>:	mov    %edx,(%eax)
   0x806fbfb <ih264d_compute_bs_non_mbaff+398>:	mov    -0x48(%ebp),%eax
   0x806fbfe <ih264d_compute_bs_non_mbaff+401>:	lea    0x4(%eax),%edx
   0x806fc01 <ih264d_compute_bs_non_mbaff+404>:	mov    -0x44(%ebp),%eax
   0x806fc04 <ih264d_compute_bs_non_mbaff+407>:	add    $0x1,%eax
   0x806fc07 <ih264d_compute_bs_non_mbaff+410>:	movzbl (%eax),%eax
   0x806fc0a <ih264d_compute_bs_non_mbaff+413>:	movsbl %al,%eax
   0x806fc0d <ih264d_compute_bs_non_mbaff+416>:	lea    0x0(,%eax,4),%ecx
   0x806fc14 <ih264d_compute_bs_non_mbaff+423>:	mov    -0x4c(%ebp),%eax
   0x806fc17 <ih264d_compute_bs_non_mbaff+426>:	add    %ecx,%eax
(gdb) i r eax edx
eax            0x11c00	72704
edx            0xf60dd420	-166865888

