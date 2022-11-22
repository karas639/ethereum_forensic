#### import struct
import re
import os
import csv
import datetime
import requests
import numpy as np
import eth_utils
from mmap import ACCESS_READ, mmap
from web3.auto import w3

now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d')
#nowDate = now.strftime('%Y-%m-%d_%H_%M_%S')
w3.eth.account.enable_unaudited_hdwallet_features()

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
    if sel == 1: #주소, 0x[0-9A-Fa-f]{40,44}
        p = re.compile(rb'^0x[a-fA-F0-9]{40}', re.IGNORECASE | re.MULTILINE)
    elif sel == 2: #개인키
        p = re.compile(rb'[0-9a-f]{64}', re.IGNORECASE | re.MULTILINE) 
    elif sel == 3: #키스토어
        #p = re.compile(rb'"([address"]*)":"([a-fA-F0-9]{40})","([crypto"]*)":', re.IGNORECASE | re.MULTILINE)
        p = re.compile(rb'UTC--[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}.[0-9]{3}Z--[a-fA-F0-9]{40}', re.IGNORECASE | re.MULTILINE)
    elif sel == 4: # 니모닉 코드(12)
        p = re.compile(rb'[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}', re.MULTILINE) # 나모닉 코드 12자리
    elif sel == 5: # 니모닉 코드(24)
        p = re.compile(rb'[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}', re.IGNORECASE | re.MULTILINE) # 나모닉 코드 24자리
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
            if sel == 1: # address는 해당 파일 사용하지 않고 결과값을 별도 csv로 파싱하여 저장(아래)
                apikey = "WP3JPWBB21D6JRN1AVIE451N4H5YVTJN4M" 
                URL = f"https://api.etherscan.io/api?module=account&action=txlist&apikey={apikey}&sort=desc&address={match_result}"
                if match_result in URL: # address 한줄 씩 받아서 검증 및 중복값 제거
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
                            break
                continue
            elif sel == 2: # 개인키
                global privatekey_list
                privatekey_list = []
                with open('c:\\temp\\'+f'{nowDate}'+'_match_1차_list.txt', '+a') as file:
                    file.write(match_result+'\n')
                    privatekey_list.append(match_result)
                    try:
                        privatekey = w3.eth.account.privateKeyToAccount(match_result) # 개인키 입력하여 주소 확인
                    except Exception:
                        print("error : this is not privatekey")
                    else:
                        global privatekey_result
                        privatekey_result = privatekey.address
                        print(privatekey_result)
                        privatekey_list.append(privatekey_result)
                        csv_file = 'c:\\temp\\result_privateKey.csv'
                        csv_print()
                    file.close()
            elif sel == 4 and len(match_result.split()) == 12: # 니모닉 코드(12)
                global mnemonic_list
                mnemonic_list = []
                with open('c:\\temp\\'+f'{nowDate}'+'_match_1차_list.txt', '+a') as file:
                    file.write(match_result+'\n')
                    print("1차 검색 완료", match_result)
                    mnemonic_list.append(match_result)
                    try:
                        mnemonic = w3.eth.account.from_mnemonic(match_result)  # 니모닉 코드 입력하여 주소 확인
                    except eth_utils.exceptions.ValidationError:
                    #except ValidationError:
                        print("error : this is not mnemonic")
                    else:
                        global mnemonic_result
                        mnemonic_result = mnemonic.address
                        print(mnemonic_result)
                        mnemonic_list.append(mnemonic_result)
                        csv_file = 'c:\\temp\\result_mnemonic.csv'
                        csv_print()
                    file.close()
            elif sel == 5 and len(match_result.split()) == 24: # 니모닉 코드(24)
                file.write(match_result+'\n')
                file.close()
        mm.close()
        
def csv_print():
    with open(csv_file, '+a', encoding='utf-8-sig') as csvfile:
        #writer = csv.writer(csvfile, fieldnames=['timeStamp', 'to', 'hash', 'isError', 'gas', 'methodId', 'blockNumber', 'cumulativeGasUsed', 'blockHash', 'gasPrice', 'contractAddress', 'nonce', 'transactionIndex', 'confirmations', 'value', 'from', 'functionName', 'input', 'txreceipt_status', 'gasUsed'])
        writer = csv.writer(csvfile)
        #writer.writeheader()
        if sel == 1:
            writer.writerow([ts_result, to_result, hx_result])
        elif sel == 2:
            writer.writerow(privatekey_list)
        elif sel == 4:
            writer.writerow(mnemonic_list)
        csvfile.close()

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