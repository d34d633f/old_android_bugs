Android libhevc overflow

How to reproduce:
1) upload test.mp4 to device and use stagefright binary to scan it

$ stagefright -s test.mp4

adb logcat output:


--------- beginning of main
01-17 05:09:18.862   598   598 I /system/bin/tombstoned: received crash request for pid 23533
--------- beginning of crash
01-17 05:09:18.864 23533 24081 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-17 05:09:18.864 23533 24081 F DEBUG   : Build fingerprint: 'google/bullhead/bullhead:8.0.0/OPR4.170623.009/4302492:user/release-keys'
01-17 05:09:18.864 23533 24081 F DEBUG   : Revision: 'rev_1.0'
01-17 05:09:18.864 23533 24081 F DEBUG   : ABI: 'arm'
01-17 05:09:18.864 23533 24081 F DEBUG   : pid: 23533, tid: 24081, name: media.codec  >>> android.hardwar <<<
01-17 05:09:18.864 23533 24081 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0xe6880000
01-17 05:09:18.869 23533 24081 F DEBUG   :     r0 e687dba0  r1 e6880000  r2 c6b40780  r3 00000070
01-17 05:09:18.869 23533 24081 F DEBUG   :     r4 00000070  r5 000021a0  r6 00000070  r7 00000070
01-17 05:09:18.869 23533 24081 F DEBUG   :     r8 00000040  r9 fff6ffb8  sl ffffde70  fp 00000060
01-17 05:09:18.869 23533 24081 F DEBUG   :     ip ffffffa0  sp e6188620  lr 00004308  pc e69c1a7c  cpsr a00f0010
01-17 05:09:18.870 23533 24081 F DEBUG   : 
01-17 05:09:18.870 23533 24081 F DEBUG   : backtrace:
01-17 05:09:18.870 23533 24081 F DEBUG   :     #00 pc 00034a7c  /system/lib/libstagefright_soft_hevcdec.so
01-17 05:09:18.871   598   598 E /system/bin/tombstoned: Tombstone written to: /data/tombstones//tombstone_05
--------- beginning of system
