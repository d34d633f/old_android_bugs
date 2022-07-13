Android libhevc null ptr.
Looks like it is useless bug.

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

AddressSanitizer: SEGV on unknown address 0x00000002 (pc 0xf1c4b4e4 bp 0xf04ff008 sp 0xf04fefe0 T22716)
04-17 07:59:13.589 26844 19505 I         : 
04-17 07:59:13.589 26844 19505 I         : 
04-17 07:59:13.654 26844 19505 I         :     #0 0xf1c4b4e3 in GET_MV_NBR_LT /proc/self/cwd/external/libhevc/decoder/ihevcd_mv_pred.c:277:13
04-17 07:59:13.654 26844 19505 I         : 
04-17 07:59:13.654 26844 19505 I         :     #1 0xf1c4de8f in ihevcd_mv_pred /proc/self/cwd/external/libhevc/decoder/ihevcd_mv_pred.c:631:13
04-17 07:59:13.655 26844 19505 I         : 
04-17 07:59:13.655 26844 19505 I         :     #2 0xf1c495e3 in ihevcd_get_mv_ctb /proc/self/cwd/external/libhevc/decoder/ihevcd_get_mv.c:354:17
04-17 07:59:13.655 26844 19505 I         : 
04-17 07:59:13.656 26844 19505 I         :     #3 0xf1c39be3 in ihevcd_process /proc/self/cwd/external/libhevc/decoder/ihevcd_process_slice.c:691:25
04-17 07:59:13.656 26844 19505 I         : 
04-17 07:59:13.656 26844 19505 I         :     #4 0xf1c410bb in ihevcd_process_thread /proc/self/cwd/external/libhevc/decoder/ihevcd_process_slice.c:1598:13
04-17 07:59:13.656 26844 19505 I         : 
04-17 07:59:13.660 26844 19505 I         :     #5 0xf5dce023 in __pthread_start(void*) (/system/lib/libc.so+0x47023)
04-17 07:59:13.660 26844 19505 I         : 
04-17 07:59:13.661 26844 19505 I         :     #6 0xf5da0e3d in __start_thread (/system/lib/libc.so+0x19e3d)
04-17 07:59:13.661 26844 19505 I         : 
04-17 07:59:13.661 26844 19505 I         : 
04-17 07:59:13.661 26844 19505 I         : 
04-17 07:59:13.661 26844 19505 I         : AddressSanitizer can not provide additional info.
04-17 07:59:13.661 26844 19505 I         : 
04-17 07:59:13.661 26844 19505 I         : SUMMARY: AddressSanitizer: SEGV /proc/self/cwd/external/libhevc/decoder/ihevcd_mv_pred.c:277:13 in GET_MV_NBR_LT
04-17 07:59:13.661 26844 19505 I         : 
04-17 07:59:13.661 26844 19505 I         : Thread T22716 created by T22693 (le.hevc.decoder) here:
04-17 07:59:13.661 26844 19505 I         : 
04-17 07:59:13.663 26844 19505 I         :     #0 0xf624f4db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-17 07:59:13.663 26844 19505 I         : 
04-17 07:59:13.663 26844 19505 I         :     #1 0xf1c43eb3 in ihevcd_parse_pic_init /proc/self/cwd/external/libhevc/decoder/ihevcd_utils.c:1075:17
04-17 07:59:13.664 26844 19505 I         : 
04-17 07:59:13.665 26844 19505 I         :     #2 0xf1c27f93 in ihevcd_parse_slice_data /proc/self/cwd/external/libhevc/decoder/ihevcd_parse_slice.c:2265:15
04-17 07:59:13.665 26844 19505 I         : 
04-17 07:59:13.665 26844 19505 I         :     #3 0xf1c11c13 in ihevcd_nal_unit /proc/self/cwd/external/libhevc/decoder/ihevcd_nal.c:405:27
04-17 07:59:13.665 26844 19505 I         : 
04-17 07:59:13.666 26844 19505 I         :     #4 0xf1c0de63 in ihevcd_decode /proc/self/cwd/external/libhevc/decoder/ihevcd_decode.c:604:15
04-17 07:59:13.666 26844 19505 I         : 
04-17 07:59:13.667 26844 19505 I         :     #5 0xf1c0c497 in ihevcd_cxa_api_function /proc/self/cwd/external/libhevc/decoder/ihevcd_api.c:3552:19
04-17 07:59:13.667 26844 19505 I         : 
04-17 07:59:13.668 26844 19505 I         :     #6 0xf1bf9f09 in android::SoftHEVC::onQueueFilled(unsigned int) /proc/self/cwd/frameworks/av/media/libstagefright/codecs/hevcdec/SoftHEVC.cpp:576:22
04-17 07:59:13.668 26844 19505 I         : 
04-17 07:59:13.668 26844 19505 I         : 
04-17 07:59:13.668 26844 19505 I         : 
04-17 07:59:13.668 26844 19505 I         : Thread T22693 (le.hevc.decoder) created by T174 (Binder:26844_5) here:
04-17 07:59:13.668 26844 19505 I         : 
04-17 07:59:13.668 26844 19505 I         :     #0 0xf624f4db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-17 07:59:13.668 26844 19505 I         : 
04-17 07:59:13.669 26844 19505 I         :     #1 0xf60cfef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-17 07:59:13.669 26844 19505 I         : 
04-17 07:59:13.669 26844 19505 I         : 
04-17 07:59:13.669 26844 19505 I         : 
04-17 07:59:13.670 26844 19505 I         : Thread T174 (Binder:26844_5) created by T0 here:
04-17 07:59:13.670 26844 19505 I         : 
04-17 07:59:13.670 26844 19505 I         :     #0 0xf624f4db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-17 07:59:13.670 26844 19505 I         : 
04-17 07:59:13.670 26844 19505 I         :     #1 0xf60cfef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-17 07:59:13.670 26844 19505 I         : 
04-17 07:59:13.670 26844 19505 I         :     #2 0xf5d9dc4d in __libc_init (/system/lib/libc.so+0x16c4d)
04-17 07:59:13.670 26844 19505 I         : 
04-17 07:59:13.671 26844 19505 I         :     #3 0xffffffff  (<unknown module>)
04-17 07:59:13.671 26844 19505 I         : 
04-17 07:59:13.671 26844 19505 I         : 
04-17 07:59:13.671 26844 19505 I         : 
04-17 07:59:13.672 26844 19505 I         : ==26844==ABORTING
04-17 07:59:13.672 26844 19505 I         : 
04-17 07:59:13.699   389   389 I ServiceManager: service 'media.codec' died
04-17 07:59:13.699 19476 19481 E ACodec  : OMX/mediaserver died, signalling error!
04-17 07:59:13.699 19476 19481 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
