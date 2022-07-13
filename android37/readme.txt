Android libavc heap overflow

Test device
$ adb shell getprop ro.build.description
aosp_bullhead-userdebug 7.1.1 N4F26I eng.ffu.20170112.053429 test-keys

How to reproduce:
1) compile libavc with ASAN (edit Android.mk then do 'make libstagefright_soft_avcdec_32')
2) upload 1.mp4 to device
3) run stagefrigt binary to decode file
$ stagefright -s /mnt/sdcard/1.mp4


04-15 08:47:42.068   469  1692 I         : =================================================================
04-15 08:47:42.068   469  1692 I         : 
04-15 08:47:42.069   469  1692 I         : 
04-15 08:47:42.069   469  1692 I         : ==469==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xed681000 at pc 0xedeb40a0 bp 0xed2ff130 sp 0xed2ff128
04-15 08:47:42.069   469  1692 I         : 
04-15 08:47:42.070   469  1692 I         : 
04-15 08:47:42.070   469  1692 I         : WRITE of size 4 at 0xed681000 thread T111 (le.h264.decoder)
04-15 08:47:42.070   469  1692 I         : 
04-15 08:47:42.154   469  1692 I         :     #0 0xedeb409f in ih264d_process_nal_unit /proc/self/cwd/external/libavc/decoder/ih264d_nal.c:344:27
04-15 08:47:42.154   469  1692 I         : 
04-15 08:47:42.156   469  1692 I         :     #1 0xede7170b in ih264d_parse_nal_unit /proc/self/cwd/external/libavc/decoder/ih264d_parse_headers.c:1072:13
04-15 08:47:42.156   469  1692 I         : 
04-15 08:47:42.157   469  1692 I         :     #2 0xede213a3 in ih264d_video_decode /proc/self/cwd/external/libavc/decoder/ih264d_api.c:2092:15
04-15 08:47:42.157   469  1692 I         : 
04-15 08:47:42.157   469  1692 I         :     #3 0xede2a6af in ih264d_api_function /proc/self/cwd/external/libavc/decoder/ih264d_api.c:3680:26
04-15 08:47:42.157   469  1692 I         : 
04-15 08:47:42.158   469  1692 I         :     #4 0xede1b7d5 in android::SoftAVC::onQueueFilled(unsigned int) /proc/self/cwd/frameworks/av/media/libstagefright/codecs/avcdec/SoftAVCDec.cpp:629:22
04-15 08:47:42.158   469  1692 I         : 
04-15 08:47:42.160   469  1692 I         :     #5 0xf01c2161 in android::SimpleSoftOMXComponent::onMessageReceived(android::sp<android::AMessage> const&) (/system/lib/libstagefright_omx.so+0x23161)
04-15 08:47:42.160   469  1692 I         : 
04-15 08:47:42.160   469  1692 I         :     #6 0xf01c319b  (/system/lib/libstagefright_omx.so+0x2419b)
04-15 08:47:42.160   469  1692 I         : 
04-15 08:47:42.161   469  1692 I         :     #7 0xf01573d1 in android::AHandler::deliverMessage(android::sp<android::AMessage> const&) (/system/lib/libstagefright_foundation.so+0xf3d1)
04-15 08:47:42.161   469  1692 I         : 
04-15 08:47:42.161   469  1692 I         :     #8 0xf0159653 in android::AMessage::deliver() (/system/lib/libstagefright_foundation.so+0x11653)
04-15 08:47:42.161   469  1692 I         : 
04-15 08:47:42.161   469  1692 I         :     #9 0xf0157f3b in android::ALooper::loop() (/system/lib/libstagefright_foundation.so+0xff3b)
04-15 08:47:42.161   469  1692 I         : 
04-15 08:47:42.162   469  1692 I         :     #10 0xefeb03c1 in android::Thread::_threadLoop(void*) (/system/lib/libutils.so+0xe3c1)
04-15 08:47:42.162   469  1692 I         : 
04-15 08:47:42.167   469  1692 I         :     #11 0xeff0a023 in __pthread_start(void*) (/system/lib/libc.so+0x47023)
04-15 08:47:42.167   469  1692 I         : 
04-15 08:47:42.167   469  1692 I         :     #12 0xefedce3d in __start_thread (/system/lib/libc.so+0x19e3d)
04-15 08:47:42.167   469  1692 I         : 
04-15 08:47:42.167   469  1692 I         : 
04-15 08:47:42.167   469  1692 I         : 
04-15 08:47:42.167   469  1692 I         : 0xed681000 is located 0 bytes to the right of 256000-byte region [0xed642800,0xed681000)
04-15 08:47:42.167   469  1692 I         : 
04-15 08:47:42.168   469  1692 I         : allocated by thread T111 (le.h264.decoder) here:
04-15 08:47:42.168   469  1692 I         : 
04-15 08:47:42.169   469  1692 I         :     #0 0xf04211ef in memalign (/system/lib/libclang_rt.asan-arm-android.so+0x751ef)
04-15 08:47:42.169   469  1692 I         : 
04-15 08:47:42.169   469  1692 I         :     #1 0xede21167 in ih264d_video_decode /proc/self/cwd/external/libavc/decoder/ih264d_api.c:1966:22
04-15 08:47:42.169   469  1692 I         : 
04-15 08:47:42.170   469  1692 I         :     #2 0xede2a6af in ih264d_api_function /proc/self/cwd/external/libavc/decoder/ih264d_api.c:3680:26
04-15 08:47:42.170   469  1692 I         : 
04-15 08:47:42.170   469  1692 I         :     #3 0xede1b7d5 in android::SoftAVC::onQueueFilled(unsigned int) /proc/self/cwd/frameworks/av/media/libstagefright/codecs/avcdec/SoftAVCDec.cpp:629:22
04-15 08:47:42.170   469  1692 I         : 
04-15 08:47:42.170   469  1692 I         : 
04-15 08:47:42.170   469  1692 I         : 
04-15 08:47:42.170   469  1692 I         : Thread T111 (le.h264.decoder) created by T4 (Binder:469_2) here:
04-15 08:47:42.170   469  1692 I         : 
04-15 08:47:42.171   469  1692 I         :     #0 0xf04084db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-15 08:47:42.171   469  1692 I         : 
04-15 08:47:42.171   469  1692 I         :     #1 0xefeafef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-15 08:47:42.171   469  1692 I         : 
04-15 08:47:42.171   469  1692 I         : 
04-15 08:47:42.171   469  1692 I         : 
04-15 08:47:42.171   469  1692 I         : Thread T4 (Binder:469_2) created by T1 (Binder:469_1) here:
04-15 08:47:42.171   469  1692 I         : 
04-15 08:47:42.171   469  1692 I         :     #0 0xf04084db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-15 08:47:42.171   469  1692 I         : 
04-15 08:47:42.171   469  1692 I         :     #1 0xefeafef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-15 08:47:42.171   469  1692 I         : 
04-15 08:47:42.171   469  1692 I         : 
04-15 08:47:42.171   469  1692 I         : 
04-15 08:47:42.171   469  1692 I         : Thread T1 (Binder:469_1) created by T0 here:
04-15 08:47:42.172   469  1692 I         : 
04-15 08:47:42.172   469  1692 I         :     #0 0xf04084db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-15 08:47:42.172   469  1692 I         : 
04-15 08:47:42.172   469  1692 I         :     #1 0xefeafef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-15 08:47:42.172   469  1692 I         : 
04-15 08:47:42.172   469  1692 I         :     #2 0xefed9c4d in __libc_init (/system/lib/libc.so+0x16c4d)
04-15 08:47:42.172   469  1692 I         : 
04-15 08:47:42.173   469  1692 I         :     #3 0xffffffff  (<unknown module>)
04-15 08:47:42.173   469  1692 I         : 
04-15 08:47:42.173   469  1692 I         : 
04-15 08:47:42.173   469  1692 I         : 
04-15 08:47:42.173   469  1692 I         : SUMMARY: AddressSanitizer: heap-buffer-overflow /proc/self/cwd/external/libavc/decoder/ih264d_nal.c:344:27 in ih264d_process_nal_unit
04-15 08:47:42.173   469  1692 I         : 
04-15 08:47:42.174   469  1692 I         : Shadow bytes around the buggy address:
04-15 08:47:42.174   469  1692 I         :   0x1dad01b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-15 08:47:42.174   469  1692 I         :   0x1dad01c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-15 08:47:42.174   469  1692 I         :   0x1dad01d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-15 08:47:42.174   469  1692 I         :   0x1dad01e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-15 08:47:42.174   469  1692 I         :   0x1dad01f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-15 08:47:42.174   469  1692 I         : =>0x1dad0200:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 08:47:42.174   469  1692 I         :   0x1dad0210: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 08:47:42.174   469  1692 I         :   0x1dad0220: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 08:47:42.174   469  1692 I         :   0x1dad0230: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 08:47:42.174   469  1692 I         :   0x1dad0240: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 08:47:42.174   469  1692 I         :   0x1dad0250: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 08:47:42.174   469  1692 I         : Shadow byte legend (one shadow byte represents 8 application bytes):
04-15 08:47:42.174   469  1692 I         :   Addressable:           00
04-15 08:47:42.174   469  1692 I         :   Partially addressable: 01 02 03 04 05 06 07 
04-15 08:47:42.174   469  1692 I         :   Heap left redzone:       fa
04-15 08:47:42.174   469  1692 I         :   Heap right redzone:      fb
04-15 08:47:42.174   469  1692 I         :   Freed heap region:       fd
04-15 08:47:42.174   469  1692 I         :   Stack left redzone:      f1
04-15 08:47:42.174   469  1692 I         :   Stack mid redzone:       f2
04-15 08:47:42.174   469  1692 I         :   Stack right redzone:     f3
04-15 08:47:42.174   469  1692 I         :   Stack partial redzone:   f4
04-15 08:47:42.174   469  1692 I         :   Stack after return:      f5
04-15 08:47:42.174   469  1692 I         :   Stack use after scope:   f8
04-15 08:47:42.174   469  1692 I         :   Global redzone:          f9
04-15 08:47:42.174   469  1692 I         :   Global init order:       f6
04-15 08:47:42.174   469  1692 I         :   Poisoned by user:        f7
04-15 08:47:42.174   469  1692 I         :   Container overflow:      fc
04-15 08:47:42.174   469  1692 I         :   Array cookie:            ac
04-15 08:47:42.174   469  1692 I         :   Intra object redzone:    bb
04-15 08:47:42.174   469  1692 I         :   ASan internal:           fe
04-15 08:47:42.174   469  1692 I         :   Left alloca redzone:     ca
04-15 08:47:42.174   469  1692 I         :   Right alloca redzone:    cb
04-15 08:47:42.174   469  1692 I         : 
04-15 08:47:42.174   469  1692 I         : ==469==ABORTING
04-15 08:47:42.174   469  1692 I         : 
04-15 08:47:42.185   386   386 I ServiceManager: service 'media.codec' died
04-15 08:47:42.185  1687  1691 E ACodec  : OMX/mediaserver died, signalling error!
04-15 08:47:42.185  1687  1691 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
