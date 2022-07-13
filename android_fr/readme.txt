Android framesequence heap overflow

Tested with android-7.1.1_r1 branch on Nexus 5X.

Code frameworks/ex/framesequence/jni/FrameSequence_webp.cpp:
FrameSequence_webp::FrameSequence_webp(Stream* stream) {
    if (stream->getRawBuffer() != NULL) {
        mData.size = stream->getRawBufferSize();
        mData.bytes = stream->getRawBufferAddr();
        mRawByteBuffer = stream->getRawBuffer();
    } else {
        uint8_t riff_header[RIFF_HEADER_SIZE];
        if (stream->read(riff_header, RIFF_HEADER_SIZE) != RIFF_HEADER_SIZE) {
            ALOGE("WebP header load failed");
            return;
        }
[1]     mData.size = CHUNK_HEADER_SIZE + GetLE32(riff_header + TAG_SIZE);
[2]     mData.bytes = new uint8_t[mData.size];
        memcpy((void*)mData.bytes, riff_header, RIFF_HEADER_SIZE);

        void* remaining_bytes = (void*)(mData.bytes + RIFF_HEADER_SIZE);
[3]     size_t remaining_size = mData.size - RIFF_HEADER_SIZE;
        if (stream->read(remaining_bytes, remaining_size) != remaining_size) {
            ALOGE("WebP full load failed");
            return;
        }
    }
    ...
}

There is integer overflow on line #1, so mData.size could be set to a value less than RIFF_HEADER_SIZE.
On line #2 small buffer will be allocated. 
On line #3 this buffer will be overwritten with our data.

How to reproduce:
1) get android source code

2) add the following line to frameworks/ex/framesequence/jni/Android.mk - "FRAMESEQUENCE_INCLUDE_WEBP := true " 

3) you will need to overwrite samples/FrameSequenceSamples/res/raw/animated_webp.webp file to trigger the bug
$ ./gen1.py
$ cp 1.webp samples/FrameSequenceSamples/res/raw/animated_webp.webp

4) compile framesequence lib and sample code:
$ cd frameworks/ex/framesequence
$ mm
$ cd samples/FrameSequenceSamples/
$ mm

5) install FrameSequenceSample.apk

To trigger the bug, open FrameSequenceSample app and click 'WEBP animation'.

adb logcat output:

--------- beginning of crash
03-15 23:53:04.713  1853  1853 F libc    : Fatal signal 11 (SIGSEGV), code 1, fault addr 0x58585858585868 in tid 1853 (equence.samp
les)
03-15 23:53:04.714   361   361 W         : debuggerd: handling request: pid=1853 uid=10042 gid=10042 tid=1853
03-15 23:53:04.794  1876  1876 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
03-15 23:53:04.794  1876  1876 F DEBUG   : Build fingerprint: 'Android/aosp_bullhead/bullhead:7.1.1/NMF26F/el12141519:userdebug/tes
t-keys'
03-15 23:53:04.794  1876  1876 F DEBUG   : Revision: 'rev_1.0'
03-15 23:53:04.794  1876  1876 F DEBUG   : ABI: 'arm64'
03-15 23:53:04.794  1876  1876 F DEBUG   : pid: 1853, tid: 1853, name: equence.samples  >>> com.android.framesequence.samples <<<
03-15 23:53:04.794  1876  1876 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x58585858585868
03-15 23:53:04.794  1876  1876 F DEBUG   :     x0   00000073be1e3380  x1   000000007a4e300c  x2   00000073d816c7d0  x3   00000073d8
16c7e1
03-15 23:53:04.794  1876  1876 F DEBUG   :     x4   0000000000000000  x5   0000000000004000  x6   00000073d81f07b0  x7   00000073d7
f261c0
03-15 23:53:04.794  1876  1876 F DEBUG   :     x8   5858585858585858  x9   0000000000004000  x10  0000000000000000  x11  00000073d7
caa5e0
03-15 23:53:04.794  1876  1876 F DEBUG   :     x12  00000073d7caa628  x13  00000073d7caa670  x14  00000073d7caa6d0  x15  0000000000000000
03-15 23:53:04.794  1876  1876 F DEBUG   :     x16  0000007fd4194998  x17  0000000000000000  x18  00000073bded1900  x19  00000073be1e3380
03-15 23:53:04.795  1876  1876 F DEBUG   :     x20  00000073d823e000  x21  000000007a4e300c  x22  000000007a4e3000  x23  0000000000000000
03-15 23:53:04.795  1876  1876 F DEBUG   :     x24  0000000000004000  x25  00000073be1e3380  x26  00000073d8295a98  x27  0000000000000043
03-15 23:53:04.795  1876  1876 F DEBUG   :     x28  00000073d814d35e  x29  0000007fd4194930  x30  00000073db8f74d4
03-15 23:53:04.795  1876  1876 F DEBUG   :     sp   0000007fd4194930  pc   00000073db8f74ec  pstate 0000000020000000
03-15 23:53:05.276  1876  1876 F DEBUG   : backtrace:
03-15 23:53:05.277  1876  1876 F DEBUG   :     #00 pc 00000000000f54ec  /system/lib64/libandroid_runtime.so
03-15 23:53:05.277  1876  1876 F DEBUG   :     #01 pc 0000000001a07ae4  /system/framework/arm64/boot-framework.oat (offset 0x1686000) (android.content.res.AssetManager.readAsset+176)
03-15 23:53:05.277  1876  1876 F DEBUG   :     #02 pc 0000000001a052b8  /system/framework/arm64/boot-framework.oat (offset 0x1686000) (android.content.res.AssetManager.-wrap1+68)
03-15 23:53:05.277  1876  1876 F DEBUG   :     #03 pc 0000000001a05020  /system/framework/arm64/boot-framework.oat (offset 0x1686000) (android.content.res.AssetManager$AssetInputStream.read+92)
03-15 23:53:05.277  1876  1876 F DEBUG   :     #04 pc 00000000000d2734  /system/lib64/libart.so (art_quick_invoke_stub+580)
03-15 23:53:05.277  1876  1876 F DEBUG   :     #05 pc 00000000000df400  /system/lib64/libart.so (_ZN3art9ArtMethod6InvokeEPNS_6ThreadEPjjPNS_6JValueEPKc+208)
03-15 23:53:05.277  1876  1876 F DEBUG   :     #06 pc 000000000042d334  /system/lib64/libart.so (_ZN3artL18InvokeWithArgArrayERKNS_33ScopedObjectAccessAlreadyRunnableEPNS_9ArtMethodEPNS_8ArgArrayEPNS_6JValueEPKc+108)
03-15 23:53:05.277  1876  1876 F DEBUG   :     #07 pc 000000000042e8dc  /system/lib64/libart.so (_ZN3art35InvokeVirtualOrInterfaceWithVarArgsERKNS_33ScopedObjectAccessAlreadyRunnableEP8_jobjectP10_jmethodIDSt9__va_list+388)
03-15 23:53:05.277  1876  1876 F DEBUG   :     #08 pc 000000000033238c  /system/lib64/libart.so (_ZN3art3JNI14CallIntMethodVEP7_JNIEnvP8_jobjectP10_jmethodIDSt9__va_list+620)
03-15 23:53:05.277  1876  1876 F DEBUG   :     #09 pc 0000000000008048  /system/lib64/libframesequence.so
03-15 23:53:05.277  1876  1876 F DEBUG   :     #10 pc 0000000000007f50  /system/lib64/libframesequence.so
03-15 23:53:05.277  1876  1876 F DEBUG   :     #11 pc 0000000000007e74  /system/lib64/libframesequence.so
03-15 23:53:05.277  1876  1876 F DEBUG   :     #12 pc 000000000000847c  /system/lib64/libframesequence.so
03-15 23:53:05.277  1876  1876 F DEBUG   :     #13 pc 0000000000008e0c  /system/lib64/libframesequence.so
03-15 23:53:05.277  1876  1876 F DEBUG   :     #14 pc 00000000000065d0  /system/lib64/libframesequence.so
03-15 23:53:05.277  1876  1876 F DEBUG   :     #15 pc 0000000000006ae4  /system/lib64/libframesequence.so
03-15 23:53:05.277  1876  1876 F DEBUG   :     #16 pc 0000000000009b04  /system/app/FrameSequenceSample/oat/arm64/FrameSequenceSample.odex (offset 0x9000)
...

