Android libhevc overflow

How to reproduce:
1) upload test.mp4 to device and use stagefright binary to scan it

$ stagefright -s test.mp4

adb logcat output:


beginning of crash
01-31 11:22:39.421  4171 18233 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-31 11:22:39.421  4171 18233 F DEBUG   : Build fingerprint: 'google/bullhead/bullhead:8.0.0/OPR4.170623.009/4302492:user/release-keys'
01-31 11:22:39.421  4171 18233 F DEBUG   : Revision: 'rev_1.0'
01-31 11:22:39.421  4171 18233 F DEBUG   : ABI: 'arm'
01-31 11:22:39.421  4171 18233 F DEBUG   : pid: 4171, tid: 18233, name: media.codec  >>> android.hardwar <<<
01-31 11:22:39.421  4171 18233 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x212ce611
01-31 11:22:39.430  4171 18233 F DEBUG   :     r0 00000400  r1 00000007  r2 0000c73d  r3 212c1ed4
01-31 11:22:39.430  4171 18233 F DEBUG   :     r4 0000212c  r5 e989df60  r6 00000000  r7 e9983000
01-31 11:22:39.430  4171 18233 F DEBUG   :     r8 e9837fe6  r9 00000001  sl 00000004  fp e989c000
01-31 11:22:39.430  4171 18233 F DEBUG   :     ip 00000001  sp f0b853c0  lr f0ba14b0  pc f0ba1500  cpsr 880f0010
01-31 11:22:39.436  4171 18233 F DEBUG   : 
01-31 11:22:39.436  4171 18233 F DEBUG   : backtrace:
01-31 11:22:39.436  4171 18233 F DEBUG   :     #00 pc 0001b500  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_proc_map_check+160)
01-31 11:22:39.436  4171 18233 F DEBUG   :     #01 pc 0001c528  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_process+2504)
01-31 11:22:39.436  4171 18233 F DEBUG   :     #02 pc 0000f3e0  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_decode+1860)
01-31 11:22:39.436  4171 18233 F DEBUG   :     #03 pc 0000a789  /system/lib/libstagefright_soft_hevcdec.so (_ZN7android8SoftHEVC13onQueueFilledEj+240)
01-31 11:22:39.436  4171 18233 F DEBUG   :     #04 pc 0003a595  /system/lib/libstagefright_omx.so (_ZN7android22SimpleSoftOMXComponent17onMessageReceivedERKNS_2spINS_8AMessageEEE+256)
01-31 11:22:39.437  4171 18233 F DEBUG   :     #05 pc 0003b5cd  /system/lib/libstagefright_omx.so
01-31 11:22:39.437  4171 18233 F DEBUG   :     #06 pc 0000fb99  /system/lib/libstagefright_foundation.so (_ZN7android8AHandler14deliverMessageERKNS_2spINS_8AMessageEEE+24)
01-31 11:22:39.437  4171 18233 F DEBUG   :     #07 pc 00011ff1  /system/lib/libstagefright_foundation.so (_ZN7android8AMessage7deliverEv+60)
01-31 11:22:39.437  4171 18233 F DEBUG   :     #08 pc 00010815  /system/lib/libstagefright_foundation.so (_ZN7android7ALooper4loopEv+484)
01-31 11:22:39.437  4171 18233 F DEBUG   :     #09 pc 0000d40f  /system/lib/libutils.so (_ZN7android6Thread11_threadLoopEPv+270)
01-31 11:22:39.437  4171 18233 F DEBUG   :     #10 pc 00047c3f  /system/lib/libc.so (_ZL15__pthread_startPv+22)
01-31 11:22:39.437  4171 18233 F DEBUG   :     #11 pc 0001af5d  /system/lib/libc.so (__start_thread+32)
01-31 11:22:39.443   627   627 E /system/bin/tombstoned: Tombstone written to: /data/tombstones//tombstone_07
--------- beginning of system
01-31 11:22:39.443   770   791 I BootReceiver: Copying /data/tombstones/tombstone_07 to DropBox (SYSTEM_TOMBSTONE)
01-31 11:22:39.474   355   355 I ServiceManager: service 'media.codec' died
01-31 11:22:39.474 18227 18232 E ACodec  : OMX/mediaserver died, signalling error!
01-31 11:22:39.474 18227 18232 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
