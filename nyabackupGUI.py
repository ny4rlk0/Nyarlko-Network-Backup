#Nyarlko Network Backup Service
from posixpath import basename;import sys;from threading import Thread as core;import time;from tkinter import *;import configparser as cfg;from zipfile import ZipFile;import zipfile;import os;from datetime import date;from datetime import datetime;from shutil import copy2;import subprocess as sp;
user="enter_your_username";password="enter_your_password";networkPath=f"\\\\192.168.1.1\\unity\\Projects" #Network Path
dirName="C://Users//Guest//Desktop//SHARES" #Source folder to backup
backupName="[NABS] Backup";compression = zipfile.ZIP_DEFLATED
w=Tk();w.title('Nyarlko Automated Backup System');w.configure(background='black');status='Idle.'
def readConfig():
    global user,password,networkPath,dirName,backupName,stat
    r=cfg.RawConfigParser()
    r.read('nbs.settings')
    user=str(r['config'] ['user'])
    password=str(r['config'] ['password'])
    networkPath=str(r['config'] ['networkPath'])
    dirName=str(r['config']['dirName'])
    backupName=str(r['config']['backupName'])
    usre.delete(0,END);pwe.delete(0,END);npe.delete(0,END);dne.delete(0,END);bne.delete(0,END)
    usre.insert(0, user);pwe.insert(0, password);npe.insert(0, networkPath);dne.insert(0, dirName);bne.insert(0, backupName)
def createExampleConfig():
    global stat
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
    stat["text"] = "Example config created."
def writeConfig():
    global stat
    r=cfg.RawConfigParser()
    r.add_section('config')
    r.set('config','user',str(usre.get()))
    r.set('config','password',str(pwe.get()))
    r.set('config','networkPath',str(npe.get()))
    r.set('config','dirName',str(dne.get()))
    r.set('config','backupName',str(bne.get()))
    makeConfig=open('nbs.settings','w');r.write(makeConfig);makeConfig.close()
    stat["text"]="Settings saved.";time.sleep(4);readConfig()
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
    n=sp.DEVNULL;stat["text"]="Deleting active network shares...";time.sleep(4)
    sp.Popen("NET USE * //delete",stdout=n,stderr=n,stdin=n)
    accessNetworkDrive='NET USE '+networkPath+' /User:'+user+' '+password
    stat["text"] = "Uploading backup..";time.sleep(4)
    sp.Popen(accessNetworkDrive,stdout=n,stderr=n,stdin=n)
    copy2(backupPath,networkPath)
    stat["text"] = "Upload finished...";time.sleep(4)
    backupButton["state"]="active";saveConfigButton["state"]="active"
def compress_folder():
    global stat
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
    stat["text"] = "Compression finished..";time.sleep(4)
    upload_file(backupPath)
def daemon_handler():
    global backupButton,saveConfigButton,stat
    stat["text"] = "Compressing folder.."
    backupButton["state"] = "disabled";saveConfigButton["state"] = "disabled"
    compress_proccess=core(target=compress_folder);compress_proccess.daemon=True 
    compress_proccess.start()
#UserBox
usr=Label (w, text="Username:" ,bg="black",fg="white",font="none 12 bold");usr.grid(row=0,column=0,sticky=W)
usre=Entry(w,width=40,bg="white");usre.grid(row=0,column=1,sticky=W)
#PasswordBox
pw=Label (w, text="Password:" ,bg="black",fg="white",font="none 12 bold");pw.grid(row=1,column=0,sticky=W)
pwe=Entry(w,width=40,bg="white");pwe.grid(row=1,column=1,sticky=W)
#NetworkBox
np=Label (w, text="Network Path:" ,bg="black",fg="white",font="none 12 bold");np.grid(row=2,column=0,sticky=W)
npe=Entry(w,width=40,bg="white");npe.grid(row=2,column=1,sticky=W)
#DirectoryNameBox
dn=Label (w, text="Directory:" ,bg="black",fg="white",font="none 12 bold");dn.grid(row=3,column=0,sticky=W)
dne=Entry(w,width=40,bg="white");dne.grid(row=3,column=1,sticky=W)
#BackupName
bn=Label (w, text="Backup Name:" ,bg="black",fg="white",font="none 12 bold");bn.grid(row=4,column=0,sticky=W)
bne=Entry(w,width=40,bg="white");bne.grid(row=4,column=1,sticky=W)
#BackupButton
backupButton=Button(w,text="Backup",width=12,font="none 12 bold",command=daemon_handler)
backupButton.grid(row=7,column=0,sticky=W)
#ConfigSaveButton
saveConfigButton=Button(w,text="Save Config",width=12,font="none 12 bold",command=writeConfig)
saveConfigButton.grid(row=7,column=1,sticky=W)
#Status
stat=Label (w, text=status ,bg="black",fg="white",font="none 12 bold");stat.grid(row=8,column=0)
settings_exists=os.path.exists(os.getcwd()+'\\nbs.settings')
if not settings_exists:createExampleConfig();readConfig()
else:readConfig()
#Run the main loop
w.mainloop()
sys.exit(0)
