#### import struct
import re
import os
import sys
import csv
import datetime
import requests
import urllib3
import json
import multiprocessing
#from multiprocessing import Pool
import numpy as np
import eth_utils
from mmap import ACCESS_READ, mmap
#from web3.auto import w3
from web3 import Web3

infura_url = "https://mainnet.infura.io/v3/1656dc090b3f4badb4591c849da213f8"
w3 = Web3(Web3.HTTPProvider(infura_url))

t=print(w3.is_connected())
print(t)


now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d_%H')
#nowDate = now.strftime('%Y-%m-%d_%H_%M_%S')
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
w3.eth.account.enable_unaudited_hdwallet_features()


def showmenu():  # 메뉴 선택 함수
    print()
    print("[Ethereum Aritifacts search choose menu]")
    for i in range(0, len(menu)):
        print(i+1, ".", menu[i])
    print()
    
path = input("write full path: ")
try:
    handle = open(path, 'rb+')
except IOError:
    print('IOError : File path is invalid')
    sys.exit()
print(path)

def artifacts():
    # re.IGNORCASE : 대소문자 구별 없이 매치를 수행할 때 사용
    # re.DOTALL : \n 문자도 포함하여 매치
    # re.MULTILINE : ^, $ 메타 문자를 문자열의 각 줄마다 적용
    if sel == 1: #주소, 0x[0-9A-Fa-f]{40,44}, ^0x[a-fA-F0-9]{40}, ^(0x)?[0-9a-fA-F]{40}$
        p = re.compile(rb'^0x[0-9a-fA-F]{40}$', re.IGNORECASE | re.DOTALL | re.MULTILINE )
    elif sel == 2: #개인키
        p = re.compile(rb'^[0-9a-fA-F]{64}$', re.IGNORECASE | re.DOTALL | re.MULTILINE)
        #p = re.compile(rb'[0-9a-fA-F]{64}', re.IGNORECASE | re.DOTALL | re.MULTILINE) 
 
    elif sel == 3: #키스토어
        #p = re.compile(rb'"([address"]*)":"([a-fA-F0-9]{40})","([crypto"]*)":', re.IGNORECASE | re.MULTILINE)
        p = re.compile(rb'UTC--[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}.[0-9]{3}Z--[a-fA-F0-9]{40}', re.IGNORECASE | re.DOTALL)
    elif sel == 4: # 니모닉 코드(12)
        p = re.compile(rb'[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}', re.IGNORECASE | re.DOTALL) # 나모닉 코드 12자리
    #elif sel == 5: # 니모닉 코드(24)
    #    p = re.compile(rb'[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}\s[a-z]{3,8}', re.IGNORECASE | re.MULTILINE) # 나모닉 코드 24자리
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
                #with open('c:\\temp\\'+f'{nowDate}'+'_ethereum_address_scan_result_1차', '+a') as file:
                #    file.write(match_result+'\n')
                #    file.close()        
                apikey = "WP3JPWBB21D6JRN1AVIE451N4H5YVTJN4M" 
                URL = f"https://api.etherscan.io/api?module=account&action=txlist&apikey={apikey}&sort=desc&address={match_result}"
                global resp
                try:
                    if match_result in URL: # address 한줄 씩 받아서 검증 및 중복값 제거
                        #http = urllib3.PoolManager()
                        #req = http.request('GET', URL)
                        #resp = json.loads(req.data.decode('utf-8'))
                        resp = requests.get(URL).json() # http get 요청을 resp 변수에 json 형태로 선언
                        global csv_file
                        csv_file = 'c:\\temp\\'+f'{nowDate}'+'_ethereum_address_scan_result_2차.csv'    
                        for key, value in resp.items():  # apikey error test
                            #if value == "1":
                            if resp["message"] == "OK":
                                #global api_result, ts_result, from_result, to_result, hx_result
                                global from_result, to_result, ts_result, hx_result
                                #status = resp["message"]
                                data = resp["result"] # result 결과인 value만 변수에 담기
                                api_result = dict(data[0])
                                ts_result = api_result.get('timeStamp')
                                from_result = api_result.get('from')
                                to_result = api_result.get('to')
                                hx_result = api_result.get('hash')
                                print(from_result)
                                csv_print()
                                break
                            elif resp["message"] == "No":
                                print("this private key's address is no transaction..")
                    #continue
                except Exception:
                    print("error : match result is wrong")
            elif sel == 2: # 개인키
                with open('c:\\temp\\'+f'{nowDate}'+'_ethereum_privatekey_scan_result_1차.txt', '+a') as file:
                    file.write(match_result+'\n')
                    print("1차 매칭 : ", match_result)
                    global privatekey_list
                    privatekey_list = []
                    privatekey_list.append(match_result)
                    try:
                        privatekey = w3.eth.account.from_key(match_result) # 임의의 개인키스트링 입력하여 유효한 주소 확인
                        #privateKeyToAccount --> from_key로 수정 
                        #privatekey = web3.eth.account.create(match_result)
                        #w3.eth.defaultAccount = web3.eth.account.privateKeyToAccount(match_result).address
                        #print(web3.eth.defaultAccount)
                    except Exception as e:
                        print(e, "error : this is not privatekey")
                    else:
                        global privatekey_result
                        privatekey_result = privatekey.address
                        print("match : ", privatekey_result)
                        privatekey_list.append(privatekey_result)
                        csv_file = 'c:\\temp\\'+f'{nowDate}'+'_ethereum_privatekey_scan_result_2차.csv'
                        csv_print()
                        ### 개인키에 해당하는 주소값 3차 검증
                        f = open('c:\\temp\\'+f'{nowDate}'+'_ethereum_privatekey_scan_result_2차.csv','r', encoding='utf-8-sig')
                        private_reader = csv.reader(f)
                        for line in private_reader:
                            match_private = str(line[1])
                            #print("3차 검증 주소", match_private)
                            apikey = "WP3JPWBB21D6JRN1AVIE451N4H5YVTJN4M" 
                            URL1 = f"https://api.etherscan.io/api?module=account&action=txlist&apikey={apikey}&sort=desc&address={match_private}"
                            #print(URL1)
                            try:
                                if match_private in URL1: # address 한줄 씩 받아서 etherscan api로 재검증
                                    headers = {'User-Agent': 'Mozilla/5.0'} # header 선언, http 요청 브라우저는 Mozilla.
                                    http = urllib3.PoolManager()
                                    req = http.request('GET', URL1)
                                    resp = json.loads(req.data.decode('utf-8'))
                                    #resp = requests.get(URL1).json() # http get 요청을 resp 변수에 json 형태로 선언
                                    #print("resp 출력", resp)
                                    global csv_file2
                                    csv_file2 = 'c:\\temp\\'+f'{nowDate}'+'_ethereum_privatekey_scan_result_3차.csv'    
                                    for key, value in resp.items():  # apikey error test
                                    #if value == "1":
                                        if resp["message"] == "OK":
                                            global api_result1, ts_result1, from_result1, to_result1, hx_result1
                                            #status = resp["message"]
                                            data = resp["result"] # result 결과인 value만 변수에 담기
                                            api_result1 = dict(data[0])
                                            #print("api result", api_result1)
                                            ts_result1 = api_result1.get('timeStamp')
                                            from_result1 = api_result1.get('from')
                                            to_result1 = api_result1.get('to')
                                            hx_result1 = api_result1.get('hash')
                                            #print(from_result)
                                            csv_print2()

                                            print("csv2")
                                            break
                                        elif resp["message"] == "No":
                                            print("this private key's address is no transaction..")
                                #continue
                            except Exception:
                                print("error : match result is wrong")
                        f.close()
                        ####
                    file.close()
            elif sel == 4 and len(match_result.split()) == 12: # 니모닉 코드(12)
                with open('c:\\temp\\'+f'{nowDate}'+'_ethereum_mnemonic_scan_result_1차.txt', '+a') as file:
                    file.write(match_result+'\n')
                    print("1차 검색 값 : ", match_result)
                    global mnemonic_list
                    mnemonic_list = []
                    mnemonic_list.append(match_result)
                    try:
                        mnemonic = w3.eth.account.from_mnemonic(match_result)  # 니모닉 코드 입력하여 주소 확인
                    except eth_utils.exceptions.ValidationError:
                    #except ValidationError:
                        print("error : this is not mnemonic")
                    else:
                        global mnemonic_result
                        mnemonic_result = mnemonic.address
                        print("match : ", mnemonic_result)
                        mnemonic_list.append(mnemonic_result)
                        csv_file = 'c:\\temp\\'+f'{nowDate}'+'_ethereum_mnemonic_scan_result_2차.csv'
                        csv_print()
                    file.close()
            #elif sel == 5 and len(match_result.split()) == 24: # 니모닉 코드(24)
            #    file.write(match_result+'\n')
            #    file.close()
        mm.close()
        
def csv_print():
    with open(csv_file, '+a', encoding='utf-8-sig', newline="") as csvfile:
        #writer = csv.writer(csvfile, fieldnames=['timeStamp', 'to', 'hash', 'isError', 'gas', 'methodId', 'blockNumber', 'cumulativeGasUsed', 'blockHash', 'gasPrice', 'contractAddress', 'nonce', 'transactionIndex', 'confirmations', 'value', 'from', 'functionName', 'input', 'txreceipt_status', 'gasUsed'])
        writer = csv.writer(csvfile)
        #writer.writeheader()
        if sel == 1:
            writer.writerow([ts_result, from_result, to_result, hx_result])
        elif sel == 2:
            writer.writerow(privatekey_list)
        elif sel == 4:
            writer.writerow(mnemonic_list)
        csvfile.close()

def csv_print2():
    with open(csv_file2, '+a', encoding='utf-8-sig', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([ts_result1, from_result1, to_result1, hx_result1])
        csvfile.close()
        
        outfile = open('c:\\temp\\'+f'{nowDate}'+'_이더리움개인키_최종.csv', '+a')
        outfile2 = open(csvfile, 'r')

        lines = outfile2.readlines(100000)
        lines = list(set(lines))
        lines.sort()
        for line in lines:
            print(line)
            outfile.write(line)
    
        outfile.close()
        outfile2.close()        

if __name__ == '__main__':
    #menu = ("address", "private key", "keystore", "mnemonic code(12)", "mnemonic code(24)")
    menu = ("address", "private key", "keystore", "mnemonic code(12)")
    while True:
        showmenu()
        sel = int(input("Choose Menu number (Exit 0) : "))
        if sel == 0:
            break
        elif(sel>=1 and sel <= len(menu)):
            #transactions("")
            artifacts()
            #pool = multiprocessing.Pool(processes=4)
            #pool.map(artifacts, artifacts().resp)
            #pool.close()
            #pool.join()
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