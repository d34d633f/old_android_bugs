Android sonivox infinite loop

Details:

static EAS_RESULT NextChunk (SDLS_SYNTHESIZER_DATA *pDLSData, EAS_I32 *pPos, EAS_U32 *pChunkType, EAS_I32 *pSize)
{
    EAS_RESULT result;

    /* seek to start of chunk */
    if ((result = EAS_HWFileSeek(pDLSData->hwInstData, pDLSData->fileHandle, *pPos)) != EAS_SUCCESS)
        return result;

    /* read the chunk type */
    if ((result = EAS_HWGetDWord(pDLSData->hwInstData, pDLSData->fileHandle, pChunkType, EAS_TRUE)) != EAS_SUCCESS)
        return result;

    /* read the chunk size */
    if ((result = EAS_HWGetDWord(pDLSData->hwInstData, pDLSData->fileHandle, pSize, EAS_FALSE)) != EAS_SUCCESS)
        return result;

    /* get form type for RIFF and LIST types */
    if ((*pChunkType == CHUNK_RIFF) || (*pChunkType == CHUNK_LIST))
    {

        /* read the form type */
        if ((result = EAS_HWGetDWord(pDLSData->hwInstData, pDLSData->fileHandle, pChunkType, EAS_TRUE)) != EAS_SUCCESS)
            return result;

    }

[1]  *pPos += *pSize + 8;

    if (*pPos & 1)
        (*pPos)++;

    return EAS_SUCCESS;
}

The value of *pSize is dword and controlled by us, so if it is equal to -8, 
the value of *pPos will stays the same. 
So it is obvious that the  code below (from DLSParser()) enters infinite loop:
	....
    while (pos < endDLS)
    {
        chunkPos = pos;

        if ((result = NextChunk(&dls, &pos, &temp, &size)) != EAS_SUCCESS)
            return result;

    ....

How to reproduce:
$ adb push 1.xmf /mnt/sdcard/
$ adb shell stagefright -s /mnt/sdcard/1.xmf


