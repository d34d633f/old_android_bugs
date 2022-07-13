Android libhevc bug

How to reproduce:
1) checkout libhevc
2) compile standalone decoder test/decoder/main.c
3) run decoder using supplied test.cfg

gdb backtrace:
Program received signal SIGSEGV, Segmentation fault.
0x0808e54b in ihevcd_ref_list (ps_codec=0x824e480, ps_pps=0x825ab80, ps_sps=0xf7cd3080, 
    ps_slice_hdr=0xf7c83080) at decoder/ihevcd_ref_list.c:508
508	                if(ps_mv_buf && ps_mv_buf->i4_abs_poc == ps_pic_buf->i4_abs_poc)
(gdb) x/10i $pc
=> 0x808e54b <ihevcd_ref_list+3718>:	mov    0x10(%eax),%edx
   0x808e54e <ihevcd_ref_list+3721>:	mov    -0x330(%ebp),%eax
   0x808e554 <ihevcd_ref_list+3727>:	mov    0x8(%eax),%eax
   0x808e557 <ihevcd_ref_list+3730>:	cmp    %eax,%edx
   0x808e559 <ihevcd_ref_list+3732>:	jne    0x808e583 <ihevcd_ref_list+3774>
   0x808e55b <ihevcd_ref_list+3734>:	mov    -0x39c(%ebp),%eax
   0x808e561 <ihevcd_ref_list+3740>:	mov    0xe0(%eax),%eax
   0x808e567 <ihevcd_ref_list+3746>:	movl   $0x2,0x8(%esp)
   0x808e56f <ihevcd_ref_list+3754>:	mov    -0x394(%ebp),%edx
   0x808e575 <ihevcd_ref_list+3760>:	mov    %edx,0x4(%esp)
(gdb) i r eax
eax            0xf7abc418	-139738088
(gdb) 

