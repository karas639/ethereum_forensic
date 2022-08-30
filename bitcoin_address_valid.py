<<<<<<< HEAD
from cryptoaddress import get_crypto_address
import csv

#datafile = open('F:\\ethereum_forensic\\ethereum_address_scan.csv','r')
#new_file = open('ethereum_address_scan_v2.csv', 'w', newline='')
#datafile_read = csv.reader(datafile)
with open('E:\\bitcoin_address.csv', 'r') as f:
    while f:
        line = f.readline()
        #print(line)
        try:
            bitcoin_address = get_crypto_address('BTC', line)     
            #writeresult= csv.writer(new_file)
            print('The address "%s" is valid.' % str(bitcoin_address))
        except ValueError:
            #print('The address "%s" is invalid.' % str(ethereum_address))
            pass

#atafile.close()
# Prints 'The address "17VZNX1SN5NtKa8UQFxwQbFeFc3iqRYhem" is valid.'
=======
from cryptoaddress import get_crypto_address
import csv

#datafile = open('F:\\ethereum_forensic\\ethereum_address_scan.csv','r')
#new_file = open('ethereum_address_scan_v2.csv', 'w', newline='')
#datafile_read = csv.reader(datafile)
with open('E:\\bitcoin_address.csv', 'r') as f:
    while f:
        line = f.readline()
        #print(line)
        try:
            bitcoin_address = get_crypto_address('BTC', line)     
            #writeresult= csv.writer(new_file)
            print('The address "%s" is valid.' % str(bitcoin_address))
        except ValueError:
            #print('The address "%s" is invalid.' % str(ethereum_address))
            pass

#atafile.close()
# Prints 'The address "17VZNX1SN5NtKa8UQFxwQbFeFc3iqRYhem" is valid.'
>>>>>>> 9c22d7588e34949bd7802bebb4502d25eceb7acc
