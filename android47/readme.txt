Android libhevc overflow.

How to reproduce:
1) checkout libhevc
2) compile standalone decoder test/decoder/main.c with ASAN 
3) run decoder using supplied test.cfg

gdb trace:

Program received signal SIGSEGV, Segmentation fault.
0x080786e9 in ihevcd_deblk_ctb (ps_deblk=ps_deblk@entry=0x80d5bb0, i4_is_last_ctb_x=i4_is_last_ctb_x@entry=0, 
    i4_is_last_ctb_y=i4_is_last_ctb_y@entry=0) at decoder/ihevcd_deblk.c:279
279	                    i1_beta_offset_div2 = ps_slice_hdr_top->i1_beta_offset_div2;
(gdb) x/10i $pc
=> 0x80786e9 <ihevcd_deblk_ctb+1273>:	movzbl 0xac(%eax),%edx
   0x80786f0 <ihevcd_deblk_ctb+1280>:	movzbl 0xad(%eax),%eax
   0x80786f7 <ihevcd_deblk_ctb+1287>:	mov    %al,-0x44(%ebp)
   0x80786fa <ihevcd_deblk_ctb+1290>:	cmpl   $0x0,-0x50(%ebp)
   0x80786fe <ihevcd_deblk_ctb+1294>:	jne    0x8078729 <ihevcd_deblk_ctb+1337>
   0x8078700 <ihevcd_deblk_ctb+1296>:	cmpl   $0x0,-0x84(%ebp)
   0x8078707 <ihevcd_deblk_ctb+1303>:	je     0x8078717 <ihevcd_deblk_ctb+1319>
   0x8078709 <ihevcd_deblk_ctb+1305>:	mov    -0xbc(%ebp),%eax
   0x807870f <ihevcd_deblk_ctb+1311>:	movzbl (%eax),%eax
   0x8078712 <ihevcd_deblk_ctb+1314>:	mov    %eax,-0x64(%ebp)
(gdb) i r eax
eax            0xf7f95230	-134655440
(gdb) 

