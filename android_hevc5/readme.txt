Android libhevc overflow

How to reproduce:
1) upload test.mp4 to device and use stagefright binary to scan it

$ stagefright -s test.mp4

adb logcat output:


--------- beginning of main
01-16 05:56:53.166   598   598 I /system/bin/tombstoned: received crash request for pid 6821
--------- beginning of crash
01-16 05:56:53.168  6821  6979 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-16 05:56:53.168  6821  6979 F DEBUG   : Build fingerprint: 'google/bullhead/bullhead:8.0.0/OPR4.170623.009/4302492:user/release-keys'
01-16 05:56:53.168  6821  6979 F DEBUG   : Revision: 'rev_1.0'
01-16 05:56:53.168  6821  6979 F DEBUG   : ABI: 'arm'
01-16 05:56:53.168  6821  6979 F DEBUG   : pid: 6821, tid: 6979, name: media.codec  >>> android.hardwar <<<
01-16 05:56:53.168  6821  6979 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x8dcefed0
01-16 05:56:53.173  6821  6979 F DEBUG   :     r0 00000000  r1 00000000  r2 000007c0  r3 8dcefed0
01-16 05:56:53.173  6821  6979 F DEBUG   :     r4 00000008  r5 e5f0fdca  r6 8dcefed0  r7 00000004
01-16 05:56:53.173  6821  6979 F DEBUG   :     r8 e527f6dc  r9 00000003  sl 00000000  fp e5f0fdc8
01-16 05:56:53.173  6821  6979 F DEBUG   :     ip 00000000  sp e527f55c  lr e75b70f0  pc e8b7af10  cpsr 28070010
01-16 05:56:53.174  6821  6979 F DEBUG   : 
01-16 05:56:53.174  6821  6979 F DEBUG   : backtrace:
01-16 05:56:53.174  6821  6979 F DEBUG   :     #00 pc 00018f10  /system/lib/libc.so (memset+48)
01-16 05:56:53.175  6821  6979 F DEBUG   :     #01 pc 000220ec  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_unpack_coeffs+192)
01-16 05:56:53.175  6821  6979 F DEBUG   :     #02 pc 00023238  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_iquant_itrans_recon_ctb+2384)
01-16 05:56:53.175  6821  6979 F DEBUG   :     #03 pc 0001c650  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_process+2800)
01-16 05:56:53.175  6821  6979 F DEBUG   :     #04 pc 0001d450  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_process_thread+148)
01-16 05:56:53.175  6821  6979 F DEBUG   :     #05 pc 00047c3f  /system/lib/libc.so (_ZL15__pthread_startPv+22)
01-16 05:56:53.175  6821  6979 F DEBUG   :     #06 pc 0001af5d  /system/lib/libc.so (__start_thread+32)
01-16 05:56:53.177   598   598 E /system/bin/tombstoned: Tombstone written to: /data/tombstones//tombstone_01
--------- beginning of system
01-16 05:56:53.179   767   791 I BootReceiver: Copying /data/tombstones/tombstone_01 to DropBox (SYSTEM_TOMBSTONE)
01-16 05:56:53.187  6868  6872 E ACodec  : OMX/mediaserver died, signalling error!
01-16 05:56:53.187  6868  6872 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
01-16 05:56:53.187   355   355 I ServiceManager: service 'media.codec' died
