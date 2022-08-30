import struct
import re
import os
from mmap import ACCESS_READ, mmap

path = input("write full path: ")
try:
    handle = open(path, 'rb+')
except IOError:
    print('IOError : File path is invalid')
    sys.exit()
print(path)

p = re.compile(rb'0x[a-fA-F0-9]{40}', re.IGNORECASE | re.MULTILINE)
with open(path, 'rb') as file, mmap(file.fileno(), length=0, access=ACCESS_READ) as mm:
    f = open('ethereum_address_scan.csv', mode='w')
    f.write("address" + "\n")
    f.close()
    for match in p.finditer(mm):
        s = match.start()
        e = match.end()
        grep_match_found = mm[s:e].decode("utf-8")
        address = str(grep_match_found)
        f = open('ethereum_address_scan.csv', mode='+a')
        f.write(address + "\n")
        print(address)
    f.close()
file.close()
mm.close()
    
# H:\mem_dump\memdump_C_210504.mem
# H:\mem_dump\memdump_A_210524.mem
# /mnt/h/mem_dump/memdump_C_210504.mem
# /mnt/h/mem_dump/memdump_A_210512.mem
#0x9ae08d0118e105dce648a7fba6fc12b2c3e9c288
