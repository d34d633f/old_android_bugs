Android libhevc overflow 

How to reproduce:
1) upload test.mp4 to device and use stagefright binary to scan it

$ stagefright -s test.mp4

adb logcat output:


beginning of crash
01-31 16:10:35.754 20056  2327 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-31 16:10:35.755 20056  2327 F DEBUG   : Build fingerprint: 'google/bullhead/bullhead:8.0.0/OPR4.170623.009/4302492:user/release-keys'
01-31 16:10:35.755 20056  2327 F DEBUG   : Revision: 'rev_1.0'
01-31 16:10:35.755 20056  2327 F DEBUG   : ABI: 'arm'
01-31 16:10:35.755 20056  2327 F DEBUG   : pid: 20056, tid: 2327, name: media.codec  >>> android.hardwar <<<
01-31 16:10:35.755 20056  2327 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x1ad13ac0
01-31 16:10:35.760 20056  2327 F DEBUG   :     r0 1ad13ac0  r1 ee1d4000  r2 00001120  r3 00000040
01-31 16:10:35.760 20056  2327 F DEBUG   :     r4 00000040  r5 00000080  r6 1ad14be0  r7 000001fc
01-31 16:10:35.760 20056  2327 F DEBUG   :     r8 00004440  r9 00000000  sl ee1d4080  fp 000000c0
01-31 16:10:35.760 20056  2327 F DEBUG   :     ip 00000040  sp ebaff620  lr ef02bb2c  pc ef04120c  cpsr 000f0010
01-31 16:10:35.760 20056  2327 F DEBUG   : 
01-31 16:10:35.760 20056  2327 F DEBUG   : backtrace:
01-31 16:10:35.761 20056  2327 F DEBUG   :     #00 pc 0003c20c  /system/lib/libstagefright_soft_hevcdec.so
01-31 16:10:35.762   627   627 E /system/bin/tombstoned: Tombstone written to: /data/tombstones//tombstone_00
--------- beginning of system
01-31 16:10:35.762   770   791 I BootReceiver: Copying /data/tombstones/tombstone_00 to DropBox (SYSTEM_TOMBSTONE)
01-31 16:10:35.790   355   355 I ServiceManager: service 'media.codec' died
01-31 16:10:35.790  2316  2321 E ACodec  : OMX/mediaserver died, signalling error!
01-31 16:10:35.790  2316  2321 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
01-31 16:10:35.790  2316  2320 E MediaCodec: Codec reported err 0xffffffe0, actionCode 0, while in state 6
01-31 16:10:35.985  2331  2331 I /vendor/bin/hw/android.hardware.media.omx@1.0-service: mediacodecservice starting
01-31 16:10:35.986  2331  2331 W /vendor/bin/hw/android.hardware.media.omx@1.0-service: Could not read additional policy file '/vendor/etc/seccomp_policy/mediacodec.policy'
01-31 16:10:35.986  2331  2331 W /vendor/bin/hw/android.hardware.media.omx@1.0-service: libminijail[2331]: allowing syscall: clock_gettime
01-31 16:10:35.986  2331  2331 W /vendor/bin/hw/android.hardware.media.omx@1.0-service: libminijail[2331]: allowing syscall: connect
01-31 16:10:35.986  2331  2331 W /vendor/bin/hw/android.hardware.media.omx@1.0-service: libminijail[2331]: allowing syscall: fcntl64
01-31 16:10:35.986  2331  2331 W /vendor/bin/hw/android.hardware.media.omx@1.0-service: libminijail[2331]: allowing syscall: socket
01-31 16:10:35.986  2331  2331 W /vendor/bin/hw/android.hardware.media.omx@1.0-service: libminijail[2331]: allowing syscall: writev
01-31 16:10:35.987  2331  2331 W /vendor/bin/hw/android.hardware.media.omx@1.0-service: libminijail[2331]: logging seccomp filter failures
01-31 16:10:35.989  2331  2331 I /vendor/bin/hw/android.hardware.media.omx@1.0-service: Non-Treble OMX service created.
