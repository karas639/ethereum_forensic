@echo off
cls
title Ethereum Wallet info extract Shell
prompt $T$S$P$G$S

echo ------------------------------------------------- 
echo          Ethereum Wallet Info Extract Kit v1.0       
echo ------------------------------------------------- 

:: -----------------------------------------------------
:: VARIABLEs
:: -----------------------------------------------------

echo ------------------------------------------------- 
echo       python install and pip install       
echo ------------------------------------------------- 

::unzip python-3.12.2-embed-amd64.zip -d python3
cd python3
::curl -O https://bootstrap.pypa.io/get-pip.py
::.\python.exe get-pip.py


echo ------------------------------------------------- 
echo          Current Directory       
echo ------------------------------------------------- 

chdir

echo ------------------------------------------------- 
echo          Install pip packages       
echo ------------------------------------------------- 

.\scripts\pip install --no-index --find-links=..\requirements web3
.\scripts\pip install --no-index --find-links=..\requirements eth_utils
.\scripts\pip install --no-index --find-links=..\requirements numpy
.\scripts\pip install --no-index --find-links=..\requirements urllib3
.\scripts\pip install --no-index --find-links=..\requirements requests

echo ------------------------------------------------- 
echo          memory dump       
echo ------------------------------------------------- 


.\python ..\eth_scan_v2.py

pause

:: -----------------------------------------------------
:: END
:: -----------------------------------------------------
:END
echo END TIME : %DATE% %TIME% >> %_LOG%
echo.
echo It's done!
