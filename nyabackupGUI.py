#Nyarlko Network Backup Service
from posixpath import basename;import sys;from threading import Thread as core;import time;from tkinter import *;import configparser as cfg;from zipfile import ZipFile;import zipfile;import os;from datetime import date;from datetime import datetime;from shutil import copy2;import subprocess as sp;
user="enter_your_username";password="enter_your_password";networkPath=f"\\\\192.168.1.1\\unity\\Projects" #Network Path
dirName="C://Users//Guest//Desktop//SHARES" #Source folder to backup
backupName="Backup";compression = zipfile.ZIP_DEFLATED
w=Tk();w.title('Nyarlko Automated Backup System');w.configure(background='black');status='Idle.'
def readConfig():
    global user,password,networkPath,dirName,backupName,status
    r=cfg.RawConfigParser()
    r.read('nbs.settings')
    user=str(r['config'] ['user'])
    password=str(r['config'] ['password'])
    networkPath=str(r['config'] ['networkPath'])
    dirName=str(r['config']['dirName'])
    backupName=str(r['config']['backupName'])
    status='Settings loaded.'
    return user,password,networkPath,dirName,backupName
def createExampleConfig():
    global status
    r=cfg.RawConfigParser()
    r.add_section('config')
    r.set('config','user',user)
    r.set('config','password',password)
    r.set('config','networkPath',networkPath)
    r.set('config','dirName',dirName)
    r.set('config','backupName',backupName)
    makeConfig=open('nbs.settings','w')
    r.write(makeConfig)
    makeConfig.close()
    status='Example config created.'
def writeConfig():
    global status
    r=cfg.RawConfigParser()
    r.add_section('config')
    r.set('config','user',str(t.get()))
    r.set('config','password',str(t1.get()))
    r.set('config','networkPath',str(t2.get()))
    r.set('config','dirName',str(t3.get()))
    r.set('config','backupName',str(t4.get()))
    makeConfig=open('nbs.settings','w')
    r.write(makeConfig)
    makeConfig.close()
    status='Settings saved.'
    readConfig()
def today():
    now = datetime.now()
    clock=now.strftime("%H.%M")
    day=date.today().strftime("%A")
    digitday=date.today().strftime("%d")
    month=date.today().strftime("%B")
    year=date.today().strftime("%Y")
    return digitday,day,month,year,clock
def upload_file(backupPath):
    global stat,backupButton,saveConfigButton
    stat["text"] = "Deleting active network shares..."
    time.sleep(2)
    sp.Popen("NET USE * //delete", stdout=sp.DEVNULL, stderr = sp.DEVNULL , stdin = sp.DEVNULL)
    accessNetworkDrive = 'NET USE ' + networkPath + ' /User:' + user + ' ' + password
    stat["text"] = "Uploading backup.."
    time.sleep(2)
    sp.Popen(accessNetworkDrive, stdout=sp.DEVNULL, stderr = sp.DEVNULL , stdin = sp.DEVNULL)
    copy2(backupPath,networkPath)
    stat["text"] = "Upload finished..."
    time.sleep(2)
    backupButton["state"] = "enable"
    saveConfigButton["state"] = "enable"
def compress_folder():
    fileNumber=0
    backupname=backupName+" "+str(today())+".zip"
    with ZipFile (backupname,'w') as zip:
        for folderName,subFolders,fileNames in os.walk(dirName):
            for fileName in fileNames:
                print(str(fileNumber)+f" {fileName}")
                filePath=os.path.join(folderName,fileName)
                zip.write(filePath,basename(filePath),compress_type=compression)
                fileNumber=fileNumber+1
    backupPath=os.getcwd()+"\\"+backupname
    status='Compression Finished!'
    time.sleep(2)
    upload_file(backupPath)
def daemon_handler():
    global backupButton,saveConfigButton,stat
    stat["text"] = "Compressing folder.."
    backupButton["state"] = "disabled"
    saveConfigButton["state"] = "disabled"
    compress_proccess = core(target=compress_folder)#, args=(1,)) Flask Server.
    compress_proccess.daemon=True #To kill when its needed neccesary
    compress_proccess.start() #Flask sunucusunu ayrı bir çekirdekte çalıştır.
print(os.getcwd()+'\\nbs.settings')
settings_exists=os.path.exists(os.getcwd()+'\\nbs.settings')
if not settings_exists:createExampleConfig()
else:readConfig()
#UserBox
Label (w, text="Username:" ,bg="black",fg="white",font="none 12 bold") .grid(row=0,column=0,sticky=W)
t=Entry(w,width=40,bg="white")
t.insert(0, user)
t.grid(row=0,column=1,sticky=W)
#PasswordBox
Label (w, text="Password:" ,bg="black",fg="white",font="none 12 bold") .grid(row=1,column=0,sticky=W)
t1=Entry(w,width=40,bg="white")
t1.insert(0, password)
t1.grid(row=1,column=1,sticky=W)
#NetworkBox
Label (w, text="Network Path:" ,bg="black",fg="white",font="none 12 bold") .grid(row=2,column=0,sticky=W)
t2=Entry(w,width=40,bg="white")
t2.insert(0, networkPath)
t2.grid(row=2,column=1,sticky=W)
#DirectoryNameBox
Label (w, text="Directory:" ,bg="black",fg="white",font="none 12 bold") .grid(row=3,column=0,sticky=W)
t3=Entry(w,width=40,bg="white")
t3.insert(0, dirName)
t3.grid(row=3,column=1,sticky=W)
#BackupName
Label (w, text="Backup Name:" ,bg="black",fg="white",font="none 12 bold") .grid(row=4,column=0,sticky=W)
t4=Entry(w,width=40,bg="white")
t4.insert(0, backupName)
t4.grid(row=4,column=1,sticky=W)
global backupButton,saveConfigButton,stat
#Backup Button
backupButton=Button(w,text="Backup",width=12,font="none 12 bold",command=daemon_handler)
backupButton.grid(row=7,column=0,sticky=W)
#DosyaKaydetButton
saveConfigButton=Button(w,text="Save Config",width=12,font="none 12 bold",command=writeConfig)
saveConfigButton.grid(row=7,column=1,sticky=W)
#Durum
stat=Label (w, text="Status: "+status+"." ,bg="black",fg="white",font="none 12 bold")
stat.grid(row=8,column=0)
#Run the main loop
w.mainloop()
sys.exit(0)
