Android libhevc denial of service 

How to reproduce:
1) upload test.mp4 to device and use stagefright binary to scan it

$ stagefright -s test.mp4

adb logcat output:


beginning of crash
01-16 08:31:49.588 32436  3418 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-16 08:31:49.589 32436  3418 F DEBUG   : Build fingerprint: 'google/bullhead/bullhead:8.0.0/OPR4.170623.009/4302492:user/release-keys'
01-16 08:31:49.589 32436  3418 F DEBUG   : Revision: 'rev_1.0'
01-16 08:31:49.589 32436  3418 F DEBUG   : ABI: 'arm'
01-16 08:31:49.589 32436  3418 F DEBUG   : pid: 32436, tid: 3418, name: media.codec  >>> android.hardwar <<<
01-16 08:31:49.589 32436  3418 F DEBUG   : signal 6 (SIGABRT), code -6 (SI_TKILL), fault addr --------
01-16 08:31:49.593 32436  3418 F DEBUG   : Abort message: 'frameworks/av/media/libstagefright/omx/SimpleSoftOMXComponent.cpp:462 CHECK_EQ( (int)mState,(int)mTargetState) failed: 2 vs. 1'
01-16 08:31:49.593 32436  3418 F DEBUG   :     r0 00000000  r1 00000d5a  r2 00000006  r3 00000008
01-16 08:31:49.593 32436  3418 F DEBUG   :     r4 00007eb4  r5 00000d5a  r6 ed2163d0  r7 0000010c
01-16 08:31:49.593 32436  3418 F DEBUG   :     r8 ed285520  r9 ed726268  sl ed285500  fp 00000000
01-16 08:31:49.593 32436  3418 F DEBUG   :     ip 00000000  sp ed2163c0  lr eecf63b7  pc eed2691c  cpsr 280f0010
01-16 08:31:49.595 32436  3418 F DEBUG   : 
01-16 08:31:49.595 32436  3418 F DEBUG   : backtrace:
01-16 08:31:49.595 32436  3418 F DEBUG   :     #00 pc 0004a91c  /system/lib/libc.so (tgkill+12)
01-16 08:31:49.595 32436  3418 F DEBUG   :     #01 pc 0001a3b3  /system/lib/libc.so (abort+54)
01-16 08:31:49.595 32436  3418 F DEBUG   :     #02 pc 000065f9  /system/lib/liblog.so (__android_log_assert+152)
01-16 08:31:49.595 32436  3418 F DEBUG   :     #03 pc 0003a8e3  /system/lib/libstagefright_omx.so (_ZN7android22SimpleSoftOMXComponent13onChangeStateE13OMX_STATETYPE+358)
01-16 08:31:49.595 32436  3418 F DEBUG   :     #04 pc 0003a5c3  /system/lib/libstagefright_omx.so (_ZN7android22SimpleSoftOMXComponent17onMessageReceivedERKNS_2spINS_8AMessageEEE+302)
01-16 08:31:49.595 32436  3418 F DEBUG   :     #05 pc 0003b5cd  /system/lib/libstagefright_omx.so
01-16 08:31:49.595 32436  3418 F DEBUG   :     #06 pc 0000fb99  /system/lib/libstagefright_foundation.so (_ZN7android8AHandler14deliverMessageERKNS_2spINS_8AMessageEEE+24)
01-16 08:31:49.595 32436  3418 F DEBUG   :     #07 pc 00011ff1  /system/lib/libstagefright_foundation.so (_ZN7android8AMessage7deliverEv+60)
01-16 08:31:49.595 32436  3418 F DEBUG   :     #08 pc 00010815  /system/lib/libstagefright_foundation.so (_ZN7android7ALooper4loopEv+484)
01-16 08:31:49.596 32436  3418 F DEBUG   :     #09 pc 0000d40f  /system/lib/libutils.so (_ZN7android6Thread11_threadLoopEPv+270)
01-16 08:31:49.596 32436  3418 F DEBUG   :     #10 pc 00047c3f  /system/lib/libc.so (_ZL15__pthread_startPv+22)
01-16 08:31:49.596 32436  3418 F DEBUG   :     #11 pc 0001af5d  /system/lib/libc.so (__start_thread+32)
01-16 08:31:49.598   598   598 E /system/bin/tombstoned: 
