Android libavc out of bound read

Test device
$ adb shell getprop ro.build.description
aosp_bullhead-userdebug 7.1.1 N4F26I eng.ffu.20170112.053429 test-keys

How to reproduce:
1) compile libavc with ASAN (edit Android.mk then do 'make libstagefright_soft_avcdec_32')
2) upload 1.mp4 to device
3) run stagefrigt binary to decode file
$ stagefright -s /mnt/sdcard/1.mp4

ASAN log:

04-10 13:19:30.949  1718  1847 I         : =================================================================
04-10 13:19:30.949  1718  1847 I         : 
04-10 13:19:30.949  1718  1847 I         : 
04-10 13:19:30.949  1718  1847 I         : ==1718==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xeb9181e4 at pc 0xeef55934 bp 0xeedfeea0 sp 0xeedfee98
04-10 13:19:30.949  1718  1847 I         : 
04-10 13:19:30.949  1718  1847 I         : 
04-10 13:19:30.949  1718  1847 I         : READ of size 2 at 0xeb9181e4 thread T2 (le.h264.decoder)
04-10 13:19:30.949  1718  1847 I         : 
04-10 13:19:31.014  1718  1847 I         :     #0 0xeef55933 in ih264d_mark_err_slice_skip /proc/self/cwd/external/libavc/decoder/ih264d_parse_pslice.c:1603:46
04-10 13:19:31.014  1718  1847 I         : 
04-10 13:19:31.016  1718  1847 I         :     #1 0xeef9cb63 in ih264d_parse_decode_slice /proc/self/cwd/external/libavc/decoder/ih264d_parse_slice.c:1391:15
04-10 13:19:31.016  1718  1847 I         : 
04-10 13:19:31.017  1718  1847 I         :     #2 0xeef7183b in ih264d_parse_nal_unit /proc/self/cwd/external/libavc/decoder/ih264d_parse_headers.c:1116:40
04-10 13:19:31.017  1718  1847 I         : 
04-10 13:19:31.020  1718  1847 I         :     #3 0xeef213a3 in ih264d_video_decode /proc/self/cwd/external/libavc/decoder/ih264d_api.c:2092:15
04-10 13:19:31.020  1718  1847 I         : 
04-10 13:19:31.020  1718  1847 I         :     #4 0xeef2a6af in ih264d_api_function /proc/self/cwd/external/libavc/decoder/ih264d_api.c:3680:26
04-10 13:19:31.020  1718  1847 I         : 
04-10 13:19:31.023  1718  1847 I         :     #5 0xeef1b7d5 in android::SoftAVC::onQueueFilled(unsigned int) /proc/self/cwd/frameworks/av/media/libstagefright/codecs/avcdec/SoftAVCDec.cpp:629:22
04-10 13:19:31.023  1718  1847 I         : 
04-10 13:19:31.026  1718  1847 I         :     #6 0xf184b161 in android::SimpleSoftOMXComponent::onMessageReceived(android::sp<android::AMessage> const&) (/system/lib/libstagefright_omx.so+0x23161)
04-10 13:19:31.026  1718  1847 I         : 
04-10 13:19:31.026  1718  1847 I         :     #7 0xf184c19b  (/system/lib/libstagefright_omx.so+0x2419b)
04-10 13:19:31.026  1718  1847 I         : 
04-10 13:19:31.028  1718  1847 I         :     #8 0xf15983d1 in android::AHandler::deliverMessage(android::sp<android::AMessage> const&) (/system/lib/libstagefright_foundation.so+0xf3d1)
04-10 13:19:31.028  1718  1847 I         : 
04-10 13:19:31.029  1718  1847 I         :     #9 0xf159a653 in android::AMessage::deliver() (/system/lib/libstagefright_foundation.so+0x11653)
04-10 13:19:31.029  1718  1847 I         : 
04-10 13:19:31.030  1718  1847 I         :     #10 0xf1598f3b in android::ALooper::loop() (/system/lib/libstagefright_foundation.so+0xff3b)
04-10 13:19:31.030  1718  1847 I         : 
04-10 13:19:31.031  1718  1847 I         :     #11 0xf16703c1 in android::Thread::_threadLoop(void*) (/system/lib/libutils.so+0xe3c1)
04-10 13:19:31.031  1718  1847 I         : 
04-10 13:19:31.039  1718  1847 I         :     #12 0xf18a3023 in __pthread_start(void*) (/system/lib/libc.so+0x47023)
04-10 13:19:31.039  1718  1847 I         : 
04-10 13:19:31.040  1718  1847 I         :     #13 0xf1875e3d in __start_thread (/system/lib/libc.so+0x19e3d)
04-10 13:19:31.040  1718  1847 I         : 
04-10 13:19:31.040  1718  1847 I         : 
04-10 13:19:31.040  1718  1847 I         : 
04-10 13:19:31.040  1718  1847 I         : 0xeb9181e4 is located 28 bytes to the left of 23760-byte region [0xeb918200,0xeb91ded0)
04-10 13:19:31.040  1718  1847 I         : 
04-10 13:19:31.040  1718  1847 I         : allocated by thread T2 (le.h264.decoder) here:
04-10 13:19:31.040  1718  1847 I         : 
04-10 13:19:31.045  1718  1847 I         :     #0 0xf10fc1ef in memalign (/system/lib/libclang_rt.asan-arm-android.so+0x751ef)
04-10 13:19:31.045  1718  1847 I         : 
04-10 13:19:31.047  1718  1847 I         :     #1 0xeef80857 in ih264d_allocate_dynamic_bufs /proc/self/cwd/external/libavc/decoder/ih264d_utils.c:1968:14
04-10 13:19:31.047  1718  1847 I         : 
04-10 13:19:31.047  1718  1847 I         :     #2 0xeef7ed8f in ih264d_init_pic /proc/self/cwd/external/libavc/decoder/ih264d_utils.c:812:15
04-10 13:19:31.047  1718  1847 I         : 
04-10 13:19:31.047  1718  1847 I         :     #3 0xeef9765f in ih264d_start_of_pic /proc/self/cwd/external/libavc/decoder/ih264d_parse_slice.c:338:11
04-10 13:19:31.047  1718  1847 I         : 
04-10 13:19:31.048  1718  1847 I         :     #4 0xeef9d6c3 in ih264d_parse_decode_slice /proc/self/cwd/external/libavc/decoder/ih264d_parse_slice.c:1587:19
04-10 13:19:31.048  1718  1847 I         : 
04-10 13:19:31.048  1718  1847 I         :     #5 0xeef7183b in ih264d_parse_nal_unit /proc/self/cwd/external/libavc/decoder/ih264d_parse_headers.c:1116:40
04-10 13:19:31.048  1718  1847 I         : 
04-10 13:19:31.048  1718  1847 I         :     #6 0xeef213a3 in ih264d_video_decode /proc/self/cwd/external/libavc/decoder/ih264d_api.c:2092:15
04-10 13:19:31.048  1718  1847 I         : 
04-10 13:19:31.049  1718  1847 I         :     #7 0xeef2a6af in ih264d_api_function /proc/self/cwd/external/libavc/decoder/ih264d_api.c:3680:26
04-10 13:19:31.049  1718  1847 I         : 
04-10 13:19:31.050  1718  1847 I         :     #8 0xeef1b7d5 in android::SoftAVC::onQueueFilled(unsigned int) /proc/self/cwd/frameworks/av/media/libstagefright/codecs/avcdec/SoftAVCDec.cpp:629:22
04-10 13:19:31.050  1718  1847 I         : 
04-10 13:19:31.050  1718  1847 I         : 
04-10 13:19:31.050  1718  1847 I         : 
04-10 13:19:31.050  1718  1847 I         : Thread T2 (le.h264.decoder) created by T1 (Binder:1718_1) here:
04-10 13:19:31.050  1718  1847 I         : 
04-10 13:19:31.050  1718  1847 I         :     #0 0xf10e34db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-10 13:19:31.050  1718  1847 I         : 
04-10 13:19:31.051  1718  1847 I         :     #1 0xf166fef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-10 13:19:31.051  1718  1847 I         : 
04-10 13:19:31.051  1718  1847 I         : 
04-10 13:19:31.051  1718  1847 I         : 
04-10 13:19:31.051  1718  1847 I         : Thread T1 (Binder:1718_1) created by T0 here:
04-10 13:19:31.051  1718  1847 I         : 
04-10 13:19:31.051  1718  1847 I         :     #0 0xf10e34db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-10 13:19:31.051  1718  1847 I         : 
04-10 13:19:31.051  1718  1847 I         :     #1 0xf166fef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-10 13:19:31.051  1718  1847 I         : 
04-10 13:19:31.052  1718  1847 I         :     #2 0xf1872c4d in __libc_init (/system/lib/libc.so+0x16c4d)
04-10 13:19:31.052  1718  1847 I         : 
04-10 13:19:31.053  1718  1847 I         :     #3 0xffffffff  (<unknown module>)
04-10 13:19:31.053  1718  1847 I         : 
04-10 13:19:31.053  1718  1847 I         : 
04-10 13:19:31.053  1718  1847 I         : 
04-10 13:19:31.054  1718  1847 I         : SUMMARY: AddressSanitizer: heap-buffer-overflow /proc/self/cwd/external/libavc/decoder/ih264d_parse_pslice.c:1603:46 in ih264d_mark_err_slice_skip
04-10 13:19:31.054  1718  1847 I         : 
04-10 13:19:31.055  1718  1847 I         : Shadow bytes around the buggy address:
04-10 13:19:31.055  1718  1847 I         :   0x1d722fe0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-10 13:19:31.055  1718  1847 I         :   0x1d722ff0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-10 13:19:31.055  1718  1847 I         :   0x1d723000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-10 13:19:31.055  1718  1847 I         :   0x1d723010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-10 13:19:31.055  1718  1847 I         :   0x1d723020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-10 13:19:31.055  1718  1847 I         : =>0x1d723030: fa fa fa fa fa fa fa fa fa fa fa fa[fa]fa fa fa
04-10 13:19:31.055  1718  1847 I         :   0x1d723040: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-10 13:19:31.055  1718  1847 I         :   0x1d723050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-10 13:19:31.055  1718  1847 I         :   0x1d723060: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-10 13:19:31.055  1718  1847 I         :   0x1d723070: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-10 13:19:31.055  1718  1847 I         :   0x1d723080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
04-10 13:19:31.055  1718  1847 I         : Shadow byte legend (one shadow byte represents 8 application bytes):
04-10 13:19:31.055  1718  1847 I         :   Addressable:           00
04-10 13:19:31.055  1718  1847 I         :   Partially addressable: 01 02 03 04 05 06 07 
04-10 13:19:31.055  1718  1847 I         :   Heap left redzone:       fa
04-10 13:19:31.055  1718  1847 I         :   Heap right redzone:      fb
04-10 13:19:31.055  1718  1847 I         :   Freed heap region:       fd
04-10 13:19:31.055  1718  1847 I         :   Stack left redzone:      f1
04-10 13:19:31.055  1718  1847 I         :   Stack mid redzone:       f2
04-10 13:19:31.055  1718  1847 I         :   Stack right redzone:     f3
04-10 13:19:31.055  1718  1847 I         :   Stack partial redzone:   f4
04-10 13:19:31.055  1718  1847 I         :   Stack after return:      f5
04-10 13:19:31.055  1718  1847 I         :   Stack use after scope:   f8
04-10 13:19:31.055  1718  1847 I         :   Global redzone:          f9
04-10 13:19:31.055  1718  1847 I         :   Global init order:       f6
04-10 13:19:31.055  1718  1847 I         :   Poisoned by user:        f7
04-10 13:19:31.055  1718  1847 I         :   Container overflow:      fc
04-10 13:19:31.055  1718  1847 I         :   Array cookie:            ac
04-10 13:19:31.055  1718  1847 I         :   Intra object redzone:    bb
04-10 13:19:31.055  1718  1847 I         :   ASan internal:           fe
04-10 13:19:31.055  1718  1847 I         :   Left alloca redzone:     ca
04-10 13:19:31.056  1718  1847 I         :   Right alloca redzone:    cb
04-10 13:19:31.056  1718  1847 I         : 
04-10 13:19:31.056  1718  1847 I         : ==1718==ABORTING
04-10 13:19:31.056  1718  1847 I         : 
04-10 13:19:31.063   386   386 I ServiceManager: service 'media.codec' died
04-10 13:19:31.063  1842  1846 E ACodec  : OMX/mediaserver died, signalling error!
04-10 13:19:31.063  1842  1846 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
