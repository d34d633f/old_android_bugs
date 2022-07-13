Android libavc bug.
Most probably it is useless null ptr dereference. 

How to reproduce:
1) checkout libavc
2) compile standalone decoder from libavc/test/decoder/main.c
3) run: ./dec -i 1.bin

gdb backtrace:
Program received signal SIGSEGV, Segmentation fault.
0x0806cd37 in ih264d_init_ref_idx_lx_b (ps_dec=0x8151480) at ih264d_process_bslice.c:1474
1474	                if(ps_next_dpb->u1_lt_idx == u1_lt_index)
(gdb) bt
#0  0x0806cd37 in ih264d_init_ref_idx_lx_b (ps_dec=0x8151480) at ih264d_process_bslice.c:1474
#1  0x08074a04 in ih264d_parse_bslice (ps_dec=0x8151480, u2_first_mb_in_slice=0)
    at ih264d_parse_bslice.c:1420
#2  0x08065019 in ih264d_parse_decode_slice (u1_is_idr_slice=0 '\000', u1_nal_ref_idc=0 '\000', 
    ps_dec=0x8151480) at ih264d_parse_slice.c:1893
#3  0x0808a433 in ih264d_parse_nal_unit (dec_hdl=0x8151400, ps_dec_op=0xfffe9d78, pu1_buf=0xf7d16080 " ", 
    u4_length=9790) at ih264d_parse_headers.c:1068
#4  0x0804fa2f in ih264d_video_decode (dec_hdl=0x8151400, pv_api_ip=0xfffe9f8c, pv_api_op=0xfffe9d78)
    at ih264d_api.c:2057
#5  0x08051d7c in ih264d_api_function (dec_hdl=0x8151400, pv_api_ip=0xfffe9f8c, pv_api_op=0xfffe9d78)
    at ih264d_api.c:3567
#6  0x0804bd57 in main (argc=3, argv=0xffffd044) at t1.c:2852

