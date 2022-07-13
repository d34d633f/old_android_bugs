Android libhevc overflow

How to reproduce:
1) upload test.mp4 to device and use stagefright binary to scan it

$ stagefright -s test.mp4

adb logcat output:


beginning of crash
01-17 09:29:16.428 32033 10035 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-17 09:29:16.428 32033 10035 F DEBUG   : Build fingerprint: 'google/bullhead/bullhead:8.0.0/OPR4.170623.009/4302492:user/release-keys'
01-17 09:29:16.428 32033 10035 F DEBUG   : Revision: 'rev_1.0'
01-17 09:29:16.428 32033 10035 F DEBUG   : ABI: 'arm'
01-17 09:29:16.428 32033 10035 F DEBUG   : pid: 32033, tid: 10035, name: media.codec  >>> android.hardwar <<<
01-17 09:29:16.428 32033 10035 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x715cf44f
01-17 09:29:16.437 32033 10035 F DEBUG   :     r0 715cf44f  r1 f0202678  r2 0000012c  r3 f0c9c35c
01-17 09:29:16.437 32033 10035 F DEBUG   :     r4 f0703000  r5 f212c8e8  r6 f0703000  r7 f0d0bd10
01-17 09:29:16.437 32033 10035 F DEBUG   :     r8 f0d05fa0  r9 f0d05f80  sl f0202808  fp 00000000
01-17 09:29:16.438 32033 10035 F DEBUG   :     ip f0cf5fcc  sp f0202630  lr f0cac8b4  pc f17dc2f6  cpsr a00f0030
01-17 09:29:16.444 32033 10035 F DEBUG   : 
01-17 09:29:16.444 32033 10035 F DEBUG   : backtrace:
01-17 09:29:16.444 32033 10035 F DEBUG   :     #00 pc 000482f6  /system/lib/libc.so (pthread_mutex_lock+1)
01-17 09:29:16.444 32033 10035 F DEBUG   :     #01 pc 0001e8b0  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_jobq_deinit+12)
01-17 09:29:16.444 32033 10035 F DEBUG   :     #02 pc 0000b744  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_free_dynamic_bufs+28)
01-17 09:29:16.444 32033 10035 F DEBUG   :     #03 pc 0000b424  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_init+8)
01-17 09:29:16.444 32033 10035 F DEBUG   :     #04 pc 0000e494  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_ctl+380)
01-17 09:29:16.444 32033 10035 F DEBUG   :     #05 pc 0000a2d1  /system/lib/libstagefright_soft_hevcdec.so (_ZN7android8SoftHEVC12resetDecoderEv+40)
01-17 09:29:16.444 32033 10035 F DEBUG   :     #06 pc 0000a497  /system/lib/libstagefright_soft_hevcdec.so (_ZN7android8SoftHEVC7onResetEv+16)
01-17 09:29:16.444 32033 10035 F DEBUG   :     #07 pc 00039f53  /system/lib/libstagefright_omx.so (_ZN7android22SimpleSoftOMXComponent16checkTransitionsEv+182)
01-17 09:29:16.444 32033 10035 F DEBUG   :     #08 pc 0003a27f  /system/lib/libstagefright_omx.so (_ZN7android22SimpleSoftOMXComponent10freeBufferEjP20OMX_BUFFERHEADERTYPE+182)
01-17 09:29:16.444 32033 10035 F DEBUG   :     #09 pc 000359a9  /system/lib/libstagefright_omx.so (_ZN7android15OMXNodeInstance10freeBufferEjj+76)
01-17 09:29:16.444 32033 10035 F DEBUG   :     #10 pc 00074431  /system/lib/libmedia.so (_ZN7android9BnOMXNode10onTransactEjRKNS_6ParcelEPS1_j+548)
01-17 09:29:16.444 32033 10035 F DEBUG   :     #11 pc 000406ef  /system/lib/libbinder.so (_ZN7android7BBinder8transactEjRKNS_6ParcelEPS1_j+70)
01-17 09:29:16.444 32033 10035 F DEBUG   :     #12 pc 000483e5  /system/lib/libbinder.so (_ZN7android14IPCThreadState14executeCommandEi+584)
01-17 09:29:16.444 32033 10035 F DEBUG   :     #13 pc 0004809d  /system/lib/libbinder.so (_ZN7android14IPCThreadState20getAndExecuteCommandEv+112)
01-17 09:29:16.444 32033 10035 F DEBUG   :     #14 pc 0004859f  /system/lib/libbinder.so (_ZN7android14IPCThreadState14joinThreadPoolEb+38)
01-17 09:29:16.445 32033 10035 F DEBUG   :     #15 pc 0005eb25  /system/lib/libbinder.so
01-17 09:29:16.445 32033 10035 F DEBUG   :     #16 pc 0000d38d  /system/lib/libutils.so (_ZN7android6Thread11_threadLoopEPv+140)
01-17 09:29:16.445 32033 10035 F DEBUG   :     #17 pc 00047c3f  /system/lib/libc.so (_ZL15__pthread_startPv+22)
01-17 09:29:16.445 32033 10035 F DEBUG   :     #18 pc 0001af5d  /system/lib/libc.so (__start_thread+32)
01-17 09:29:16.452   598   598 E /system/bin/tombstoned: Tombstone written to: /data/tombstones//tombstone_06
--------- beginning of system
01-17 09:29:16.453   767   791 I BootReceiver: Copying /data/tombstones/tombstone_06 to DropBox (SYSTEM_TOMBSTONE)
01-17 09:29:16.466   355   355 I ServiceManager: service 'media.codec' died
01-17 09:29:16.466  6627  6632 E ACodec  : OMX/mediaserver died, signalling error!
