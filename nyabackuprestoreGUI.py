#Nyarlko Network Backup / Restore Service GUI
from posixpath import basename;import base64;import rsa;import sys;from tkinter.ttk import *;from threading import Thread as core;import time;from tkinter import *;import configparser as cfg;from zipfile import ZipFile;import zipfile;import os;from datetime import date;from datetime import datetime;from shutil import copy2;import subprocess as sp

from rsa.pkcs1 import encrypt;
user="enter_your_username";password="enter_your_password";networkPath=f"\\\\192.168.1.1\\unity\\Projects" #Network Path
dirName="C://Users//Guest//Desktop//SHARES" #Source folder to backup
backupName="[NABS] Backup";compression = zipfile.ZIP_DEFLATED ;backup_list=[]
w=Tk();w.title('Nyarlko Automated Backup System');w.configure(background='black');status='Idle.'
#publicKey,privateKey=rsa.newkeys(1024) #Generate new one and change below for better security.
#print("Pub: "+str(publicKey))#;print("Prv: "+str(privateKey))
publicKey=rsa.PublicKey(93210106885308409673894147092817318540212544310203232607163836869322642798656241116149958978716165252579302990376441913575114718192641469813434041390632395005863940670390000350781400541721230908214485357175702643894061842885526098036566283186227390908535521521468214114398274677753683561918267377895059635759, 65537)
privateKey=rsa.PrivateKey(93210106885308409673894147092817318540212544310203232607163836869322642798656241116149958978716165252579302990376441913575114718192641469813434041390632395005863940670390000350781400541721230908214485357175702643894061842885526098036566283186227390908535521521468214114398274677753683561918267377895059635759, 65537, 66272660490024199544905100509391772464688403912637747071059299427801504287486227128022943353086609888680253619216184198954172765363420885437181805231702470461960843476751027527233864135148094718943620449467333807396167122239999140524479715153256421379321279498016053989894614170482896468753909274464965830769, 44148962656467641997255269035201270095410858384556956919777906414579728115404314512598651806960418067521895211843094577970680919896506342422192638391888224179382537, 2111263805009323615927154438436683493141199441169831062117901381899226963175119191779051811591930732161790116716929465694361259510399201312134007)
#For safety reasons public release .exe will not have the same Public/Private keys.
def encrypt(data):
    return_data=rsa.encrypt(bytes(data,'ISO-8859-1'),publicKey)
    return return_data
def decrypt(data):
    return_data=rsa.decrypt(data,privateKey)
    return return_data
def readConfig():
    global user,password,networkPath,dirName,backupName,stat
    f=open('nbs.settings','rb')
    content=f.read()
    a=content.split(b'data_ayirma_dizisi')
    user=decrypt(a[0]).decode('ISO-8859-1')
    password=decrypt(a[1]).decode('ISO-8859-1')
    networkPath=decrypt(a[2]).decode('ISO-8859-1')
    dirName=decrypt(a[3]).decode('ISO-8859-1')
    backupName=decrypt(a[4]).decode('ISO-8859-1')
    usre.delete(0,END);pwe.delete(0,END);npe.delete(0,END);dne.delete(0,END);bne.delete(0,END)
    usre.insert(0, user);pwe.insert(0, password);npe.insert(0, networkPath);dne.insert(0, dirName);bne.insert(0, backupName)
    try:list_backups()
    except:pass
def createExampleConfig():
    global stat
    f=open('nbs.settings','wb')
    values=[user,password,networkPath,dirName,backupName]
    for value in values:
        print(value)
        f.write(encrypt(value)+b'data_ayirma_dizisi')
    f.close()
    stat["text"] = "Example config created."
def writeConfig():
    global stat
    user=usre.get();password=pwe.get()
    networkPath=npe.get();dirName=dne.get();backupName=bne.get()
    values=[user,password,networkPath,dirName,backupName]
    os.remove('nbs.settings')
    f=open('nbs.settings','wb')
    for value in values:
        f.write(encrypt(value)+b'data_ayirma_dizisi')
    f.close()
    stat["text"]="Settings saved.";time.sleep(4);readConfig()
def today():
    now = datetime.now()
    clock=now.strftime("%H.%M")
    day=date.today().strftime("%A")
    digitday=date.today().strftime("%d")
    month=date.today().strftime("%B")
    year=date.today().strftime("%Y")
    return digitday,day,month,year,clock
def access_network_drive():
    global stat,backupButton,saveConfigButton
    n=sp.DEVNULL;stat["text"]="Deleting active network shares...";time.sleep(4)
    sp.Popen("NET USE * //delete",stdout=n,stderr=n,stdin=n)
    accessNetworkDrive='NET USE '+networkPath+' /User:'+user+' '+password
    stat["text"] = "Accessing network drive..";time.sleep(4)
    sp.Popen(accessNetworkDrive,stdout=n,stderr=n,stdin=n)
def upload_file(backupPath):
    global stat,backupButton,saveConfigButton,restoreButton
    access_network_drive();time.sleep(2)
    stat["text"] = "Uploading backup..";time.sleep(4)
    copy2(backupPath,networkPath)
    stat["text"] = "Upload finished...";time.sleep(4)
    stat["text"] = "Updating backup list...";time.sleep(4)
    try:list_backups()
    except:pass
    stat["text"] = "Successfully updated backup list...";time.sleep(4)
    backupButton["state"]="active";saveConfigButton["state"]="active";restoreButton["state"]="active"
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
def list_backups():
    global backup_list,backupComboboxList
    backup_list=[]
    selected_backup_name=backupComboboxList.get()
    access_network_drive()
    selected_backup=os.path.join(networkPath, selected_backup_name)
    backup_exists=os.path.exists(selected_backup)
    if not backup_exists:
        backupComboboxList.delete(0,END)
    if backup_exists:
        for file in os.listdir(networkPath): #Find backup files ending with .zip in networkDirectory
            if file.endswith(".zip"):
                backup_list.append(file)
    for b in backup_list: #Update Combobox list
        backupComboboxList["values"] = backup_list
def restore():
    global backupComboboxList,backupButton,saveConfigButton,restoreButton,stat
    list_backups()
    selected_backup_name=backupComboboxList.get()
    selected_backup=os.path.join(networkPath, selected_backup_name)
    copy_dir=dirName+"//"+selected_backup_name
    zip_dir=dirName+"//"+selected_backup_name+"//"+selected_backup_name
    copydir_exists=os.path.exists(copy_dir)
    if not copydir_exists:
        os.mkdir(copy_dir)
    backup_exists=os.path.exists(selected_backup)
    if backup_exists:
        copy2(selected_backup,copy_dir)
        with zipfile.ZipFile(zip_dir, 'r') as z:
            z.extractall(copy_dir)
        os.remove(zip_dir)
        stat["text"] = "Backup restored";time.sleep(2)
    else:stat["text"] = "Backup not found";time.sleep(2)
    backupButton["state"]="active";saveConfigButton["state"]="active";restoreButton["state"]="active"
def upload_proccess_handler():
    global backupButton,saveConfigButton,restoreButton,stat
    stat["text"] = "Compressing folder.."
    backupButton["state"] = "disabled";saveConfigButton["state"] = "disabled";restoreButton["state"] = "disabled"
    compress_proccess=core(target=compress_folder);compress_proccess.daemon=True 
    compress_proccess.start()
def restore_proccess_handler():
    global backupButton,saveConfigButton,restoreButton,stat
    stat["text"] = "Restoring from backup.."
    backupButton["state"] = "disabled";saveConfigButton["state"] = "disabled";restoreButton["state"] = "disabled"
    restore_proccess=core(target=restore);restore_proccess.daemon=True 
    restore_proccess.start()
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
#BackupList
bkl=Label (w, text="Existing Backups:" ,bg="black",fg="white",font="none 12 bold");bkl.grid(row=7,column=0,sticky=W)
backupComboboxList=Combobox(w,width=65,values=list_backups,state="readonly")
backupComboboxList.grid(row=7,column=1)
#BackupButton
backupButton=Button(w,text="Backup",width=12,font="none 12 bold",command=upload_proccess_handler)
backupButton.grid(row=8,column=0,sticky=W)
#ConfigSaveButton
saveConfigButton=Button(w,text="Save Config",width=12,font="none 12 bold",command=writeConfig)
saveConfigButton.grid(row=8,column=1,sticky=W)
#RestoreButton
restoreButton=Button(w,text="Restore",width=12,font="none 12 bold",command=restore_proccess_handler)
restoreButton.grid(row=8,column=2,sticky=W)
#Status
stat=Label (w, text=status ,bg="black",fg="white",font="none 12 bold");stat.grid(row=9,column=0)
settings_exists=os.path.exists(os.getcwd()+'\\nbs.settings')
if not settings_exists:createExampleConfig();readConfig()
else:
    readConfig();
    try:
        list_backups();
    except:pass
#Run the main loop
w.mainloop()
sys.exit(0)
