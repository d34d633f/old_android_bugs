Android libavc use after free

Test device
$ adb shell getprop ro.build.description
aosp_bullhead-userdebug 7.1.1 N4F26I eng.ffu.20170112.053429 test-keys

How to reproduce:
1) compile libavc with ASAN (edit Android.mk then do 'make libstagefright_soft_avcdec_32')
2) upload 1.mp4 to device
3) run stagefrigt binary to decode file
$ stagefright -s /mnt/sdcard/1.mp4

ASAN log:


AddressSanitizer: heap-buffer-overflow on address 0xe69090cd at pc 0xe6c7437c bp 0xe5dfedc8 sp 0xe5dfedc0
04-15 17:09:33.351  1247  2337 I         : 
04-15 17:09:33.351  1247  2337 I         : 
04-15 17:09:33.351  1247  2337 I         : READ of size 1 at 0xe69090cd thread T212 (le.h264.decoder)
04-15 17:09:33.351  1247  2337 I         : 
04-15 17:09:33.420  1247  2337 I         :     #0 0xe6c7437b in ih264d_get_mb_info_cabac_nonmbaff /proc/self/cwd/external/libavc/decoder/ih264d_mb_utils.c:449:64
04-15 17:09:33.420  1247  2337 I         : 
04-15 17:09:33.420  1247  2337 I         :     #1 0xe6c5bf5f in ih264d_parse_islice_data_cabac /proc/self/cwd/external/libavc/decoder/ih264d_parse_islice.c:1034:13
04-15 17:09:33.420  1247  2337 I         : 
04-15 17:09:33.421  1247  2337 I         :     #2 0xe6c5cd53 in ih264d_parse_islice /proc/self/cwd/external/libavc/decoder/ih264d_parse_islice.c:1462:15
04-15 17:09:33.421  1247  2337 I         : 
04-15 17:09:33.421  1247  2337 I         :     #3 0xe6c9e5bb in ih264d_parse_decode_slice /proc/self/cwd/external/libavc/decoder/ih264d_parse_slice.c:1885:15
04-15 17:09:33.421  1247  2337 I         : 
04-15 17:09:33.422  1247  2337 I         :     #4 0xe6c7183b in ih264d_parse_nal_unit /proc/self/cwd/external/libavc/decoder/ih264d_parse_headers.c:1116:40
04-15 17:09:33.422  1247  2337 I         : 
04-15 17:09:33.423  1247  2337 I         :     #5 0xe6c213a3 in ih264d_video_decode /proc/self/cwd/external/libavc/decoder/ih264d_api.c:2092:15
04-15 17:09:33.423  1247  2337 I         : 
04-15 17:09:33.423  1247  2337 I         :     #6 0xe6c2a6af in ih264d_api_function /proc/self/cwd/external/libavc/decoder/ih264d_api.c:3680:26
04-15 17:09:33.423  1247  2337 I         : 
04-15 17:09:33.425  1247  2337 I         :     #7 0xe6c1b7d5 in android::SoftAVC::onQueueFilled(unsigned int) /proc/self/cwd/frameworks/av/media/libstagefright/codecs/avcdec/SoftAVCDec.cpp:629:22
04-15 17:09:33.425  1247  2337 I         : 
04-15 17:09:33.426  1247  2337 I         :     #8 0xe984d161 in android::SimpleSoftOMXComponent::onMessageReceived(android::sp<android::AMessage> const&) (/system/lib/libstagefright_omx.so+0x23161)
04-15 17:09:33.426  1247  2337 I         : 
04-15 17:09:33.426  1247  2337 I         :     #9 0xe984e19b  (/system/lib/libstagefright_omx.so+0x2419b)
04-15 17:09:33.426  1247  2337 I         : 
04-15 17:09:33.427  1247  2337 I         :     #10 0xe966c3d1 in android::AHandler::deliverMessage(android::sp<android::AMessage> const&) (/system/lib/libstagefright_foundation.so+0xf3d1)
04-15 17:09:33.427  1247  2337 I         : 
04-15 17:09:33.428  1247  2337 I         :     #11 0xe966e653 in android::AMessage::deliver() (/system/lib/libstagefright_foundation.so+0x11653)
04-15 17:09:33.428  1247  2337 I         : 
04-15 17:09:33.428  1247  2337 I         :     #12 0xe966cf3b in android::ALooper::loop() (/system/lib/libstagefright_foundation.so+0xff3b)
04-15 17:09:33.428  1247  2337 I         : 
04-15 17:09:33.429  1247  2337 I         :     #13 0xe981f3c1 in android::Thread::_threadLoop(void*) (/system/lib/libutils.so+0xe3c1)
04-15 17:09:33.429  1247  2337 I         : 
04-15 17:09:33.433  1247  2337 I         :     #14 0xe9612023 in __pthread_start(void*) (/system/lib/libc.so+0x47023)
04-15 17:09:33.433  1247  2337 I         : 
04-15 17:09:33.433  1247  2337 I         :     #15 0xe95e4e3d in __start_thread (/system/lib/libc.so+0x19e3d)
04-15 17:09:33.433  1247  2337 I         : 
04-15 17:09:33.433  1247  2337 I         : 
04-15 17:09:33.433  1247  2337 I         : 
04-15 17:09:33.434  1247  2337 I         : 0xe69090cd is located 101 bytes to the right of 360-byte region [0xe6908f00,0xe6909068)
04-15 17:09:33.434  1247  2337 I         : 
04-15 17:09:33.434  1247  2337 I         : allocated by thread T212 (le.h264.decoder) here:
04-15 17:09:33.434  1247  2337 I         : 
04-15 17:09:33.436  1247  2337 I         :     #0 0xe99011ef in memalign (/system/lib/libclang_rt.asan-arm-android.so+0x751ef)
04-15 17:09:33.436  1247  2337 I         : 
04-15 17:09:33.437  1247  2337 I         :     #1 0xe6c8079f in ih264d_allocate_dynamic_bufs /proc/self/cwd/external/libavc/decoder/ih264d_utils.c:1951:14
04-15 17:09:33.437  1247  2337 I         : 
04-15 17:09:33.437  1247  2337 I         :     #2 0xe6c7ed8f in ih264d_init_pic /proc/self/cwd/external/libavc/decoder/ih264d_utils.c:812:15
04-15 17:09:33.437  1247  2337 I         : 
04-15 17:09:33.437  1247  2337 I         :     #3 0xe6c9765f in ih264d_start_of_pic /proc/self/cwd/external/libavc/decoder/ih264d_parse_slice.c:338:11
04-15 17:09:33.437  1247  2337 I         : 
04-15 17:09:33.437  1247  2337 I         :     #4 0xe6c9d6c3 in ih264d_parse_decode_slice /proc/self/cwd/external/libavc/decoder/ih264d_parse_slice.c:1587:19
04-15 17:09:33.437  1247  2337 I         : 
04-15 17:09:33.438  1247  2337 I         :     #5 0xe6c7183b in ih264d_parse_nal_unit /proc/self/cwd/external/libavc/decoder/ih264d_parse_headers.c:1116:40
04-15 17:09:33.438  1247  2337 I         : 
04-15 17:09:33.438  1247  2337 I         :     #6 0xe6c213a3 in ih264d_video_decode /proc/self/cwd/external/libavc/decoder/ih264d_api.c:2092:15
04-15 17:09:33.438  1247  2337 I         : 
04-15 17:09:33.438  1247  2337 I         :     #7 0xe6c2a6af in ih264d_api_function /proc/self/cwd/external/libavc/decoder/ih264d_api.c:3680:26
04-15 17:09:33.438  1247  2337 I         : 
04-15 17:09:33.438  1247  2337 I         :     #8 0xe6c1b7d5 in android::SoftAVC::onQueueFilled(unsigned int) /proc/self/cwd/frameworks/av/media/libstagefright/codecs/avcdec/SoftAVCDec.cpp:629:22
04-15 17:09:33.438  1247  2337 I         : 
04-15 17:09:33.439  1247  2337 I         : 
04-15 17:09:33.439  1247  2337 I         : 
04-15 17:09:33.439  1247  2337 I         : Thread T212 (le.h264.decoder) created by T13 (Binder:1247_6) here:
04-15 17:09:33.439  1247  2337 I         : 
04-15 17:09:33.439  1247  2337 I         :     #0 0xe98e84db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-15 17:09:33.439  1247  2337 I         : 
04-15 17:09:33.439  1247  2337 I         :     #1 0xe981eef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-15 17:09:33.439  1247  2337 I         : 
04-15 17:09:33.439  1247  2337 I         : 
04-15 17:09:33.439  1247  2337 I         : 
04-15 17:09:33.439  1247  2337 I         : Thread T13 (Binder:1247_6) created by T5 (Binder:1247_3) here:
04-15 17:09:33.439  1247  2337 I         : 
04-15 17:09:33.440  1247  2337 I         :     #0 0xe98e84db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-15 17:09:33.440  1247  2337 I         : 
04-15 17:09:33.440  1247  2337 I         :     #1 0xe981eef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-15 17:09:33.440  1247  2337 I         : 
04-15 17:09:33.440  1247  2337 I         : 
04-15 17:09:33.440  1247  2337 I         : 
04-15 17:09:33.440  1247  2337 I         : Thread T5 (Binder:1247_3) created by T0 here:
04-15 17:09:33.440  1247  2337 I         : 
04-15 17:09:33.440  1247  2337 I         :     #0 0xe98e84db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-15 17:09:33.440  1247  2337 I         : 
04-15 17:09:33.440  1247  2337 I         :     #1 0xe981eef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-15 17:09:33.440  1247  2337 I         : 
04-15 17:09:33.441  1247  2337 I         :     #2 0xe95e1c4d in __libc_init (/system/lib/libc.so+0x16c4d)
04-15 17:09:33.441  1247  2337 I         : 
04-15 17:09:33.441  1247  2337 I         :     #3 0xffffffff  (<unknown module>)
04-15 17:09:33.441  1247  2337 I         : 
04-15 17:09:33.441  1247  2337 I         : 
04-15 17:09:33.441  1247  2337 I         : 
04-15 17:09:33.441  1247  2337 I         : SUMMARY: AddressSanitizer: heap-buffer-overflow /proc/self/cwd/external/libavc/decoder/ih264d_mb_utils.c:449:64 in ih264d_get_mb_info_cabac_nonmbaff
04-15 17:09:33.441  1247  2337 I         : 
04-15 17:09:33.442  1247  2337 I         : Shadow bytes around the buggy address:
04-15 17:09:33.442  1247  2337 I         :   0x1cd211c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 17:09:33.442  1247  2337 I         :   0x1cd211d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 17:09:33.442  1247  2337 I         :   0x1cd211e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-15 17:09:33.442  1247  2337 I         :   0x1cd211f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-15 17:09:33.442  1247  2337 I         :   0x1cd21200: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa
04-15 17:09:33.442  1247  2337 I         : =>0x1cd21210: fa fa fa fa fa fa fa fa fa[fa]fa fa fa fa fa fa
04-15 17:09:33.442  1247  2337 I         :   0x1cd21220: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 17:09:33.442  1247  2337 I         :   0x1cd21230: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-15 17:09:33.442  1247  2337 I         :   0x1cd21240: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-15 17:09:33.442  1247  2337 I         :   0x1cd21250: 00 00 00 00 fa fa fa fa fa fa fa fa fa fa fa fa
04-15 17:09:33.442  1247  2337 I         :   0x1cd21260: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 17:09:33.442  1247  2337 I         : Shadow byte legend (one shadow byte represents 8 application bytes):
04-15 17:09:33.442  1247  2337 I         :   Addressable:           00
04-15 17:09:33.442  1247  2337 I         :   Partially addressable: 01 02 03 04 05 06 07 
04-15 17:09:33.442  1247  2337 I         :   Heap left redzone:       fa
04-15 17:09:33.442  1247  2337 I         :   Heap right redzone:      fb
04-15 17:09:33.442  1247  2337 I         :   Freed heap region:       fd
04-15 17:09:33.442  1247  2337 I         :   Stack left redzone:      f1
04-15 17:09:33.442  1247  2337 I         :   Stack mid redzone:       f2
04-15 17:09:33.442  1247  2337 I         :   Stack right redzone:     f3
04-15 17:09:33.442  1247  2337 I         :   Stack partial redzone:   f4
04-15 17:09:33.442  1247  2337 I         :   Stack after return:      f5
04-15 17:09:33.442  1247  2337 I         :   Stack use after scope:   f8
04-15 17:09:33.442  1247  2337 I         :   Global redzone:          f9
04-15 17:09:33.442  1247  2337 I         :   Global init order:       f6
04-15 17:09:33.442  1247  2337 I         :   Poisoned by user:        f7
04-15 17:09:33.442  1247  2337 I         :   Container overflow:      fc
04-15 17:09:33.442  1247  2337 I         :   Array cookie:            ac
04-15 17:09:33.442  1247  2337 I         :   Intra object redzone:    bb
04-15 17:09:33.442  1247  2337 I         :   ASan internal:           fe
04-15 17:09:33.442  1247  2337 I         :   Left alloca redzone:     ca
04-15 17:09:33.442  1247  2337 I         :   Right alloca redzone:    cb
04-15 17:09:33.442  1247  2337 I         : 
04-15 17:09:33.443  1247  2337 I         : ==1247==ABORTING
04-15 17:09:33.443  1247  2337 I         : 
04-15 17:09:33.461   385   385 I ServiceManager: service 'media.codec' died
04-15 17:09:33.461  2331  2336 E ACodec  : unexpected dir: Input(0) on output port
04-15 17:09:33.461  2331  2336 E ACodec  : [OMX.google.h264.decoder] Failed to get port format to send format change
04-15 17:09:33.461  2331  2336 E ACodec  : OMX/mediaserver died, signalling error!
04-15 17:09:33.461  2331  2336 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
04-15 17:09:33.462  2331  2335 E MediaCodec: Codec reported err 0xffffffe0, actionCode 0, while in state 6
04-15 17:09:33.560  2342  2342 I mediacodec: @@@ mediacodecservice starting
04-15 17:09:33.560  2342  2342 W         : No seccomp filter defined for this architecture.
04-15 17:09:33.852   475   497 E QC-QMI  : qmi_client [475]: unable to connect to server, errno=[2:No such file or directory], attempt=24
04-15 17:09:34.312  2319  2319 E QC-QMI  : qmi_client [2319]: unable to connect to server, errno=[2:No such file or directory], attempt=5
