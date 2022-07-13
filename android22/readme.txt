
Android libavc bug

How to reproduce:
1) checkout libavc
2) compile standalone decoder test/decoder/main.c
3) run decoder: ./dec -i 1.bin

gdb backtrace:
Program terminated with signal SIGSEGV, Segmentation fault.
#0  0x08051fe1 in ih264d_form_mb_part_info_bp (ps_pred_pkd=0x4de00734, ps_dec=0x8937480, u2_mb_x=1, u2_mb_y=7, 
    mb_index=1, ps_cur_mb_info=0x89bae3c) at ih264d_inter_pred.c:216
216	     i1_size_pos_info = ps_pred_pkd->i1_size_pos_info;
(gdb) x/10i $pc
=> 0x8051fe1 <ih264d_form_mb_part_info_bp+94>:	movzbl 0x8(%eax),%eax
   0x8051fe5 <ih264d_form_mb_part_info_bp+98>:	mov    %al,-0x76(%ebp)
   0x8051fe8 <ih264d_form_mb_part_info_bp+101>:	movsbl -0x76(%ebp),%eax
   0x8051fec <ih264d_form_mb_part_info_bp+105>:	and    $0x3,%eax
   0x8051fef <ih264d_form_mb_part_info_bp+108>:	mov    %eax,-0x58(%ebp)
   0x8051ff2 <ih264d_form_mb_part_info_bp+111>:	mov    -0x58(%ebp),%eax
   0x8051ff5 <ih264d_form_mb_part_info_bp+114>:	mov    %al,-0x7a(%ebp)
   0x8051ff8 <ih264d_form_mb_part_info_bp+117>:	movzbl -0x76(%ebp),%eax
   0x8051ffc <ih264d_form_mb_part_info_bp+121>:	sar    $0x2,%al
   0x8051fff <ih264d_form_mb_part_info_bp+124>:	movsbl %al,%eax
(gdb) i r eax
eax            0x4de00734	1306527540
