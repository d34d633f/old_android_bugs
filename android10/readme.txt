Trigger for new 0day libavc bug.

To test it: copy 1.mp4 to /mnt/sdcard/Download and open this folder using the Photos app.

Tested on Nexus 5X with MTC19T factory image.

Crash log:
05-12 01:22:30.839   491  5806 F libc    : Fatal signal 11 (SIGSEGV), code 1, fault addr 0x1 in tid 5806 (le.h264.decoder)
05-12 01:22:30.893   487   487 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
05-12 01:22:30.894   487   487 F DEBUG   : Build fingerprint: 'google/bullhead/bullhead:6.0.1/MTC19T/2741993:user/release-keys'
05-12 01:22:30.894   487   487 F DEBUG   : Revision: 'rev_1.0'
05-12 01:22:30.895   487   487 F DEBUG   : ABI: 'arm'
05-12 01:22:30.895   883  2870 W NativeCrashListener: Couldn't find ProcessRecord for pid 491
05-12 01:22:30.895   487   487 F DEBUG   : pid: 491, tid: 5806, name: le.h264.decoder  >>> /system/bin/mediaserver <<<
05-12 01:22:30.896   487   487 E DEBUG   : AM write failed: Broken pipe
05-12 01:22:30.896   487   487 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x1
05-12 01:22:30.920   487   487 F DEBUG   :     r0 ef4bf838  r1 f1c894b8  r2 00000001  r3 00000100
05-12 01:22:30.921   487   487 F DEBUG   :     r4 00000005  r5 00000010  r6 000015c4  r7 00000004
05-12 01:22:30.922   487   487 F DEBUG   :     r8 00000571  r9 ffffffff  sl 00000001  fp 00000100
05-12 01:22:30.922   487   487 F DEBUG   :     ip 0000060f  sp ef4bf6d0  lr f007ed1b  pc f007aae0  cpsr 80070010
05-12 01:22:30.924   487   487 F DEBUG   : 
05-12 01:22:30.924   487   487 F DEBUG   : backtrace:
05-12 01:22:30.924   487   487 F DEBUG   :     #00 pc 00013ae0  /system/lib/libstagefright_soft_avcdec.so

