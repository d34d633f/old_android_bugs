Trigger for new 0day libavc bug.

To test it: copy 1.mp4 to /mnt/sdcard/Download and open this folder using the Photos app.

Tested on Nexus 5X with MTC19T factory image.

Crash log:
05-12 01:34:10.923   490  6076 F libc    : Fatal signal 11 (SIGSEGV), code 1, fault addr 0xee684f04 in tid 6076 (le.h264.decoder)
05-12 01:34:10.924   881   894 I ActivityManager: Waited long enough for: ServiceRecord{a318609 u0 com.qualcomm.qcrilmsgtunnel/.QcrilMsgTunnelService}
05-12 01:34:10.979   485   485 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
05-12 01:34:10.980   485   485 F DEBUG   : Build fingerprint: 'google/bullhead/bullhead:6.0.1/MTC19T/2741993:user/release-keys'
05-12 01:34:10.980   485   485 F DEBUG   : Revision: 'rev_1.0'
05-12 01:34:10.981   485   485 F DEBUG   : ABI: 'arm'
05-12 01:34:10.981   485   485 F DEBUG   : pid: 490, tid: 6076, name: le.h264.decoder  >>> /system/bin/mediaserver <<<
05-12 01:34:10.982   485   485 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0xee684f04
05-12 01:34:10.982   881  2784 W NativeCrashListener: Couldn't find ProcessRecord for pid 490
05-12 01:34:10.992   485   485 F DEBUG   :     r0 f0abf290  r1 00000000  r2 ee684f04  r3 000000ff
05-12 01:34:10.993   485   485 E DEBUG   : AM write failed: Broken pipe
05-12 01:34:10.993   485   485 F DEBUG   :     r4 00000000  r5 00000004  r6 f0abf36c  r7 f0abf29c
05-12 01:34:10.993   485   485 F DEBUG   :     r8 f0abf290  r9 00000001  sl f0c03ea4  fp 000000ff
05-12 01:34:10.994   485   485 F DEBUG   :     ip f0abf29c  sp f0abf270  lr 00000008  pc f0bcba8e  cpsr 20070030
05-12 01:34:10.999   485   485 F DEBUG   : backtrace:
05-12 01:34:11.000   485   485 F DEBUG   :     #00 pc 00021a8e  /system/lib/libstagefright_soft_avcdec.so (ih264d_mvpred_mbaff+941)
05-12 01:34:11.000   485   485 F DEBUG   :     #01 pc 000260cf  /system/lib/libstagefright_soft_avcdec.so (ih264d_mv_pred_ref_tfr_nby2_pmb+558)
05-12 01:34:11.001   485   485 F DEBUG   :     #02 pc 00019e27  /system/lib/libstagefright_soft_avcdec.so (ih264d_mark_err_slice_skip+526)
05-12 01:34:11.001   485   485 F DEBUG   :     #03 pc 00027f59  /system/lib/libstagefright_soft_avcdec.so (ih264d_parse_decode_slice+972)
05-12 01:34:11.001   485   485 F DEBUG   :     #04 pc 0001fc77  /system/lib/libstagefright_soft_avcdec.so (ih264d_parse_nal_unit+182)
05-12 01:34:11.002   485   485 F DEBUG   :     #05 pc 0000c403  /system/lib/libstagefright_soft_avcdec.so (ih264d_video_decode+750)
05-12 01:34:11.002   485   485 F DEBUG   :     #06 pc 0000aaab  /system/lib/libstagefright_soft_avcdec.so
05-12 01:34:11.003   485   485 F DEBUG   :     #07 pc 000227e1  /system/lib/libstagefright_omx.so (_ZN7android22SimpleSoftOMXComponent17onMessageReceivedERKNS_2spINS_8AMessageEEE+240)
05-12 01:34:11.003   485   485 F DEBUG   :     #08 pc 000236e7  /system/lib/libstagefright_omx.so
05-12 01:34:11.004   485   485 F DEBUG   :     #09 pc 0000b309  /system/lib/libstagefright_foundation.so (_ZN7android8AHandler14deliverMessageERKNS_2spINS_8AMessageEEE+16)
05-12 01:34:11.004   485   485 F DEBUG   :     #10 pc 0000d327  /system/lib/libstagefright_foundation.so (_ZN7android8AMessage7deliverEv+54)
05-12 01:34:11.005   485   485 F DEBUG   :     #11 pc 0000bd2d  /system/lib/libstagefright_foundation.so (_ZN7android7ALooper4loopEv+224)
05-12 01:34:11.006   485   485 F DEBUG   :     #12 pc 00010071  /system/lib/libutils.so (_ZN7android6Thread11_threadLoopEPv+112)
05-12 01:34:11.006   485   485 F DEBUG   :     #13 pc 0003f883  /system/lib/libc.so (_ZL15__pthread_startPv+30)
05-12 01:34:11.006   485   485 F DEBUG   :     #14 pc 00019f75  /system/lib/libc.so (__start_thread+6)

