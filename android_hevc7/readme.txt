Android libhevc overflow

How to reproduce:
1) upload test.mp4 to device and use stagefright binary to scan it

$ stagefright -s test.mp4

adb logcat output:


01-16 06:38:06.899   598   598 I /system/bin/tombstoned: received crash request for pid 7924
--------- beginning of crash
01-16 06:38:06.901  7924  7968 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-16 06:38:06.902  7924  7968 F DEBUG   : Build fingerprint: 'google/bullhead/bullhead:8.0.0/OPR4.170623.009/4302492:user/release-keys'
01-16 06:38:06.902  7924  7968 F DEBUG   : Revision: 'rev_1.0'
01-16 06:38:06.902  7924  7968 F DEBUG   : ABI: 'arm'
01-16 06:38:06.902  7924  7968 F DEBUG   : pid: 7924, tid: 7968, name: media.codec  >>> android.hardwar <<<
01-16 06:38:06.902  7924  7968 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x4677b94d
01-16 06:38:06.909  7924  7968 F DEBUG   :     r0 4677b93d  r1 e4c02678  r2 0000012c  r3 e5e2435c
01-16 06:38:06.909  7924  7968 F DEBUG   :     r4 e5fb9000  r5 4677b93d  r6 e5fb9000  r7 e5fa9090
01-16 06:38:06.909  7924  7968 F DEBUG   :     r8 e5f98020  r9 e5f98000  sl e4c02808  fp 00000000
01-16 06:38:06.909  7924  7968 F DEBUG   :     ip e5e7df10  sp e4c02630  lr e5e21748  pc e5e348ac  cpsr 200f0010
01-16 06:38:06.917  7924  7968 F DEBUG   : 
01-16 06:38:06.917  7924  7968 F DEBUG   : backtrace:
01-16 06:38:06.917  7924  7968 F DEBUG   :     #00 pc 0001e8ac  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_jobq_deinit+8)
01-16 06:38:06.917  7924  7968 F DEBUG   :     #01 pc 0000b744  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_free_dynamic_bufs+28)
01-16 06:38:06.917  7924  7968 F DEBUG   :     #02 pc 0000b424  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_init+8)
01-16 06:38:06.917  7924  7968 F DEBUG   :     #03 pc 0000e494  /system/lib/libstagefright_soft_hevcdec.so (ihevcd_ctl+380)
01-16 06:38:06.917  7924  7968 F DEBUG   :     #04 pc 0000a2d1  /system/lib/libstagefright_soft_hevcdec.so (_ZN7android8SoftHEVC12resetDecoderEv+40)
01-16 06:38:06.917  7924  7968 F DEBUG   :     #05 pc 0000a497  /system/lib/libstagefright_soft_hevcdec.so (_ZN7android8SoftHEVC7onResetEv+16)
01-16 06:38:06.917  7924  7968 F DEBUG   :     #06 pc 00039f53  /system/lib/libstagefright_omx.so (_ZN7android22SimpleSoftOMXComponent16checkTransitionsEv+182)
01-16 06:38:06.917  7924  7968 F DEBUG   :     #07 pc 0003a27f  /system/lib/libstagefright_omx.so (_ZN7android22SimpleSoftOMXComponent10freeBufferEjP20OMX_BUFFERHEADERTYPE+182)
01-16 06:38:06.917  7924  7968 F DEBUG   :     #08 pc 000359a9  /system/lib/libstagefright_omx.so (_ZN7android15OMXNodeInstance10freeBufferEjj+76)
01-16 06:38:06.917  7924  7968 F DEBUG   :     #09 pc 00074431  /system/lib/libmedia.so (_ZN7android9BnOMXNode10onTransactEjRKNS_6ParcelEPS1_j+548)
01-16 06:38:06.917  7924  7968 F DEBUG   :     #10 pc 000406ef  /system/lib/libbinder.so (_ZN7android7BBinder8transactEjRKNS_6ParcelEPS1_j+70)
01-16 06:38:06.917  7924  7968 F DEBUG   :     #11 pc 000483e5  /system/lib/libbinder.so (_ZN7android14IPCThreadState14executeCommandEi+584)
01-16 06:38:06.917  7924  7968 F DEBUG   :     #12 pc 0004809d  /system/lib/libbinder.so (_ZN7android14IPCThreadState20getAndExecuteCommandEv+112)
01-16 06:38:06.918  7924  7968 F DEBUG   :     #13 pc 0004859f  /system/lib/libbinder.so (_ZN7android14IPCThreadState14joinThreadPoolEb+38)
01-16 06:38:06.918  7924  7968 F DEBUG   :     #14 pc 0005eb25  /system/lib/libbinder.so
01-16 06:38:06.918  7924  7968 F DEBUG   :     #15 pc 0000d38d  /system/lib/libutils.so (_ZN7android6Thread11_threadLoopEPv+140)
01-16 06:38:06.918  7924  7968 F DEBUG   :     #16 pc 00047c3f  /system/lib/libc.so (_ZL15__pthread_startPv+22)
01-16 06:38:06.918  7924  7968 F DEBUG   :     #17 pc 0001af5d  /system/lib/libc.so (__start_thread+32)
01-16 06:38:06.926   598   598 E /system/bin/tombstoned: Tombstone written to: /data/tombstones//tombstone_05
--------- beginning of system
01-16 06:38:06.927   767   791 I BootReceiver: Copying /data/tombstones/tombstone_05 to DropBox (SYSTEM_TOMBSTONE)
01-16 06:38:06.934   355   355 I ServiceManager: service 'media.codec' died
01-16 06:38:06.934  7961  7965 E ACodec  : OMX/mediaserver died, signalling error!
01-16 06:38:06.934  7961  7965 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
01-16 06:38:06.934  7961  7964 E MediaCodec: Codec reported err 0xffffffe0, actionCode 0, while in state 9
