
Vulnerable code exists in rtsp/AAMRAssembler.cpp

<code>
ARTPAssembler::AssemblyStatus AAMRAssembler::addPacket() {
    ... 
    ...
    size_t offset = 1;
    size_t totalSize = 0;
    for (;;) {
        if (offset >= buffer->size()) {
            queue->erase(queue->begin());
            ++mNextExpectedSeqNo;

            ALOGV("Unable to parse TOC.");

            return MALFORMED_PACKET;
        }

        uint8_t toc = buffer->data()[offset++];

        unsigned FT = (toc >> 3) & 0x0f;
        if ((toc & 3) != 0
                || (mIsWide && FT > 9 && FT != 15)
                || (!mIsWide && FT > 8 && FT != 15)) {
            queue->erase(queue->begin());
            ++mNextExpectedSeqNo;

            ALOGV("Illegal TOC entry.");

            return MALFORMED_PACKET;
        }

[1]      totalSize += getFrameSize(mIsWide, (toc >> 3) & 0x0f);
	...
     }


[2] sp<ABuffer> accessUnit = new ABuffer(totalSize);
    CopyTimes(accessUnit, buffer);

    size_t dstOffset = 0;
[3] for (size_t i = 0; i < tableOfContents.size(); ++i) {
        uint8_t toc = tableOfContents[i];

        size_t frameSize = getFrameSize(mIsWide, (toc >> 3) & 0x0f);

        if (offset + frameSize - 1 > buffer->size()) {
            queue->erase(queue->begin());
            ++mNextExpectedSeqNo;

            ALOGV("AMR packet too short.");

            return MALFORMED_PACKET;
        }

        accessUnit->data()[dstOffset++] = toc;
        memcpy(accessUnit->data() + dstOffset,
               buffer->data() + offset, frameSize - 1);

        offset += frameSize - 1;
        dstOffset += frameSize - 1;
    }

</code>

On line #1 heap overflow will occur, thus on line #2 small buffer will be allocated.
On line #3 for loop overflows our small buffer.

Bug most probably is not exploitable in practice, because largest frame size is 61.
