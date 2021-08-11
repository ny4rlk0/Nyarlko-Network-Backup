#Nyarlko Network Backup Service
#https://github.com/ny4rlk0/Nyarlko-Network-Backup/
from posixpath import basename;from zipfile import ZipFile;import os;from datetime import date;from datetime import datetime;from shutil import copy2;import subprocess as sp;
user="enter_your_username";password="enter_your_password";networkPath=f"\\\\192.168.1.1\\unity\\Projects"
dirName="C://Users//Guest//Desktop//SHARES";backupName="Backup"
def today():
    now = datetime.now()
    clock=now.strftime("%H.%M")
    day=date.today().strftime("%A")
    digitday=date.today().strftime("%d")
    month=date.today().strftime("%B")
    year=date.today().strftime("%Y")
    return digitday,day,month,year,clock
def upload_file(backupPath):
    sp.Popen("NET USE * //delete", stdout=sp.DEVNULL, stderr = sp.DEVNULL , stdin = sp.DEVNULL)
    accessNetworkDrive = 'NET USE ' + networkPath + ' /User:' + user + ' ' + password
    sp.Popen(accessNetworkDrive, stdout=sp.DEVNULL, stderr = sp.DEVNULL , stdin = sp.DEVNULL)
    copy2(backupPath,networkPath)
def backup():
    backupname=backupName+" "+str(today())+".zip"
    with ZipFile (backupname,'w') as zip:
        for folderName,subFolders,fileNames in os.walk(dirName):
            for fileName in fileNames:
                filePath=os.path.join(folderName,fileName)
                zip.write(filePath,basename(filePath))
    backupPath=os.getcwd()+"\\"+backupname
    upload_file(backupPath)
backup()
