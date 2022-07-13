Android libhevc overflow

How to reproduce:
1) upload test.mp4 to device and use stagefright binary to scan it

$ stagefright -s test.mp4

adb logcat output:


01-16 06:31:49.665   598   598 I /system/bin/tombstoned: received crash request for pid 7202
--------- beginning of crash
01-16 06:31:49.666  7202  7800 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-16 06:31:49.666  7202  7800 F DEBUG   : Build fingerprint: 'google/bullhead/bullhead:8.0.0/OPR4.170623.009/4302492:user/release-keys'
01-16 06:31:49.666  7202  7800 F DEBUG   : Revision: 'rev_1.0'
01-16 06:31:49.667  7202  7800 F DEBUG   : ABI: 'arm'
01-16 06:31:49.667  7202  7800 F DEBUG   : pid: 7202, tid: 7800, name: media.codec  >>> android.hardwar <<<
01-16 06:31:49.667  7202  7800 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0xbddf1d67
01-16 06:31:49.672  7202  7800 F DEBUG   :     r0 bddf1d67  r1 e8796200  r2 00000001  r3 bddf1d23
01-16 06:31:49.673  7202  7800 F DEBUG   :     r4 e8796040  r5 0000000f  r6 00000029  r7 00000000
01-16 06:31:49.673  7202  7800 F DEBUG   :     r8 00000011  r9 00000004  sl 00000010  fp e8541490
01-16 06:31:49.673  7202  7800 F DEBUG   :     ip 00000040  sp e78856c0  lr e98fc0a8  pc e9da3884  cpsr 28070010
01-16 06:31:49.674  7202  7800 F DEBUG   : 
01-16 06:31:49.674  7202  7800 F DEBUG   : backtrace:
01-16 06:31:49.674  7202  7800 F DEBUG   :     #00 pc 0001f884  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_get_mv_ctb+764)
01-16 06:31:49.674  7202  7800 F DEBUG   :     #01 pc 0001bffc  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_process+1180)
01-16 06:31:49.674  7202  7800 F DEBUG   :     #02 pc 0001d450  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_process_thread+148)
01-16 06:31:49.675  7202  7800 F DEBUG   :     #03 pc 00047c3f  /system/lib/libc.so (_ZL15__pthread_startPv+22)
01-16 06:31:49.675  7202  7800 F DEBUG   :     #04 pc 0001af5d  /system/lib/libc.so (__start_thread+32)
01-16 06:31:49.677   598   598 E /system/bin/tombstoned: Tombstone written to: /data/tombstones//tombstone_03
--------- beginning of system
01-16 06:31:49.678   767   791 I BootReceiver: Copying /data/tombstones/tombstone_03 to DropBox (SYSTEM_TOMBSTONE)
01-16 06:31:49.688   355   355 I ServiceManager: service 'media.codec' died
01-16 06:31:49.688  7681  7685 E ACodec  : OMX/mediaserver died, signalling error!
01-16 06:31:49.688  7681  7685 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
01-16 06:31:49.688  7681  7684 E MediaCodec: Codec reported err 0xffffffe0, actionCode 0, while in state 6
