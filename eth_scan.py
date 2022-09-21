# import struct
import re
import os
import csv
import datetime
import requests
import numpy as np
from mmap import ACCESS_READ, mmap

now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d_%H_%M_%S')

path = input("write full path: ")
try:
    handle = open(path, 'rb+')
except IOError:
    print('IOError : File path is invalid')
    sys.exit()
print(path)

def showmenu():  # 메뉴 선택 함수
    print()
    print("[Ethereum Aritifacts search choose menu]")
    for i in range(0, len(menu)):
        print(i+1, ".", menu[i])
    print()
    
def artifacts():
    if sel == 1:
        p = re.compile(rb'0x[a-fA-F0-9]{40}', re.IGNORECASE | re.MULTILINE) #이더리움 주소, 0x[0-9A-Fa-f]{40,44}
    elif sel == 2:
        p = re.compile(rb'[0-9a-f]{64}', re.IGNORECASE | re.MULTILINE) #이더리움 개인키
    elif sel == 3:
        p = re.compile(rb'"([address"]*)":"([a-fA-F0-9]{40})","([crypto"]*)":', re.IGNORECASE | re.MULTILINE) #이더리움 키스토어
    elif sel == 4:
        p = re.compile(rb'[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}', re.IGNORECASE | re.MULTILINE) # 나모닉 코드 12자리
        mnemonic_word()
    elif sel == 5:
        p = re.compile(rb'[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}\s[a-z]{3,15}', re.IGNORECASE | re.MULTILINE) # 나모닉 코드 24자리
        mnemonic_word()
    else:
        print("another artifacts?")
    print("============ Next Step ============")
    
    with open(path, 'rb') as file, mmap(file.fileno(), length=0, access=ACCESS_READ) as mm:
        b=type(mm)
        #print(b)
        for match in p.finditer(mm):
            s = match.start()
            e = match.end()
            grep_match_found = mm[s:e].decode("utf-8")
            match_result = str(grep_match_found) #결과값 String
            #print(match_result)
            with open('c:\\temp\\'+f'{nowDate}'+'_match_1차_list.txt', '+a') as file:
                file.write(match_result+'\n')
                file.close()
        #mm.close()

            #여기서 부터 address 한줄 씩 받아서 검증 및 중복값 제거
            if sel == 1:
                apikey = "WP3JPWBB21D6JRN1AVIE451N4H5YVTJN4M" 
                URL = f"https://api.etherscan.io/api?module=account&action=txlist&apikey={apikey}&sort=desc&address={match_result}"
                if match_result in URL:
                    global csv_file
                    csv_file = 'c:\\temp\\'+f'{nowDate}'+'_ethereum_address_scan_result.csv'
                    headers = {'User-Agent': 'Mozilla/5.0'} # header 선언, http 요청 브라우저는 Mozilla.
                    resp = requests.get(URL).json() # http get 요청을 resp 변수에 json 형태로 선언
                    for key, value in resp.items():  # apikey error test
                        if value == "1":
                            print(URL)
                            global api_result, ts_result, to_result, hx_result
                            status = resp["message"]
                            data = resp["result"] # result 결과인 value만 변수에 담기
                            api_result = dict(data[0])
                            ts_result = api_result.get('timeStamp')
                            to_result = api_result.get('to')
                            hx_result = api_result.get('hash')
                            csv_print()
                        else:
                            continue
            elif sel == 2:
                print("sel 2")
            elif sel == 3:
                print(match_result)
            elif sel == 4:
                mnemonic_file = open('c:\\temp\\match_1차_list.txt')
                for line in mnemonic_file.readlines():
                    print(line)
                    type(line)
                    if line in MNEM_LIST:
                        match_mnemonic = line
                        print("MATCH FOUND : ", match_mnemonic)
                    #csv_file = input("file full path : ")
                    #csv_print()
                    else:
                        #print("This is not mnemonic code")
                        exit()
                                
        file.close()
        mm.close()
        
def csv_print():
    with open(csv_file, '+a', encoding='utf-8-sig') as csvfile:
        #writer = csv.writer(csvfile, fieldnames=['timeStamp', 'to', 'hash', 'isError', 'gas', 'methodId', 'blockNumber', 'cumulativeGasUsed', 'blockHash', 'gasPrice', 'contractAddress', 'nonce', 'transactionIndex', 'confirmations', 'value', 'from', 'functionName', 'input', 'txreceipt_status', 'gasUsed'])
        writer = csv.writer(csvfile)
        #writer.writeheader()
        if sel == 1:
            writer.writerow([ts_result, to_result, hx_result])
        elif sel == 4:
            writer.writerow(match_result)

def mnemonic_word():
    global MNEM_LIST
    dicfile = open("G:\\내 드라이브\\04 - Ethereum_study\\ethereum_forensic\\mnemonic_word.csv",'r')
    MNEMONIC_DIC = csv.reader(dicfile)
    MNEM_LIST = list(MNEMONIC_DIC)
    print(MNEM_LIST)
    dicfile.close()
    
if __name__ == '__main__':
    menu = ("address", "private key", "keystore", "mnemonic code(12)", "mnemonic code(24)")
    while True:
        showmenu()
        sel = int(input("Choose Menu number (Exit 0) : "))
        if sel == 0:
            break
        elif(sel>=1 and sel <= len(menu)):
            #transactions("")
            artifacts()
            print ("transaction result print")
            sel1 = str(input("[*] Do you want to continue searching? if you enter 'no', quit process : "))
            if sel1 == "no":
                break
            elif sel1 == "yes":
                print ("keep going")
                artifacts()
            else : 
                print ("quit")
        else:
            print("잘못된 메뉴 번호입니다.")
    print ("complete search")


#0x9ae08d0118e105dce648a7fba6fc12b2c3e9c288
# G:\내 드라이브\mem_dump\memdump.mem
# G:\내 드라이브\04 - Ethereum_study\ethereum_tracking\051021-8734-01.dmp