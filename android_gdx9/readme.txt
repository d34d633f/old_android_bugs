Android libgdx stbi__getn() overflow

static int stbi__getn(stbi__context *s, stbi_uc *buffer, int n)
{
   if (s->io.read) {
      int blen = (int) (s->img_buffer_end - s->img_buffer);
      if (blen < n) {
         int res, count;

         memcpy(buffer, s->img_buffer, blen);

         count = (s->io.read)(s->io_user_data, (char*) buffer + blen, n - blen);
         res = (count == (n-blen));
         s->img_buffer = s->img_buffer_end;
         return res;
      }
   }

[1] if (s->img_buffer+n <= s->img_buffer_end) {
[2]   memcpy(buffer, s->img_buffer, n);
      s->img_buffer += n;
      return 1;
   } else
      return 0;
}
 
As you can see, on line #1, if 'n' is large enough, s->img_buffer+n could overflow,
so check validates to true. It will lead to heap overflow on line #2.


It is easier to reproduce this bug if sample code is compiled with ASAN.

1) compile test app t1.c

$ cp t1.c external/libgdx/gdx/jni/gdx2
$ cd external/libgdx/gdx/jni/gdx2
$ clang -O1  -fsanitize=address -fno-omit-frame-pointer  -o t1a t1.c gdx2d.c  -m32 -I. -DNOJNI=1 -lm -g

2) run t1a
$./t1a 1.bin

reading file 1.bin, 1662 bytes
ASAN:SIGSEGV
=================================================================
==27331==ERROR: AddressSanitizer: SEGV on unknown address 0xf5d00000 (pc 0x080c0c50 sp 0xffe749cc bp 0x5fc03eed T0)
    #0 0x80c0c4f in __sanitizer::internal_memcpy(void*, void const*, unsigned long) (/dist/src/android/libgdx/gdx2d/test/t1a+0x80c0c4f)
    #1 0x809f88a in __interceptor_memcpy (/dist/src/android/libgdx/gdx2d/test/t1a+0x809f88a)
    #2 0x80d4c7b in stbi__getn /dist/src/android/libgdx/gdx2d/test/./stb_image.h:1287
    #3 0x80d3f2f in stbi__parse_png_file /dist/src/android/libgdx/gdx2d/test/./stb_image.h:4449
    #4 0x80e43ed in stbi__do_png /dist/src/android/libgdx/gdx2d/test/./stb_image.h:4516
    #5 0x80ddbd8 in stbi__png_load /dist/src/android/libgdx/gdx2d/test/./stb_image.h:4539
    #6 0x80cb123 in stbi__load_flip /dist/src/android/libgdx/gdx2d/test/./stb_image.h:983
    #7 0x80cb387 in stbi_load_from_memory /dist/src/android/libgdx/gdx2d/test/./stb_image.h:1072
    #8 0x80cd396 in gdx2d_load /dist/src/android/libgdx/gdx2d/test/gdx2d.c:226
    #9 0x80cadf7 in main /dist/src/android/libgdx/gdx2d/test/t1.c:34
    #10 0xf7587af2 (/lib/i386-linux-gnu/libc.so.6+0x19af2)
    #11 0x80cabb4 in _start (/dist/src/android/libgdx/gdx2d/test/t1a+0x80cabb4)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV ??:0 __sanitizer::internal_memcpy(void*, void const*, unsigned long)
==27331==ABORTING

