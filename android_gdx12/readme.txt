Android libgdx stbi__getn() unchecked return value 

There are a couple of places, where return value from stbi__getn() is not checked properly.
If there is no input data left, output buffer will be unitialized.

Most simple from hdr_load():
...
for (j=0; j < height; ++j) {
         for (i=0; i < width; ++i) {
            stbi_uc rgbe[4];
           main_decode_loop:
[1]        stbi__getn(s, rgbe, 4);
            stbi__hdr_convert(hdr_data + j * width * req_comp + i * req_comp, rgbe, req_comp);
         }
...

If there is no input data, rgbe array will be uninitalized
and this uninitialized data will be used to init hdr_data buffer.

How to test:

1) compile test app t1.c

$ cp t1.c external/libgdx/gdx/jni/gdx2
$ cd external/libgdx/gdx/jni/gdx2
$ clang -O1  -fsanitize=address -fno-omit-frame-pointer  -o t1a t1.c gdx2d.c  -m32 -I. -DNOJNI=1 -lm -g

Debug session:

$ gdb -q ./t1
Reading symbols from ./t1...done.
(gdb) list stbi__hdr_convert
5924	   buffer[len] = 0;
5925	   return buffer;
5926	}
5927	
5928	static void stbi__hdr_convert(float *output, stbi_uc *input, int req_comp)
5929	{
5930	   if ( input[3] != 0 ) {
5931	      float f1;
5932	      // Exponent
5933	      f1 = (float) ldexp(1.0f, input[3] - (int)(128 + 8));
(gdb) b 5930
Breakpoint 1 at 0x804fff0: file ./stb_image.h, line 5930.
(gdb) r 1.bin
Starting program: /dist/src/android/libgdx/gdx2d/test/t1 1.bin
reading file 1.bin, 45 bytes

Breakpoint 1, stbi__hdr_convert (output=0x805b018, input=0xffffc9f4 "\300\352\366\367\004\312\377\377-Y 2 +X 2", 
    req_comp=3) at ./stb_image.h:5930
5930	   if ( input[3] != 0 ) {
(gdb) x/1wx input
0xffffc9f4:	0xf7f6eac0
(gdb) x/10wx 0xf7f6eac0 // Valid pointer
0xf7f6eac0 <_IO_2_1_stdout_>:	0xfbad2a84	0xf7fd5000	0xf7fd5000	0xf7fd5000
0xf7f6ead0 <_IO_2_1_stdout_+16>:	0xf7fd5000	0xf7fd5000	0xf7fd5000	0xf7fd5000
0xf7f6eae0 <_IO_2_1_stdout_+32>:	0xf7fd5400	0x00000000
(gdb) 

