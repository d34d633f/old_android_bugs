Android libhevc null ptr dereference

How to reproduce:
1) upload test.mp4 to device and use stagefright binary to scan it

$ stagefright -s test.mp4

adb logcat output:


--------- beginning of main
01-19 21:54:20.208   598   598 I /system/bin/tombstoned: received crash request for pid 5252
--------- beginning of crash
01-19 21:54:20.209  5252 14161 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-19 21:54:20.209  5252 14161 F DEBUG   : Build fingerprint: 'google/bullhead/bullhead:8.0.0/OPR4.170623.009/4302492:user/release-keys'
01-19 21:54:20.209  5252 14161 F DEBUG   : Revision: 'rev_1.0'
01-19 21:54:20.209  5252 14161 F DEBUG   : ABI: 'arm'
01-19 21:54:20.209  5252 14161 F DEBUG   : pid: 5252, tid: 14161, name: media.codec  >>> android.hardwar <<<
01-19 21:54:20.209  5252 14161 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0
01-19 21:54:20.210  5252 14161 F DEBUG   : Cause: null pointer dereference
01-19 21:54:20.215  5252 14161 F DEBUG   :     r0 00000000  r1 e64f2230  r2 ed905640  r3 00000024
01-19 21:54:20.215  5252 14161 F DEBUG   :     r4 00000005  r5 00000010  r6 00000008  r7 00000020
01-19 21:54:20.215  5252 14161 F DEBUG   :     r8 e5b214f8  r9 00000009  sl e5b21924  fp e5a33000
01-19 21:54:20.215  5252 14161 F DEBUG   :     ip e5b21928  sp ed9055a0  lr 00000004  pc ee9250e4  cpsr 800f0010
01-19 21:54:20.218  5252 14161 F DEBUG   : 
01-19 21:54:20.218  5252 14161 F DEBUG   : backtrace:
01-19 21:54:20.218  5252 14161 F DEBUG   :     #00 pc 000210e4  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_collocated_mvp+220)
01-19 21:54:20.218  5252 14161 F DEBUG   :     #01 pc 00021bc0  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_mv_merge+1896)
01-19 21:54:20.218  5252 14161 F DEBUG   :     #02 pc 0001fb70  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_get_mv_ctb+1512)
01-19 21:54:20.218  5252 14161 F DEBUG   :     #03 pc 0001bffc  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_process+1180)
01-19 21:54:20.218  5252 14161 F DEBUG   :     #04 pc 0001d450  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_process_thread+148)
01-19 21:54:20.218  5252 14161 F DEBUG   :     #05 pc 00047c3f  /system/lib/libc.so (_ZL15__pthread_startPv+22)
01-19 21:54:20.218  5252 14161 F DEBUG   :     #06 pc 0001af5d  /system/lib/libc.so (__start_thread+32)
01-19 21:54:20.222   598   598 E /system/bin/tombstoned: Tombstone written to: /data/tombstones//tombstone_01
--------- beginning of system
01-19 21:54:20.223   767   791 I BootReceiver: Copying /data/tombstones/tombstone_01 to DropBox (SYSTEM_TOMBSTONE)
01-19 21:54:20.241 14149 14153 E ACodec  : OMX/mediaserver died, signalling error!
01-19 21:54:20.241 14149 14153 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
01-19 21:54:20.241 14149 14152 E MediaCodec: Codec reported err 0xffffffe0, actionCode 0, while in state 6
01-19 21:54:20.241   355   355 I ServiceManager: service 'media.codec' died
