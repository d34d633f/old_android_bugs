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

AddressSanitizer: SEGV on unknown address 0x00000001 (pc 0xf1c4fc44 bp 0xf01ff008 sp 0xf01fefb8 T11676)
04-17 08:23:46.600  7001 19679 I         : 
04-17 08:23:46.600  7001 19679 I         : 
04-17 08:23:46.668  7001 19679 I         :     #0 0xf1c4fc43 in ihevcd_collocated_mvp /proc/self/cwd/external/libhevc/decoder/ihevcd_mv_merge.c:329:39
04-17 08:23:46.668  7001 19679 I         : 
04-17 08:23:46.668  7001 19679 I         :     #1 0xf1c4e18b in ihevcd_mv_pred /proc/self/cwd/external/libhevc/decoder/ihevcd_mv_pred.c:680:13
04-17 08:23:46.669  7001 19679 I         : 
04-17 08:23:46.669  7001 19679 I         :     #2 0xf1c495e3 in ihevcd_get_mv_ctb /proc/self/cwd/external/libhevc/decoder/ihevcd_get_mv.c:354:17
04-17 08:23:46.669  7001 19679 I         : 
04-17 08:23:46.670  7001 19679 I         :     #3 0xf1c39be3 in ihevcd_process /proc/self/cwd/external/libhevc/decoder/ihevcd_process_slice.c:691:25
04-17 08:23:46.670  7001 19679 I         : 
04-17 08:23:46.670  7001 19679 I         :     #4 0xf1c410bb in ihevcd_process_thread /proc/self/cwd/external/libhevc/decoder/ihevcd_process_slice.c:1598:13
04-17 08:23:46.670  7001 19679 I         : 
04-17 08:23:46.674  7001 19679 I         :     #5 0xf5359023 in __pthread_start(void*) (/system/lib/libc.so+0x47023)
04-17 08:23:46.674  7001 19679 I         : 
04-17 08:23:46.674  7001 19679 I         :     #6 0xf532be3d in __start_thread (/system/lib/libc.so+0x19e3d)
04-17 08:23:46.674  7001 19679 I         : 
04-17 08:23:46.675  7001 19679 I         : 
04-17 08:23:46.675  7001 19679 I         : 
04-17 08:23:46.675  7001 19679 I         : AddressSanitizer can not provide additional info.
04-17 08:23:46.675  7001 19679 I         : 
04-17 08:23:46.675  7001 19679 I         : SUMMARY: AddressSanitizer: SEGV /proc/self/cwd/external/libhevc/decoder/ihevcd_mv_merge.c:329:39 in ihevcd_collocated_mvp
04-17 08:23:46.675  7001 19679 I         : 
04-17 08:23:46.675  7001 19679 I         : Thread T11676 created by T11647 (le.hevc.decoder) here:
04-17 08:23:46.675  7001 19679 I         : 
04-17 08:23:46.677  7001 19679 I         :     #0 0xf54364db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-17 08:23:46.677  7001 19679 I         : 
04-17 08:23:46.678  7001 19679 I         :     #1 0xf1c43eb3 in ihevcd_parse_pic_init /proc/self/cwd/external/libhevc/decoder/ihevcd_utils.c:1075:17
04-17 08:23:46.678  7001 19679 I         : 
04-17 08:23:46.679  7001 19679 I         :     #2 0xf1c27f93 in ihevcd_parse_slice_data /proc/self/cwd/external/libhevc/decoder/ihevcd_parse_slice.c:2265:15
04-17 08:23:46.679  7001 19679 I         : 
04-17 08:23:46.679  7001 19679 I         :     #3 0xf1c11c13 in ihevcd_nal_unit /proc/self/cwd/external/libhevc/decoder/ihevcd_nal.c:405:27
04-17 08:23:46.679  7001 19679 I         : 
04-17 08:23:46.680  7001 19679 I         :     #4 0xf1c0de63 in ihevcd_decode /proc/self/cwd/external/libhevc/decoder/ihevcd_decode.c:604:15
04-17 08:23:46.680  7001 19679 I         : 
04-17 08:23:46.681  7001 19679 I         :     #5 0xf1c0c497 in ihevcd_cxa_api_function /proc/self/cwd/external/libhevc/decoder/ihevcd_api.c:3552:19
04-17 08:23:46.681  7001 19679 I         : 
04-17 08:23:46.682  7001 19679 I         :     #6 0xf1bf9f09 in android::SoftHEVC::onQueueFilled(unsigned int) /proc/self/cwd/frameworks/av/media/libstagefright/codecs/hevcdec/SoftHEVC.cpp:576:22
04-17 08:23:46.682  7001 19679 I         : 
04-17 08:23:46.682  7001 19679 I         : 
04-17 08:23:46.682  7001 19679 I         : 
04-17 08:23:46.683  7001 19679 I         : Thread T11647 (le.hevc.decoder) created by T581 (Binder:7001_5) here:
04-17 08:23:46.683  7001 19679 I         : 
04-17 08:23:46.683  7001 19679 I         :     #0 0xf54364db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-17 08:23:46.683  7001 19679 I         : 
04-17 08:23:46.684  7001 19679 I         :     #1 0xf5b04ef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-17 08:23:46.684  7001 19679 I         : 
04-17 08:23:46.684  7001 19679 I         : 
04-17 08:23:46.684  7001 19679 I         : 
04-17 08:23:46.684  7001 19679 I         : Thread T581 (Binder:7001_5) created by T287 (Binder:7001_4) here:
04-17 08:23:46.684  7001 19679 I         : 
04-17 08:23:46.684  7001 19679 I         :     #0 0xf54364db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-17 08:23:46.684  7001 19679 I         : 
04-17 08:23:46.684  7001 19679 I         :     #1 0xf5b04ef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-17 08:23:46.684  7001 19679 I         : 
04-17 08:23:46.685  7001 19679 I         : 
04-17 08:23:46.685  7001 19679 I         : 
04-17 08:23:46.685  7001 19679 I         : Thread T287 (Binder:7001_4) created by T1 (Binder:7001_1) here:
04-17 08:23:46.685  7001 19679 I         : 
04-17 08:23:46.685  7001 19679 I         :     #0 0xf54364db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-17 08:23:46.685  7001 19679 I         : 
04-17 08:23:46.685  7001 19679 I         :     #1 0xf5b04ef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-17 08:23:46.685  7001 19679 I         : 
04-17 08:23:46.685  7001 19679 I         : 
04-17 08:23:46.685  7001 19679 I         : 
04-17 08:23:46.685  7001 19679 I         : Thread T1 (Binder:7001_1) created by T0 here:
04-17 08:23:46.685  7001 19679 I         : 
04-17 08:23:46.685  7001 19679 I         :     #0 0xf54364db in pthread_create (/system/lib/libclang_rt.asan-arm-android.so+0x5c4db)
04-17 08:23:46.685  7001 19679 I         : 
04-17 08:23:46.686  7001 19679 I         :     #1 0xf5b04ef9 in androidCreateRawThreadEtc (/system/lib/libutils.so+0xdef9)
04-17 08:23:46.686  7001 19679 I         : 
04-17 08:23:46.686  7001 19679 I         :     #2 0xf5328c4d in __libc_init (/system/lib/libc.so+0x16c4d)
04-17 08:23:46.686  7001 19679 I         : 
04-17 08:23:46.686  7001 19679 I         :     #3 0xffffffff  (<unknown module>)
04-17 08:23:46.686  7001 19679 I         : 
04-17 08:23:46.687  7001 19679 I         : 
04-17 08:23:46.687  7001 19679 I         : 
04-17 08:23:46.687  7001 19679 I         : ==7001==ABORTING
04-17 08:23:46.687  7001 19679 I         : 
04-17 08:23:46.714 19644 19649 E ACodec  : OMX/mediaserver died, signalling error!
04-17 08:23:46.714   389   389 I ServiceManager: service 'media.codec' died
04-17 08:23:46.714 19644 19649 E ACodec  : signalError(omxError 0x8000100d, internalError -32)
04-17 08:23:46.715 19644 19648 E MediaCodec: Codec reported err 0xffffffe0, actionCode 0, while in state 6
