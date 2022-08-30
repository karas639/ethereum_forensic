<<<<<<< HEAD
import re
import mmap 

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def searchFile(list_txt, raw_str):
    search="^"+raw_str #add regex ^ newline operator
    search_rgx=re.sub(r'\*+',r'[\\s\\S]*?',search) #replace * with regex function

    #search file
    with open(list_txt, 'r+') as f: 
        data = mmap.mmap(f.fileno(), 0)
        results = re.findall(bytes(search_rgx,encoding="utf-8"),data, re.MULTILINE)

    #save results
    f1 = open('results.txt', 'w+b')
    results_bin = b'\n'.join(results)
    f1.write(results_bin)
    f1.close()

    print("Found "+str(file_len("results.txt"))+" results")

=======
import re
import mmap 

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def searchFile(list_txt, raw_str):
    search="^"+raw_str #add regex ^ newline operator
    search_rgx=re.sub(r'\*+',r'[\\s\\S]*?',search) #replace * with regex function

    #search file
    with open(list_txt, 'r+') as f: 
        data = mmap.mmap(f.fileno(), 0)
        results = re.findall(bytes(search_rgx,encoding="utf-8"),data, re.MULTILINE)

    #save results
    f1 = open('results.txt', 'w+b')
    results_bin = b'\n'.join(results)
    f1.write(results_bin)
    f1.close()

    print("Found "+str(file_len("results.txt"))+" results")

>>>>>>> 9c22d7588e34949bd7802bebb4502d25eceb7acc
searchFile("largelist.txt","ab**cd")