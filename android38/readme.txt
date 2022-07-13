Android libavc out of bounds read

Test device
$ adb shell getprop ro.build.description
aosp_bullhead-userdebug 7.1.1 N4F26I eng.ffu.20170112.053429 test-keys

How to reproduce:
1) compile libavc with ASAN (edit Android.mk then do 'make libstagefright_soft_avcdec_32')
2) upload 1.mp4 to device
3) run stagefrigt binary to decode file
$ stagefright -s /mnt/sdcard/1.mp4

ASAN log:

AddressSanitizer: heap-buffer-overflow on address 0xec31dfb5 at pc 0xedd721a0 bp 0xed3fedb8 sp 0xed3fedb0
04-15 14:07:21.897 28107 28375 I         : 
04-15 14:07:21.897 28107 28375 I         : 
04-15 14:07:21.898 28107 28375 I         : READ of size 1 at 0xec31dfb5 thread T64 (le.h264.decoder)
04-15 14:07:21.898 28107 28375 I         : 
04-15 14:07:21.956 28107 28375 I         :     #0 0xedd7219f in ih264d_get_mb_info_cavlc_nonmbaff /proc/self/cwd/external/libavc/decoder/ih264d_mb_utils.c:159:64
04-15 14:07:21.956 28107 28375 I         : 
04-15 14:07:21.957 28107 28375 I         :     #1 0xedd59fbb in ih264d_parse_islice_data_cavlc /proc/self/cwd/external/libavc/decoder/ih264d_parse_islice.c:804:9
04-15 14:07:21.957 28107 28375 I         : 
04-15 14:07:21.957 28107 28375 I         :     #2 0xedd5cd8f in ih264d_parse_islice /proc/self/cwd/external/libavc/decoder/ih264d_parse_islice.c:1476:15
04-15 14:07:21.957 28107 28375 I         : 
04-15 14:07:21.958 28107 28375 I         :     #3 0xedd9e5bb in ih264d_parse_decode_slice /proc/self/cwd/external/libavc/decoder/ih264d_parse_slice.c:1885:15
04-15 14:07:21.958 28107 28375 I         : 
04-15 14:07:21.959 28107 28375 I         :     #4 0xedd7183b in ih264d_parse_nal_unit /proc/self/cwd/external/libavc/decoder/ih264d_parse_headers.c:1116:40
04-15 14:07:21.959 28107 28375 I         : 
04-15 14:07:21.960 28107 28375 I         :     #5 0xedd213a3 in ih264d_video_decode /proc/self/cwd/external/libavc/decoder/ih264d_api.c:2092:15
04-15 14:07:21.960 28107 28375 I         : 
04-15 14:07:21.960 28107 28375 I         :     #6 0xedd2a6af in ih264d_api_function /proc/self/cwd/external/libavc/decoder/ih264d_api.c:3680:26
04-15 14:07:21.960 28107 28375 I         : 
04-15 14:07:21.961 28107 28375 I         :     #7 0xedd1b7d5 in android::SoftAVC::onQueueFilled(unsigned int) /proc/self/cwd/frameworks/av/media/libstagefright/codecs/avcdec/SoftAVCDec.cpp:629:22
04-15 14:07:21.961 28107 28375 I         : 
04-15 14:07:21.963 28107 28375 I         :     #8 0xefbad161 in android::SimpleSoftOMXComponent::onMessageReceived(android::sp<android::AMessage> const&) (/system/lib/libstagefright_omx.so+0x23161)
04-15 14:07:21.963 28107 28375 I         : 
04-15 14:07:21.963 28107 28375 I         :     #9 0xefbae19b  (/system/lib/libstagefright_omx.so+0x2419b)
04-15 14:07:21.963 28107 28375 I         : 
04-15 14:07:21.964 28107 28375 I         :     #10 0xf004c3d1 in android::AHandler::deliverMessage(android::sp<android::AMessage> const&) (/system/lib/libstagefright_foundation.so+0xf3d1)
04-15 14:07:21.964 28107 28375 I         : 
04-15 14:07:21.964 28107 28375 I         :     #11 0xf004e653 in android::AMessage::deliver() (/system/lib/libstagefright_foundation.so+0x11653)
04-15 14:07:21.964 28107 28375 I         : 
04-15 14:07:21.964 28107 28375 I         :     #12 0xf004cf3b in android::ALooper::loop() (/system/lib/libstagefright_foundation.so+0xff3b)
04-15 14:07:21.964 28107 28375 I         : 
04-15 14:07:21.965 28107 28375 I         :     #13 0xf07263c1 in android::Thread::_threadLoop(void*) (/system/lib/libutils.so+0xe3c1)
04-15 14:07:21.965 28107 28375 I         : 
04-15 14:07:21.969 28107 28375 I         :     #14 0xf06cd023 in __pthread_start(void*) (/system/lib/libc.so+0x47023)
04-15 14:07:21.969 28107 28375 I         : 
04-15 14:07:21.969 28107 28375 I         :     #15 0xf069fe3d in __start_thread (/system/lib/libc.so+0x19e3d)
04-15 14:07:21.969 28107 28375 I         : 
04-15 14:07:21.969 28107 28375 I         : 
04-15 14:07:21.969 28107 28375 I         : 
04-15 14:07:21.970 28107 28375 I         : 0xec31dfb5 is located 101 bytes to the right of 720-byte region [0xec31dc80,0xec31df50)
04-15 14:07:21.970 28107 28375 I         : 
04-15 14:07:21.970 28107 28375 I         : allocated by thread T64 (le.h264.decoder) here:
04-15 14:07:21.970 28107 28375 I         : 
04-15 14:07:21.971 28107 28375 I         :     #0 0xf01931ef in memalign (/system/lib/libclang_rt.asan-arm-android.so+0x751ef)
04-15 14:07:21.971 28107 28375 I         : 
04-15 14:07:21.972 28107 28375 I         :     #1 0xedd8079f in ih264d_allocate_dynamic_bufs /proc/self/cwd/external/libavc/decoder/ih264d_utils.c:1951:14
04-15 14:07:21.972 28107 28375 I         : 
04-15 14:07:21.972 28107 28375 I         :     #2 0xedd7ed8f in ih264d_init_pic /proc/self/cwd/external/libavc/decoder/ih264d_utils.c:812:15
04-15 14:07:21.972 28107 28375 I         : 
04-15 14:07:21.973 28107 28375 I         :     #3 0xedd9765f in ih264d_start_of_pic /proc/self/cwd/external/libavc/decoder/ih264d_parse_slice.c:338:11
04-15 14:07:21.973 28107 28375 I         : 
04-15 14:07:21.973 28107 28375 I         :     #4 0xedd9d6c3 in ih264d_parse_decode_slice /proc/self/cwd/external/libavc/decoder/ih264d_parse_slice.c:1587:19
04-15 14:07:21.973 28107 28375 I         : 
04-15 14:07:21.973 28107 28375 I         :     #5 0xedd7183b in ih264d_parse_nal_unit /proc/self/cwd/external/libavc/decoder/ih264d_parse_headers.c:1116:40
04-15 14:07:21.973 28107 28375 I         : 
04-15 14:07:21.973 28107 28375 I         :     #6 0xedd213a3 in ih264d_video_decode /proc/self/cwd/external/libavc/decoder/ih264d_api.c:2092:15
04-15 14:07:21.973 28107 28375 I         : 
04-15 14:07:21.974 28107 28375 I         :     #7 0xedd2a6af in ih264d_api_function /proc/self/cwd/external/libavc/decoder/ih264d_api.c:3680:26
04-15 14:07:21.974 28107 28375 I         : 
04-15 14:07:21.974 28107 28375 I         :     #8 0xedd1b7d5 in android::SoftAVC::onQueueFilled(unsigned int) /proc/self/cwd/frameworks/av/media/libstagefright/codecs/avcdec/SoftAVCDec.cpp:629:22
04-15 14:07:21.974 28107 28375 I         : 
04-15 14:07:21.974 28107 28375 I         : 
04-15 14:07:21.974 28107 28375 I         : 
04-15 14:07:21.974 28107 28375 I         : Thread T64 (le.h264.decoder) created by T5 (Binder:28107_3) here:
04-15 14:07:21.974 28107 28375 I         : 
04-15 14:07:21.974 28107 28375 I         :     #0 0xf017a4db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-15 14:07:21.975 28107 28375 I         : 
04-15 14:07:21.975 28107 28375 I         :     #1 0xf0725ef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-15 14:07:21.975 28107 28375 I         : 
04-15 14:07:21.975 28107 28375 I         : 
04-15 14:07:21.975 28107 28375 I         : 
04-15 14:07:21.975 28107 28375 I         : Thread T5 (Binder:28107_3) created by T4 (Binder:28107_2) here:
04-15 14:07:21.975 28107 28375 I         : 
04-15 14:07:21.975 28107 28375 I         :     #0 0xf017a4db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-15 14:07:21.975 28107 28375 I         : 
04-15 14:07:21.975 28107 28375 I         :     #1 0xf0725ef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-15 14:07:21.975 28107 28375 I         : 
04-15 14:07:21.975 28107 28375 I         : 
04-15 14:07:21.975 28107 28375 I         : 
04-15 14:07:21.975 28107 28375 I         : Thread T4 (Binder:28107_2) created by T0 here:
04-15 14:07:21.975 28107 28375 I         : 
04-15 14:07:21.976 28107 28375 I         :     #0 0xf017a4db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-15 14:07:21.976 28107 28375 I         : 
04-15 14:07:21.976 28107 28375 I         :     #1 0xf0725ef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-15 14:07:21.976 28107 28375 I         : 
04-15 14:07:21.976 28107 28375 I         :     #2 0xf069cc4d in __libc_init (/system/lib/libc.so+0x16c4d)
04-15 14:07:21.976 28107 28375 I         : 
04-15 14:07:21.977 28107 28375 I         :     #3 0xffffffff  (<unknown module>)
04-15 14:07:21.977 28107 28375 I         : 
04-15 14:07:21.977 28107 28375 I         : 
04-15 14:07:21.977 28107 28375 I         : 
04-15 14:07:21.977 28107 28375 I         : SUMMARY: AddressSanitizer: heap-buffer-overflow /proc/self/cwd/external/libavc/decoder/ih264d_mb_utils.c:159:64 in ih264d_get_mb_info_cavlc_nonmbaff
04-15 14:07:21.977 28107 28375 I         : 
04-15 14:07:21.977 28107 28375 I         : Shadow bytes around the buggy address:
04-15 14:07:21.977 28107 28375 I         :   0x1d863ba0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-15 14:07:21.977 28107 28375 I         :   0x1d863bb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-15 14:07:21.977 28107 28375 I         :   0x1d863bc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-15 14:07:21.977 28107 28375 I         :   0x1d863bd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-15 14:07:21.978 28107 28375 I         :   0x1d863be0: 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa
04-15 14:07:21.978 28107 28375 I         : =>0x1d863bf0: fa fa fa fa fa fa[fa]fa fa fa fa fa fa fa fa fa
04-15 14:07:21.978 28107 28375 I         :   0x1d863c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 14:07:21.978 28107 28375 I         :   0x1d863c10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 14:07:21.978 28107 28375 I         :   0x1d863c20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 14:07:21.978 28107 28375 I         :   0x1d863c30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 14:07:21.978 28107 28375 I         :   0x1d863c40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 14:07:21.978 28107 28375 I         : Shadow byte legend (one shadow byte represents 8 application bytes):
04-15 14:07:21.978 28107 28375 I         :   Addressable:           00
04-15 14:07:21.978 28107 28375 I         :   Partially addressable: 01 02 03 04 05 06 07 
04-15 14:07:21.978 28107 28375 I         :   Heap left redzone:       fa
04-15 14:07:21.978 28107 28375 I         :   Heap right redzone:      fb
04-15 14:07:21.978 28107 28375 I         :   Freed heap region:       fd
04-15 14:07:21.978 28107 28375 I         :   Stack left redzone:      f1
04-15 14:07:21.978 28107 28375 I         :   Stack mid redzone:       f2
04-15 14:07:21.978 28107 28375 I         :   Stack right redzone:     f3
04-15 14:07:21.978 28107 28375 I         :   Stack partial redzone:   f4
04-15 14:07:21.978 28107 28375 I         :   Stack after return:      f5
04-15 14:07:21.978 28107 28375 I         :   Stack use after scope:   f8
04-15 14:07:21.978 28107 28375 I         :   Global redzone:          f9
04-15 14:07:21.978 28107 28375 I         :   Global init order:       f6
04-15 14:07:21.978 28107 28375 I         :   Poisoned by user:        f7
04-15 14:07:21.978 28107 28375 I         :   Container overflow:      fc
04-15 14:07:21.978 28107 28375 I         :   Array cookie:            ac
04-15 14:07:21.978 28107 28375 I         :   Intra object redzone:    bb
04-15 14:07:21.978 28107 28375 I         :   ASan internal:           fe
04-15 14:07:21.978 28107 28375 I         :   Left alloca redzone:     ca
04-15 14:07:21.978 28107 28375 I         :   Right alloca redzone:    cb
04-15 14:07:21.978 28107 28375 I         : 
04-15 14:07:21.978 28107 28375 I         : ==28107==ABORTING
04-15 14:07:21.978 28107 28375 I         : 
04-15 14:07:21.990   385   385 I ServiceManager: service 'media.codec' died
04-15 14:07:21.990 28369 28374 E ACodec  : unexpected dir: Input(0) on output port
04-15 14:07:21.990 28369 28374 E ACodec  : [OMX.google.h264.decoder] Failed to get port format to send format change
04-15 14:07:21.991 28369 28374 E ACodec  : OMX/mediaserver died, signalling error!
04-15 14:07:21.991 28369 28374 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
04-15 14:07:21.991 28369 28373 E MediaCodec: Codec reported err 0xffffffe0, actionCode 0, while in state 6
04-15 14:07:22.085 28380 28380 I mediacodec: @@@ mediacodecservice starting
04-15 14:07:22.085 28380 28380 W         : No seccomp filter defined for this architecture.
04-15 14:07:22.151 28314 28314 E QC-QMI  : qmi_client [28314]: unable to connect to server, errno=[2:No such file or directory], attempt=7
04-15 14:07:22.833   475   497 E QC-QMI  : qmi_client [475]: unable to connect to server, errno=[2:No such file or directory], attempt=42
