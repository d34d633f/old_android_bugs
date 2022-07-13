Android libhevc overflow 

How to reproduce:
1) upload test.mp4 to device and use stagefright binary to scan it

$ stagefright -s test.mp4

adb logcat output:


02-03 13:05:40.572 28556 12681 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
02-03 13:05:40.573 28556 12681 F DEBUG   : Build fingerprint: 'google/bullhead/bullhead:8.0.0/OPR4.170623.009/4302492:user/release-keys'
02-03 13:05:40.573 28556 12681 F DEBUG   : Revision: 'rev_1.0'
02-03 13:05:40.573 28556 12681 F DEBUG   : ABI: 'arm'
02-03 13:05:40.573 28556 12681 F DEBUG   : pid: 28556, tid: 12681, name: media.codec  >>> android.hardwar <<<
02-03 13:05:40.573 28556 12681 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x20002000
02-03 13:05:40.578 28556 12681 F DEBUG   :     r0 00002000  r1 00000000  r2 20002000  r3 00000003
02-03 13:05:40.578 28556 12681 F DEBUG   :     r4 00002000  r5 00000006  r6 ef203000  r7 00000006
02-03 13:05:40.578 28556 12681 F DEBUG   :     r8 0000000f  r9 0000000f  sl 000cff00  fp 000001a4
02-03 13:05:40.578 28556 12681 F DEBUG   :     ip 00000000  sp ee588648  lr 0000000f  pc f012f468  cpsr 200f0010
02-03 13:05:40.579 28556 12681 F DEBUG   : 
02-03 13:05:40.579 28556 12681 F DEBUG   : backtrace:
02-03 13:05:40.579 28556 12681 F DEBUG   :     #00 pc 00026468  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_inter_pred_ctb+740)
02-03 13:05:40.579 28556 12681 F DEBUG   :     #01 pc 0001c004  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_process+1188)
02-03 13:05:40.579 28556 12681 F DEBUG   :     #02 pc 0001d450  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_process_thread+148)
02-03 13:05:40.579 28556 12681 F DEBUG   :     #03 pc 00047c3f  /system/lib/libc.so (_ZL15__pthread_startPv+22)
02-03 13:05:40.580 28556 12681 F DEBUG   :     #04 pc 0001af5d  /system/lib/libc.so (__start_thread+32)
02-03 13:05:40.582   627   627 E /system/bin/tombstoned: Tombstone written to: /data/tombstones//tombstone_09
--------- beginning of system
02-03 13:05:40.583   770   791 I BootReceiver: Copying /data/tombstones/tombstone_09 to DropBox (SYSTEM_TOMBSTONE)
02-03 13:05:40.627   355   355 I ServiceManager: service 'media.codec' died
02-03 13:05:40.627 12669 12674 E ACodec  : OMX/mediaserver died, signalling error!
02-03 13:05:40.627 12669 12674 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
02-03 13:05:40.627 12669 12673 E MediaCodec: Codec reported err 0xffffffe0, actionCode 0, while in state 6
