Android libhevc null ptr dereference 

How to reproduce:
1) checkout libhevc
2) compile standalone decoder test/decoder/main.c
3) run decoder using supplied test.cfg

gdb trace:

Program received signal SIGSEGV, Segmentation fault.
ihevcd_inter_pred_ctb (ps_proc=ps_proc@entry=0x80d5a34) at decoder/ihevcd_inter_pred.c:235
235	            ref_pic_luma_l0 = ps_pic_buf_l0->pu1_luma;
(gdb) x/10i $pc
=> 0x80798be <ihevcd_inter_pred_ctb+638>:	mov    (%ecx),%esi
   0x80798c0 <ihevcd_inter_pred_ctb+640>:	mov    %esi,-0x10c(%ebp)
   0x80798c6 <ihevcd_inter_pred_ctb+646>:	mov    0x4(%ecx),%ecx
   0x80798c9 <ihevcd_inter_pred_ctb+649>:	mov    %ecx,-0xbc(%ebp)
   0x80798cf <ihevcd_inter_pred_ctb+655>:	add    %edi,%edx
   0x80798d1 <ihevcd_inter_pred_ctb+657>:	movswl 0x124(%edx),%edi
   0x80798d8 <ihevcd_inter_pred_ctb+664>:	mov    %edi,-0x104(%ebp)
   0x80798de <ihevcd_inter_pred_ctb+670>:	movswl 0x164(%edx),%edi
   0x80798e5 <ihevcd_inter_pred_ctb+677>:	mov    %edi,-0xcc(%ebp)
   0x80798eb <ihevcd_inter_pred_ctb+683>:	movswl 0x1a4(%edx),%edi
(gdb) i r ecx
ecx            0x0	0
(gdb) 

