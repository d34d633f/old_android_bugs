Android libgdx stbi__psd_load() heap overflow


static stbi_uc *stbi__psd_load(stbi__context *s, int *x, int *y, int *comp, int req_comp)
{
   int   pixelCount;
   int channelCount, compression;
   int channel, i, count, len;
   int bitdepth;
   int w,h;
   stbi_uc *out;
   ...
   ...
           // Read the RLE data.
            count = 0;
            while (count < pixelCount) {
[1]            len = stbi__get8(s);
               if (len == 128) {
                  // No-op.
               } else if (len < 128) {
                  // Copy next len+1 bytes literally.
                  len++;
                  count += len;
                  while (len) {
[2]                  *p = stbi__get8(s);
                     p += 4;
                     len--;
                  }

The problem is that 'len' (read on line #1) is not cheched against 
the size of allocated buffer (which is 4*w*h).

If 'len' > 4*w*h heap overflow will occur on line #2.

How to test:

1) compile test app t1.c

$ cp t1.c external/libgdx/gdx/jni/gdx2
$ cd external/libgdx/gdx/jni/gdx2
$ clang -O1  -fsanitize=address -fno-omit-frame-pointer  -o t1a t1.c gdx2d.c  -m32 -I. -DNOJNI=1 -DSTBI_ONLY_PSD=1 -lm -g

2) generate malformed psd file:
$ ./gen.py

3) run t1a
$./t1a 1.bin

reading file 1.bin, 4043 bytes
=================================================================
==10748==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf62007d4 at pc 0x80d0eae bp 0xff98f638 sp 0xff98f630
WRITE of size 1 at 0xf62007d4 thread T0
    #0 0x80d0ead in stbi__psd_load /dist/src/android/libgdx/gdx2d/./stb_image.h:5233
    #1 0x80caf43 in stbi__load_flip /dist/src/android/libgdx/gdx2d/./stb_image.h:983
    #2 0x80cb1a7 in stbi_load_from_memory /dist/src/android/libgdx/gdx2d/./stb_image.h:1072
    #3 0x80cc166 in gdx2d_load /dist/src/android/libgdx/gdx2d/gdx2d.c:226
    #4 0x80cac17 in main /dist/src/android/libgdx/gdx2d/t1.c:34
    #5 0xf74a9af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #6 0x80ca9d4 in _start (/dist/src/android/libgdx/gdx2d/t1a+0x80ca9d4)

0xf62007d4 is located 0 bytes to the right of 4-byte region [0xf62007d0,0xf62007d4)
allocated by thread T0 here:
    #0 0x80b3601 in __interceptor_malloc (/dist/src/android/libgdx/gdx2d/t1a+0x80b3601)
    #1 0x80d0a1d in stbi__malloc /dist/src/android/libgdx/gdx2d/./stb_image.h:903
    #2 0x80d0ba1 in stbi__psd_load /dist/src/android/libgdx/gdx2d/./stb_image.h:5191
    #3 0x80caf43 in stbi__load_flip /dist/src/android/libgdx/gdx2d/./stb_image.h:983
    #4 0x80cb1a7 in stbi_load_from_memory /dist/src/android/libgdx/gdx2d/./stb_image.h:1072
    #5 0x80cc166 in gdx2d_load /dist/src/android/libgdx/gdx2d/gdx2d.c:226
    #6 0x80cac17 in main /dist/src/android/libgdx/gdx2d/t1.c:34
    #7 0xf74a9af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)

SUMMARY: AddressSanitizer: heap-buffer-overflow /dist/src/android/libgdx/gdx2d/./stb_image.h:5233 stbi__psd_load
Shadow bytes around the buggy address:
  0x3ec400a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ec400b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ec400c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ec400d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ec400e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x3ec400f0: fa fa fa fa fa fa fa fa fa fa[04]fa fa fa 06 fa
  0x3ec40100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ec40110: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ec40120: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ec40130: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x3ec40140: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:     fa
  Heap right redzone:    fb
  Freed heap region:     fd
  Stack left redzone:    f1
  Stack mid redzone:     f2
  Stack right redzone:   f3
  Stack partial redzone: f4
  Stack after return:    f5
  Stack use after scope: f8
  Global redzone:        f9
  Global init order:     f6
  Poisoned by user:      f7
  ASan internal:         fe
==10748==ABORTING


