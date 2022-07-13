Android libgdx out of bounds read

Code:
stbi_inline static int stbi__extend_receive(stbi__jpeg *j, int n)
{
    unsigned int k;
    int sgn;
    if (j->code_bits < n) stbi__grow_buffer_unsafe(j);

    sgn = (stbi__int32)j->code_buffer >> 31; // sign bit is always in MSB
    k = stbi_lrot(j->code_buffer, n);
[1] STBI_ASSERT(n >= 0 && n < (int) (sizeof(stbi__bmask)/sizeof(*stbi__bmask)));
    j->code_buffer = k & ~stbi__bmask[n];
    k &= stbi__bmask[n];
    j->code_bits -= n;
[2] return k + (stbi__jbias[n] & ~sgn);
}


Size of stbi__mask array is 17, size of stbi__jbias array is 16.
According to check on line #1, max value of 'n' is 16, which will lead to
out of bounds read on line #2.

How to test:

1) compile test app t1.c

$ cp t1.c external/libgdx/gdx/jni/gdx2
$ cd external/libgdx/gdx/jni/gdx2
$ clang -O1  -fsanitize=address -fno-omit-frame-pointer  -o t1a t1.c gdx2d.c  -m32 -I. -DNOJNI=1 -lm -g

2) run t1a
$./t1a 1.bin

reading file 1.bin, 4872 bytes
=================================================================
==30808==ERROR: AddressSanitizer: global-buffer-overflow on address 0x080f9240 at pc 0x80ea5da bp 0xfffb9978 sp 0xfffb9970
READ of size 4 at 0x080f9240 thread T0
    #0 0x80ea5d9 in stbi__extend_receive /home/el/dist/src/android/libgdx/gdx2d/./stb_image.h:1690
    #1 0x80e8c72 in stbi__jpeg_decode_block /home/el/dist/src/android/libgdx/gdx2d/./stb_image.h:1745
    #2 0x80e7f5f in stbi__parse_entropy_coded_data /home/el/dist/src/android/libgdx/gdx2d/./stb_image.h:2510
    #3 0x80e606c in stbi__decode_jpeg_image /home/el/dist/src/android/libgdx/gdx2d/./stb_image.h:2848
    #4 0x80e49aa in load_jpeg_image /home/el/dist/src/android/libgdx/gdx2d/./stb_image.h:3340
    #5 0x80ddaa3 in stbi__jpeg_load /home/el/dist/src/android/libgdx/gdx2d/./stb_image.h:3438
    #6 0x80cb123 in stbi__load_flip /home/el/dist/src/android/libgdx/gdx2d/./stb_image.h:983
    #7 0x80cb387 in stbi_load_from_memory /home/el/dist/src/android/libgdx/gdx2d/./stb_image.h:1072
    #8 0x80cd396 in gdx2d_load /home/el/dist/src/android/libgdx/gdx2d/gdx2d.c:226
    #9 0x80cadf7 in main /home/el/dist/src/android/libgdx/gdx2d/t1.c:34
    #10 0xf7569af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #11 0x80cabb4 in _start (/home/el/dist/src/android/libgdx/gdx2d/t1a+0x80cabb4)

0x080f9240 is located 32 bytes to the left of global variable '.str25' from 'gdx2d.c' (0x80f9260) of size 82
  '.str25' is ascii string '(((j->code_buffer) >> (32 - h->size[c])) & stbi__bmask[h->size[c]]) == h->code[c]'
0x080f9240 is located 0 bytes to the right of global variable 'stbi__jbias' from 'gdx2d.c' (0x80f9200) of size 64
SUMMARY: AddressSanitizer: global-buffer-overflow /home/el/dist/src/android/libgdx/gdx2d/./stb_image.h:1690 stbi__extend_receive
Shadow bytes around the buggy address:
  0x2101f1f0: 02 f9 f9 f9 f9 f9 f9 f9 05 f9 f9 f9 f9 f9 f9 f9
  0x2101f200: 00 00 00 01 f9 f9 f9 f9 00 00 00 00 00 00 00 00
  0x2101f210: 03 f9 f9 f9 f9 f9 f9 f9 00 00 00 00 00 00 00 07
  0x2101f220: f9 f9 f9 f9 00 00 00 00 00 04 f9 f9 f9 f9 f9 f9
  0x2101f230: 00 00 00 00 00 00 00 00 04 f9 f9 f9 f9 f9 f9 f9
=>0x2101f240: 00 00 00 00 00 00 00 00[f9]f9 f9 f9 00 00 00 00
  0x2101f250: 00 00 00 00 00 00 02 f9 f9 f9 f9 f9 00 00 00 00
  0x2101f260: 00 00 00 02 f9 f9 f9 f9 00 00 00 f9 f9 f9 f9 f9
  0x2101f270: 00 00 00 f9 f9 f9 f9 f9 00 00 00 f9 f9 f9 f9 f9
  0x2101f280: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x2101f290: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==30808==ABORTING

