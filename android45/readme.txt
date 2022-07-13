Android libhevc out of bounds read

Test device
$ adb shell getprop ro.build.description
aosp_bullhead-userdebug 7.1.1 N4F26I eng.ffu.20170112.053429 test-keys


How to test:
1) compile libhevc with ASAN, also compile stagefright binary

2) copy mp4 file to device
$ adb push 1.mp4 /data/local/tmp

3) run stagefright decoder:
<phone>$ stagefright -s /data/local/tmp/1.mp4

ASAN log:


04-21 15:03:04.228  5242  9677 I         : =================================================================
04-21 15:03:04.228  5242  9677 I         : 
04-21 15:03:04.229  5242  9677 I         : 
04-21 15:03:04.229  5242  9677 I         : ==5242==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xe8d00928 at pc 0xec4209b8 bp 0xeb8ff0f0 sp 0xeb8ff0e8
04-21 15:03:04.229  5242  9677 I         : 
04-21 15:03:04.229  5242  9677 I         : 
04-21 15:03:04.229  5242  9677 I         : READ of size 4 at 0xe8d00928 thread T120 (le.hevc.decoder)
04-21 15:03:04.229  5242  9677 I         : 
04-21 15:03:04.304  5242  9677 I         :     #0 0xec4209b7 in ihevcd_parse_slice_header /proc/self/cwd/external/libhevc/decoder/ihevcd_parse_slice_header.c:885:52
04-21 15:03:04.304  5242  9677 I         : 
04-21 15:03:04.305  5242  9677 I         :     #1 0xec411ba3 in ihevcd_nal_unit /proc/self/cwd/external/libhevc/decoder/ihevcd_nal.c:398:19
04-21 15:03:04.305  5242  9677 I         : 
04-21 15:03:04.305  5242  9677 I         :     #2 0xec40de63 in ihevcd_decode /proc/self/cwd/external/libhevc/decoder/ihevcd_decode.c:604:15
04-21 15:03:04.305  5242  9677 I         : 
04-21 15:03:04.306  5242  9677 I         :     #3 0xec40c497 in ihevcd_cxa_api_function /proc/self/cwd/external/libhevc/decoder/ihevcd_api.c:3552:19
04-21 15:03:04.306  5242  9677 I         : 
04-21 15:03:04.308  5242  9677 I         :     #4 0xec3f9f09 in android::SoftHEVC::onQueueFilled(unsigned int) /proc/self/cwd/frameworks/av/media/libstagefright/codecs/hevcdec/SoftHEVC.cpp:576:22
04-21 15:03:04.308  5242  9677 I         : 
04-21 15:03:04.309  5242  9677 I         :     #5 0xf0749161 in android::SimpleSoftOMXComponent::onMessageReceived(android::sp<android::AMessage> const&) (/system/lib/libstagefright_omx.so+0x23161)
04-21 15:03:04.309  5242  9677 I         : 
04-21 15:03:04.309  5242  9677 I         :     #6 0xf074a19b  (/system/lib/libstagefright_omx.so+0x2419b)
04-21 15:03:04.309  5242  9677 I         : 
04-21 15:03:04.311  5242  9677 I         :     #7 0xf036a3d1 in android::AHandler::deliverMessage(android::sp<android::AMessage> const&) (/system/lib/libstagefright_foundation.so+0xf3d1)
04-21 15:03:04.311  5242  9677 I         : 
04-21 15:03:04.311  5242  9677 I         :     #8 0xf036c653 in android::AMessage::deliver() (/system/lib/libstagefright_foundation.so+0x11653)
04-21 15:03:04.311  5242  9677 I         : 
04-21 15:03:04.311  5242  9677 I         :     #9 0xf036af3b in android::ALooper::loop() (/system/lib/libstagefright_foundation.so+0xff3b)
04-21 15:03:04.311  5242  9677 I         : 
04-21 15:03:04.312  5242  9677 I         :     #10 0xefc2f3c1 in android::Thread::_threadLoop(void*) (/system/lib/libutils.so+0xe3c1)
04-21 15:03:04.312  5242  9677 I         : 
04-21 15:03:04.316  5242  9677 I         :     #11 0xf03e0023 in __pthread_start(void*) (/system/lib/libc.so+0x47023)
04-21 15:03:04.316  5242  9677 I         : 
04-21 15:03:04.316  5242  9677 I         :     #12 0xf03b2e3d in __start_thread (/system/lib/libc.so+0x19e3d)
04-21 15:03:04.316  5242  9677 I         : 
04-21 15:03:04.316  5242  9677 I         : 
04-21 15:03:04.316  5242  9677 I         : 
04-21 15:03:04.317  5242  9677 I         : AddressSanitizer can not describe address in more detail (wild memory access suspected).
04-21 15:03:04.317  5242  9677 I         : 
04-21 15:03:04.317  5242  9677 I         : SUMMARY: AddressSanitizer: heap-buffer-overflow /proc/self/cwd/external/libhevc/decoder/ihevcd_parse_slice_header.c:885:52 in ihevcd_parse_slice_header
04-21 15:03:04.317  5242  9677 I         : 
04-21 15:03:04.317  5242  9677 I         : Shadow bytes around the buggy address:
04-21 15:03:04.317  5242  9677 I         :   0x1d1a00d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-21 15:03:04.318  5242  9677 I         :   0x1d1a00e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-21 15:03:04.318  5242  9677 I         :   0x1d1a00f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-21 15:03:04.318  5242  9677 I         :   0x1d1a0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-21 15:03:04.318  5242  9677 I         :   0x1d1a0110: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-21 15:03:04.318  5242  9677 I         : =>0x1d1a0120: fa fa fa fa fa[fa]fa fa fa fa fa fa fa fa fa fa
04-21 15:03:04.318  5242  9677 I         :   0x1d1a0130: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-21 15:03:04.318  5242  9677 I         :   0x1d1a0140: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-21 15:03:04.318  5242  9677 I         :   0x1d1a0150: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-21 15:03:04.318  5242  9677 I         :   0x1d1a0160: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-21 15:03:04.318  5242  9677 I         :   0x1d1a0170: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
04-21 15:03:04.318  5242  9677 I         : Shadow byte legend (one shadow byte represents 8 application bytes):
04-21 15:03:04.318  5242  9677 I         :   Addressable:           00
04-21 15:03:04.318  5242  9677 I         :   Partially addressable: 01 02 03 04 05 06 07 
04-21 15:03:04.318  5242  9677 I         :   Heap left redzone:       fa
04-21 15:03:04.318  5242  9677 I         :   Heap right redzone:      fb
04-21 15:03:04.318  5242  9677 I         :   Freed heap region:       fd
04-21 15:03:04.318  5242  9677 I         :   Stack left redzone:      f1
04-21 15:03:04.318  5242  9677 I         :   Stack mid redzone:       f2
04-21 15:03:04.318  5242  9677 I         :   Stack right redzone:     f3
04-21 15:03:04.318  5242  9677 I         :   Stack partial redzone:   f4
04-21 15:03:04.318  5242  9677 I         :   Stack after return:      f5
04-21 15:03:04.318  5242  9677 I         :   Stack use after scope:   f8
04-21 15:03:04.318  5242  9677 I         :   Global redzone:          f9
04-21 15:03:04.318  5242  9677 I         :   Global init order:       f6
04-21 15:03:04.318  5242  9677 I         :   Poisoned by user:        f7
04-21 15:03:04.318  5242  9677 I         :   Container overflow:      fc
04-21 15:03:04.318  5242  9677 I         :   Array cookie:            ac
04-21 15:03:04.318  5242  9677 I         :   Intra object redzone:    bb
04-21 15:03:04.318  5242  9677 I         :   ASan internal:           fe
04-21 15:03:04.318  5242  9677 I         :   Left alloca redzone:     ca
04-21 15:03:04.318  5242  9677 I         :   Right alloca redzone:    cb
04-21 15:03:04.318  5242  9677 I         : 
04-21 15:03:04.318  5242  9677 I         : Thread T120 (le.hevc.decoder) created by T11 (Binder:5242_5) here:
04-21 15:03:04.318  5242  9677 I         : 
04-21 15:03:04.320  5242  9677 I         :     #0 0xefc9e4db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-21 15:03:04.320  5242  9677 I         : 
04-21 15:03:04.320  5242  9677 I         :     #1 0xefc2eef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-21 15:03:04.320  5242  9677 I         : 
04-21 15:03:04.320  5242  9677 I         : 
04-21 15:03:04.320  5242  9677 I         : 
04-21 15:03:04.320  5242  9677 I         : Thread T11 (Binder:5242_5) created by T4 (Binder:5242_2) here:
04-21 15:03:04.320  5242  9677 I         : 
04-21 15:03:04.321  5242  9677 I         :     #0 0xefc9e4db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-21 15:03:04.321  5242  9677 I         : 
04-21 15:03:04.321  5242  9677 I         :     #1 0xefc2eef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-21 15:03:04.321  5242  9677 I         : 
04-21 15:03:04.321  5242  9677 I         : 
04-21 15:03:04.321  5242  9677 I         : 
04-21 15:03:04.321  5242  9677 I         : Thread T4 (Binder:5242_2) created by T0 here:
04-21 15:03:04.321  5242  9677 I         : 
04-21 15:03:04.321  5242  9677 I         :     #0 0xefc9e4db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-21 15:03:04.321  5242  9677 I         : 
04-21 15:03:04.321  5242  9677 I         :     #1 0xefc2eef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-21 15:03:04.321  5242  9677 I         : 
04-21 15:03:04.322  5242  9677 I         :     #2 0xf03afc4d in __libc_init (/system/lib/libc.so+0x16c4d)
04-21 15:03:04.322  5242  9677 I         : 
04-21 15:03:04.322  5242  9677 I         :     #3 0xffffffff  (<unknown module>)
04-21 15:03:04.322  5242  9677 I         : 
04-21 15:03:04.322  5242  9677 I         : 
04-21 15:03:04.322  5242  9677 I         : 
04-21 15:03:04.323  5242  9677 I         : ==5242==ABORTING
04-21 15:03:04.323  5242  9677 I         : 
04-21 15:03:04.345   387   387 I ServiceManager: service 'media.codec' died
04-21 15:03:04.345  9671  9676 E ACodec  : OMX/mediaserver died, signalling error!
04-21 15:03:04.346  9671  9676 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
04-21 15:03:04.347  9671  9675 E MediaCodec: Codec reported err 0xffffffe0, actionCode 0, while in state 6
