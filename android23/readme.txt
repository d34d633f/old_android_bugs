Android libavc bug
Probably useless null ptr dereference.

How to reproduce:
1) checkout libavc
2) compile standalone decoder test/decoder/main.c
3) run decoder: ./dec -i 1.bin

gdb trace:
Program terminated with signal SIGSEGV, Segmentation fault.
#0  0x080816e2 in ih264d_update_default_index_list (ps_dpb_mgr=0x875d580) at ih264d_dpb_mgr.c:677
677	        ps_dpb_mgr->ps_def_dpb[i] = ps_next_dpb->ps_pic_buf;
(gdb) x/10i $pc
=> 0x80816e2 <ih264d_update_default_index_list+89>:	mov    (%eax),%ecx
   0x80816e4 <ih264d_update_default_index_list+91>:	mov    0x8(%ebp),%eax
   0x80816e7 <ih264d_update_default_index_list+94>:	mov    -0x8(%ebp),%edx
   0x80816ea <ih264d_update_default_index_list+97>:	mov    %ecx,(%eax,%edx,4)
   0x80816ed <ih264d_update_default_index_list+100>:	mov    -0x4(%ebp),%eax
   0x80816f0 <ih264d_update_default_index_list+103>:	mov    0xc(%eax),%eax
   0x80816f3 <ih264d_update_default_index_list+106>:	mov    %eax,-0x4(%ebp)
   0x80816f6 <ih264d_update_default_index_list+109>:	addl   $0x1,-0x8(%ebp)
   0x80816fa <ih264d_update_default_index_list+113>:	mov    0x8(%ebp),%eax
   0x80816fd <ih264d_update_default_index_list+116>:	movzbl 0x908(%eax),%eax
(gdb) i r eax
eax            0x0	0

