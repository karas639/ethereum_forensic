import struct
import re
import os
from mmap import ACCESS_READ, mmap

global a

a = input("input file name: ")
#print(a)

'''
f = open(a, 'rb')
data = f.read()
f.close()
'''
chunk_size = 2**32
matches = []
#pattern_group = [b,'^0x[a-fA-F0-9]{40}$']
p = re.compile(b'^0x[a-fA-F0-9]{40}$')
max_length = 42
#p1 = re.compile(b'0x9Ae08d0118E105Dce648A7fBA6fc12b2c3e9c288')
#m = p.match('0x9Ae08d0118E105Dce648A7fBA6fc12b2c3e9c288')
#m = p.search(data)
#print(m) # 내용없음
#m = re.finditer(p, data)
#print(m)

with open(a, 'rb') as f, mmap(f.fileno(), 0, access=ACCESS_READ) as mm:
    #print(mm[0:])
    for match in p.finditer(mm):
        #if not (match.end() == len(mm) and len(match.group()) < max_length and length == chunk_size):
        #    matches.append(match.group())
    #mm.close()
#f.close()
        #print("------result------")
        print(match)
        #print(match.decode("utf-8"))

#if m:
#    print("found a match: ", m.group(1))
#    print("match offset: ", m.start())
