@echo off

:HTML
REM https://windows.php.net/downloads/releases/archives/
echo Running Python code...
REM Namestitev Python
REM https://www.python.org/downloads/windows/
REM Download Windows embeddable package (64-bit)
REM https://www.python.org/ftp/python/3.13.2/python-3.13.2-embed-amd64.zip

REM   C:\Osebno\SavliM86\util\python3\python313._pth
REM         python313.zip
REM         .
REM         Lib
REM         Lib\site-packages

REM Download get-pip.py from pip’s official site. https://pip.pypa.io/en/stable/installation/
REM c:\Osebno\SavliM86\util\wget\wget.exe -O c:\Osebno\SavliM86\util\python3\get-pip.py https://bootstrap.pypa.io/get-pip.py
rem Cd c:/Osebno/SavliM86/util/python3/
rem dir get-pip.py
REM C:\Osebno\SavliM86\util\python3\python.exe get-pip.py
REM C:\Osebno\SavliM86\util\python3\python.exe -m pip --version
REM C:\Osebno\SavliM86\util\python3\python.exe -m pip install lxml
mkdir c:\temp\sword\html  1>NUL
C:\Osebno\SavliM86\util\python3\python.exe "m:\SloKJVA\github\osis2html\osis2html.py"

pause
echo.
echo   Odpre Firefox 
c:
cd C:/Temp/sword/html
start /wait "" "C:\Program Files\Mozilla Firefox\firefox.exe" http://localhost:8000
echo   Odpre lokalni web server
cd C:/Temp/sword/html && python -m http.server 8000
pause