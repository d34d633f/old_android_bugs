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


AddressSanitizer: heap-use-after-free on address 0xe9bea800 at pc 0xefa8fe0c bp 0xeecfe978 sp 0xeecfe970
04-15 16:17:25.883  4663  5093 I         : 
04-15 16:17:25.883  4663  5093 I         : 
04-15 16:17:25.883  4663  5093 I         : READ of size 1 at 0xe9bea800 thread T104 (le.h264.decoder)
04-15 16:17:25.883  4663  5093 I         : 
04-15 16:17:25.952  4663  5093 I         :     #0 0xefa8fe0b in ih264d_one_to_one /proc/self/cwd/external/libavc/decoder/ih264d_process_bslice.c:1601:27
04-15 16:17:25.952  4663  5093 I         : 
04-15 16:17:25.952  4663  5093 I         :     #1 0xefa87d2b in ih264d_decode_spatial_direct /proc/self/cwd/external/libavc/decoder/ih264d_process_bslice.c:220:5
04-15 16:17:25.952  4663  5093 I         : 
04-15 16:17:25.954  4663  5093 I         :     #2 0xefadc637 in ih264d_mv_pred_ref_tfr_nby2_bmb /proc/self/cwd/external/libavc/decoder/ih264d_parse_bslice.c:1025:27
04-15 16:17:25.954  4663  5093 I         : 
04-15 16:17:25.955  4663  5093 I         :     #3 0xefa515c7 in ih264d_parse_inter_slice_data_cabac /proc/self/cwd/external/libavc/decoder/ih264d_parse_pslice.c:1045:13
04-15 16:17:25.955  4663  5093 I         : 
04-15 16:17:25.957  4663  5093 I         :     #4 0xefa9e6e7 in ih264d_parse_decode_slice /proc/self/cwd/external/libavc/decoder/ih264d_parse_slice.c:1902:15
04-15 16:17:25.957  4663  5093 I         : 
04-15 16:17:25.958  4663  5093 I         :     #5 0xefa7183b in ih264d_parse_nal_unit /proc/self/cwd/external/libavc/decoder/ih264d_parse_headers.c:1116:40
04-15 16:17:25.958  4663  5093 I         : 
04-15 16:17:25.960  4663  5093 I         :     #6 0xefa213a3 in ih264d_video_decode /proc/self/cwd/external/libavc/decoder/ih264d_api.c:2092:15
04-15 16:17:25.960  4663  5093 I         : 
04-15 16:17:25.960  4663  5093 I         :     #7 0xefa2a6af in ih264d_api_function /proc/self/cwd/external/libavc/decoder/ih264d_api.c:3680:26
04-15 16:17:25.960  4663  5093 I         : 
04-15 16:17:25.963  4663  5093 I         :     #8 0xefa1b7d5 in android::SoftAVC::onQueueFilled(unsigned int) /proc/self/cwd/frameworks/av/media/libstagefright/codecs/avcdec/SoftAVCDec.cpp:629:22
04-15 16:17:25.963  4663  5093 I         : 
04-15 16:17:25.965  4663  5093 I         :     #9 0xf201a161 in android::SimpleSoftOMXComponent::onMessageReceived(android::sp<android::AMessage> const&) (/system/lib/libstagefright_omx.so+0x23161)
04-15 16:17:25.965  4663  5093 I         : 
04-15 16:17:25.965  4663  5093 I         :     #10 0xf201b19b  (/system/lib/libstagefright_omx.so+0x2419b)
04-15 16:17:25.965  4663  5093 I         : 
04-15 16:17:25.967  4663  5093 I         :     #11 0xf29d43d1 in android::AHandler::deliverMessage(android::sp<android::AMessage> const&) (/system/lib/libstagefright_foundation.so+0xf3d1)
04-15 16:17:25.967  4663  5093 I         : 
04-15 16:17:25.967  4663  5093 I         :     #12 0xf29d6653 in android::AMessage::deliver() (/system/lib/libstagefright_foundation.so+0x11653)
04-15 16:17:25.967  4663  5093 I         : 
04-15 16:17:25.968  4663  5093 I         :     #13 0xf29d4f3b in android::ALooper::loop() (/system/lib/libstagefright_foundation.so+0xff3b)
04-15 16:17:25.968  4663  5093 I         : 
04-15 16:17:25.969  4663  5093 I         :     #14 0xf29f73c1 in android::Thread::_threadLoop(void*) (/system/lib/libutils.so+0xe3c1)
04-15 16:17:25.969  4663  5093 I         : 
04-15 16:17:25.977  4663  5093 I         :     #15 0xf22ec023 in __pthread_start(void*) (/system/lib/libc.so+0x47023)
04-15 16:17:25.977  4663  5093 I         : 
04-15 16:17:25.977  4663  5093 I         :     #16 0xf22bee3d in __start_thread (/system/lib/libc.so+0x19e3d)
04-15 16:17:25.977  4663  5093 I         : 
04-15 16:17:25.977  4663  5093 I         : 
04-15 16:17:25.977  4663  5093 I         : 
04-15 16:17:25.978  4663  5093 I         : 0xe9bea800 is located 0 bytes inside of 1681920-byte region [0xe9bea800,0xe9d85200)
04-15 16:17:25.978  4663  5093 I         : 
04-15 16:17:25.978  4663  5093 I         : freed by thread T104 (le.h264.decoder) here:
04-15 16:17:25.978  4663  5093 I         : 
04-15 16:17:25.981  4663  5093 I         :     #0 0xf253790f in __interceptor_free (/system/lib/libclang_rt.asan-arm-android.so+0x7490f)
04-15 16:17:25.981  4663  5093 I         : 
04-15 16:17:25.982  4663  5093 I         :     #1 0xefa823e3 in ih264d_free_dynamic_bufs /proc/self/cwd/external/libavc/decoder/ih264d_utils.c:2226:5
04-15 16:17:25.983  4663  5093 I         : 
04-15 16:17:25.983  4663  5093 I         :     #2 0xefa1c2bb in ih264d_init_decoder /proc/self/cwd/external/libavc/decoder/ih264d_api.c:964:5
04-15 16:17:25.983  4663  5093 I         : 
04-15 16:17:25.983  4663  5093 I         :     #3 0xefa2751b in ih264d_reset /proc/self/cwd/external/libavc/decoder/ih264d_api.c:3176:9
04-15 16:17:25.983  4663  5093 I         : 
04-15 16:17:25.983  4663  5093 I         :     #4 0xefa2751b in ih264d_ctl /proc/self/cwd/external/libavc/decoder/ih264d_api.c:3237
04-15 16:17:25.983  4663  5093 I         : 
04-15 16:17:25.984  4663  5093 I         :     #5 0xefa2a2cb in ih264d_api_function /proc/self/cwd/external/libavc/decoder/ih264d_api.c:3702:26
04-15 16:17:25.984  4663  5093 I         : 
04-15 16:17:25.984  4663  5093 I         :     #6 0xefa1afff in android::SoftAVC::resetDecoder() /proc/self/cwd/frameworks/av/media/libstagefright/codecs/avcdec/SoftAVCDec.cpp:238:14
04-15 16:17:25.984  4663  5093 I         : 
04-15 16:17:25.984  4663  5093 I         : 
04-15 16:17:25.984  4663  5093 I         : 
04-15 16:17:25.985  4663  5093 I         : previously allocated by thread T104 (le.h264.decoder) here:
04-15 16:17:25.985  4663  5093 I         : 
04-15 16:17:25.985  4663  5093 I         :     #0 0xf25381ef in memalign (/system/lib/libclang_rt.asan-arm-android.so+0x751ef)
04-15 16:17:25.985  4663  5093 I         : 
04-15 16:17:25.985  4663  5093 I         :     #1 0xefa80b9b in ih264d_allocate_dynamic_bufs /proc/self/cwd/external/libavc/decoder/ih264d_utils.c:2041:18
04-15 16:17:25.985  4663  5093 I         : 
04-15 16:17:25.985  4663  5093 I         :     #2 0xefa7ed8f in ih264d_init_pic /proc/self/cwd/external/libavc/decoder/ih264d_utils.c:812:15
04-15 16:17:25.985  4663  5093 I         : 
04-15 16:17:25.986  4663  5093 I         :     #3 0xefa9765f in ih264d_start_of_pic /proc/self/cwd/external/libavc/decoder/ih264d_parse_slice.c:338:11
04-15 16:17:25.986  4663  5093 I         : 
04-15 16:17:25.986  4663  5093 I         :     #4 0xefa9d6c3 in ih264d_parse_decode_slice /proc/self/cwd/external/libavc/decoder/ih264d_parse_slice.c:1587:19
04-15 16:17:25.986  4663  5093 I         : 
04-15 16:17:25.987  4663  5093 I         :     #5 0xefa7183b in ih264d_parse_nal_unit /proc/self/cwd/external/libavc/decoder/ih264d_parse_headers.c:1116:40
04-15 16:17:25.987  4663  5093 I         : 
04-15 16:17:25.987  4663  5093 I         :     #6 0xefa213a3 in ih264d_video_decode /proc/self/cwd/external/libavc/decoder/ih264d_api.c:2092:15
04-15 16:17:25.987  4663  5093 I         : 
04-15 16:17:25.987  4663  5093 I         :     #7 0xefa2a6af in ih264d_api_function /proc/self/cwd/external/libavc/decoder/ih264d_api.c:3680:26
04-15 16:17:25.987  4663  5093 I         : 
04-15 16:17:25.988  4663  5093 I         :     #8 0xefa1b7d5 in android::SoftAVC::onQueueFilled(unsigned int) /proc/self/cwd/frameworks/av/media/libstagefright/codecs/avcdec/SoftAVCDec.cpp:629:22
04-15 16:17:25.988  4663  5093 I         : 
04-15 16:17:25.988  4663  5093 I         : 
04-15 16:17:25.988  4663  5093 I         : 
04-15 16:17:25.988  4663  5093 I         : Thread T104 (le.h264.decoder) created by T20 (Binder:4663_6) here:
04-15 16:17:25.988  4663  5093 I         : 
04-15 16:17:25.988  4663  5093 I         :     #0 0xf251f4db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-15 16:17:25.988  4663  5093 I         : 
04-15 16:17:25.989  4663  5093 I         :     #1 0xf29f6ef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-15 16:17:25.989  4663  5093 I         : 
04-15 16:17:25.989  4663  5093 I         : 
04-15 16:17:25.989  4663  5093 I         : 
04-15 16:17:25.989  4663  5093 I         : Thread T20 (Binder:4663_6) created by T5 (Binder:4663_3) here:
04-15 16:17:25.989  4663  5093 I         : 
04-15 16:17:25.989  4663  5093 I         :     #0 0xf251f4db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-15 16:17:25.989  4663  5093 I         : 
04-15 16:17:25.989  4663  5093 I         :     #1 0xf29f6ef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-15 16:17:25.990  4663  5093 I         : 
04-15 16:17:25.990  4663  5093 I         : 
04-15 16:17:25.990  4663  5093 I         : 
04-15 16:17:25.990  4663  5093 I         : Thread T5 (Binder:4663_3) created by T0 here:
04-15 16:17:25.990  4663  5093 I         : 
04-15 16:17:25.990  4663  5093 I         :     #0 0xf251f4db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-15 16:17:25.990  4663  5093 I         : 
04-15 16:17:25.990  4663  5093 I         :     #1 0xf29f6ef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-15 16:17:25.990  4663  5093 I         : 
04-15 16:17:25.991  4663  5093 I         :     #2 0xf22bbc4d in __libc_init (/system/lib/libc.so+0x16c4d)
04-15 16:17:25.991  4663  5093 I         : 
04-15 16:17:25.991  4663  5093 I         :     #3 0xffffffff  (<unknown module>)
04-15 16:17:25.991  4663  5093 I         : 
04-15 16:17:25.992  4663  5093 I         : 
04-15 16:17:25.992  4663  5093 I         : 
04-15 16:17:25.992  4663  5093 I         : SUMMARY: AddressSanitizer: heap-use-after-free /proc/self/cwd/external/libavc/decoder/ih264d_process_bslice.c:1601:27 in ih264d_one_to_one
04-15 16:17:25.992  4663  5093 I         : 
04-15 16:17:25.993  4663  5093 I         : Shadow bytes around the buggy address:
04-15 16:17:25.993  4663  5093 I         :   0x1d37d4b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 16:17:25.993  4663  5093 I         :   0x1d37d4c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 16:17:25.993  4663  5093 I         :   0x1d37d4d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 16:17:25.993  4663  5093 I         :   0x1d37d4e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 16:17:25.993  4663  5093 I         :   0x1d37d4f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-15 16:17:25.993  4663  5093 I         : =>0x1d37d500:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
04-15 16:17:25.993  4663  5093 I         :   0x1d37d510: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
04-15 16:17:25.993  4663  5093 I         :   0x1d37d520: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
04-15 16:17:25.993  4663  5093 I         :   0x1d37d530: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
04-15 16:17:25.993  4663  5093 I         :   0x1d37d540: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
04-15 16:17:25.993  4663  5093 I         :   0x1d37d550: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
04-15 16:17:25.993  4663  5093 I         : Shadow byte legend (one shadow byte represents 8 application bytes):
04-15 16:17:25.993  4663  5093 I         :   Addressable:           00
04-15 16:17:25.993  4663  5093 I         :   Partially addressable: 01 02 03 04 05 06 07 
04-15 16:17:25.993  4663  5093 I         :   Heap left redzone:       fa
04-15 16:17:25.993  4663  5093 I         :   Heap right redzone:      fb
04-15 16:17:25.993  4663  5093 I         :   Freed heap region:       fd
04-15 16:17:25.993  4663  5093 I         :   Stack left redzone:      f1
04-15 16:17:25.993  4663  5093 I         :   Stack mid redzone:       f2
04-15 16:17:25.993  4663  5093 I         :   Stack right redzone:     f3
04-15 16:17:25.993  4663  5093 I         :   Stack partial redzone:   f4
04-15 16:17:25.993  4663  5093 I         :   Stack after return:      f5
04-15 16:17:25.993  4663  5093 I         :   Stack use after scope:   f8
04-15 16:17:25.993  4663  5093 I         :   Global redzone:          f9
04-15 16:17:25.993  4663  5093 I         :   Global init order:       f6
04-15 16:17:25.993  4663  5093 I         :   Poisoned by user:        f7
04-15 16:17:25.993  4663  5093 I         :   Container overflow:      fc
04-15 16:17:25.993  4663  5093 I         :   Array cookie:            ac
04-15 16:17:25.993  4663  5093 I         :   Intra object redzone:    bb
04-15 16:17:25.993  4663  5093 I         :   ASan internal:           fe
04-15 16:17:25.993  4663  5093 I         :   Left alloca redzone:     ca
04-15 16:17:25.993  4663  5093 I         :   Right alloca redzone:    cb
04-15 16:17:25.993  4663  5093 I         : 
04-15 16:17:25.994  4663  5093 I         : ==4663==ABORTING
04-15 16:17:25.994  4663  5093 I         : 
04-15 16:17:26.008   385   385 I ServiceManager: service 'media.codec' died
04-15 16:17:26.008  5087  5092 E ACodec  : unexpected dir: Input(0) on output port
04-15 16:17:26.008  5087  5092 E ACodec  : [OMX.google.h264.decoder] Failed to get port format to send format change
04-15 16:17:26.008  5087  5092 E ACodec  : OMX/mediaserver died, signalling error!
04-15 16:17:26.008  5087  5092 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
04-15 16:17:26.009  5087  5091 E MediaCodec: Codec reported err 0xffffffe0, actionCode 0, while in state 6
04-15 16:17:26.112  5100  5100 I mediacodec: @@@ mediacodecservice starting
04-15 16:17:26.112  5100  5100 W         : No seccomp filter defined for this architecture.
04-15 16:17:26.122   475   497 E QC-QMI  : qmi_client [475]: unable to connect to server, errno=[2:No such file or directory], attempt=26
04-15 16:17:26.209  4508  4508 E QC-QMI  : qmi_client [4508]: unable to connect to server after 60 tries... giving up
04-15 16:17:26.209  4508  4508 E QC-QMI  : qmi_qmux_if_pwr_up_init_ex:  Initialization failed, rc = -1
04-15 16:17:26.264  5102  5102 E QC-QMI  : qmi_client [5102]: unable to connect to server, errno=[2:No such file or directory], attempt=1
