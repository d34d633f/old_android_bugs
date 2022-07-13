Android libhevc null ptr dereference.
Most probably it is absolutely useless.
Putting it here for reference.

How to reproduce:
1) checkout libhevc
2) compile standalone decoder test/decoder/main.c 
3) run decoder using supplied test.cfg

gdb trace:

ived signal SIGSEGV, Segmentation fault.
ihevcd_parse_slice_data (ps_codec=ps_codec@entry=0x80d5480) at decoder/ihevcd_parse_slice.c:2307
2307	            if(ref_list_poc > cur_poc)
(gdb) x/i $pc
=> 0x806aab3 <ihevcd_parse_slice_data+826>:	cmp    0x10(%edx),%eax
(gdb) i r dx
dx             0x0	0

