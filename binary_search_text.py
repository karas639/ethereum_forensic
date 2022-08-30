#-*- coding: utf-8 -*-

import os, sys, re

path = input("write full path : ")

try:
    handle = open(path, 'rb+')
except IOError:
    print('IOError : File path is invalid')
    sys.exit()

regex = ''
regex = input("write regex or string : ")

RE = 'r'+regex
regexobj = re.compile(RE)

matchcount = 0
length = 0

for line in handle.readlines():
    for matchobj in regexobj.finditer(line):
        print('find : \''+matchobj.group()+'\'\ file offset : %d'%(length+matchobj.start()))
        matchcount += 1
    length += len(line)
print('file total : '+str(length/1000000.0) +'MB')
handle.close()
