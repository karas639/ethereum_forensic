import struct
import re
import os
from mmap import ACCESS_READ, mmap
import pandas as pd
from pandas import Series, DataFrame

path = input("write full path: ")

try:
    handle = open(path, 'rb+')
except IOError:
    print('IOError : File path is invalid')
    sys.exit()

print(path)

global df
global count
df = DataFrame(columns=['address'])
count = 1000000000


#p = re.compile(rb'0x[a-fA-F0-9]{40}$', re.DOTALL | re.IGNORECASE | re.MULTILINE)
p = re.compile(rb'0x[a-fA-F0-9]{40}', re.IGNORECASE | re.MULTILINE)

with open(path, 'rb') as f, mmap(f.fileno(), length=0, access=ACCESS_READ) as mm:
    #print(mm[0:42])
    b=type(mm)
    print(b)
        
    for match in p.finditer(mm):
        s = match.start()
        e = match.end()
        grep_match_found = mm[s:e].decode("utf-8")
        print(str(grep_match_found))
        address = str(grep_match_found)
        for i in address:
            y = 0
            if y < count:
                df = df.append(DataFrame([address], columns=['address']))
                df.to_csv('result.csv')
            else:
                break
        #g = match.group()
        #grep_match_found = mm[g].decode("utf-8")
        #print("match_found : ", match.group())


