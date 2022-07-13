Android libhevc heap overflow

How to reproduce:
1) checkout libhevc
2) compile standalone decoder test/decoder/main.c 
3) run decoder using supplied test.cfg

gdb trace:

Program received signal SIGSEGV, Segmentation fault.
0x08052e65 in ihevc_recon_4x4_ttype1 (pi2_src=0xf7af1880, pu1_pred=0xf7af3480 "", pu1_dst=0xf7903ad1 "", 
    src_strd=-141542703, pred_strd=32, dst_strd=576, zero_cols=576) at common/ihevc_recon.c:124
124	                                CLIP_U8(pi2_src[j * src_strd] + pu1_pred[j * pred_strd]);
(gdb) x/10i $pc
=> 0x8052e65 <ihevc_recon_4x4_ttype1+94>:	movswl (%ebx),%edi
   0x8052e68 <ihevc_recon_4x4_ttype1+97>:	movzbl (%ecx),%esi
   0x8052e6b <ihevc_recon_4x4_ttype1+100>:	add    %edi,%esi
   0x8052e6d <ihevc_recon_4x4_ttype1+102>:	mov    $0xffffffff,%edi
   0x8052e72 <ihevc_recon_4x4_ttype1+107>:	cmp    $0xff,%esi
   0x8052e78 <ihevc_recon_4x4_ttype1+113>:	jg     0x8052e84 <ihevc_recon_4x4_ttype1+125>
   0x8052e7a <ihevc_recon_4x4_ttype1+115>:	test   %esi,%esi
   0x8052e7c <ihevc_recon_4x4_ttype1+117>:	mov    $0x0,%edi
   0x8052e81 <ihevc_recon_4x4_ttype1+122>:	cmovns %esi,%edi
   0x8052e84 <ihevc_recon_4x4_ttype1+125>:	mov    %edi,%eax
(gdb) i r ebx
ebx            0xe6cf8e22	-422605278
(gdb) bt
#0  0x08052e65 in ihevc_recon_4x4_ttype1 (pi2_src=0xf7af1880, pu1_pred=0xf7af3480 "", pu1_dst=0xf7903ad1 "", 
    src_strd=-141542703, pred_strd=32, dst_strd=576, zero_cols=576) at common/ihevc_recon.c:124
#1  0x08076aee in ihevcd_iquant_itrans_recon_ctb (ps_proc=0x84768476) at decoder/ihevcd_iquant_itrans_recon_ctb.c:1111
#2  0x85768776 in ?? ()
#3  0x84768476 in ?? ()
#4  0x84778477 in ?? ()
#5  0x83778477 in ?? ()
#6  0x83778377 in ?? ()
#7  0x83778377 in ?? ()
#8  0x83778377 in ?? ()
#9  0x81798377 in ?? ()
#10 0x82798179 in ?? ()
#11 0x82798279 in ?? ()
#12 0x83798279 in ?? ()
#13 0x837b837a in ?? ()
#14 0x837b837b in ?? ()
#15 0x827a827b in ?? ()
#16 0x8079817a in ?? ()
#17 0x7f797f79 in ?? ()
#18 0x7e797e79 in ?? ()
#19 0x6f7a7d7a in ?? ()
#20 0x6e7a6f7a in ?? ()
#21 0x7c796e7a in ?? ()
#22 0x7c797c79 in ?? ()
#23 0x7c797c79 in ?? ()
#24 0x7c797c79 in ?? ()
#25 0x00007c79 in ?? ()
#26 0xf79ad02c in ?? ()
Backtrace stopped: previous frame inner to this frame (corrupt stack?)


