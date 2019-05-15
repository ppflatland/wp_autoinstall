
#!/usr/bin/python2
#-*- coding: utf-8 -*-

import re
import os, sys
import pwd
import subprocess
import time
from os import stat
from pwd import getpwuid
import shutil
import urllib2
import zipfile
import string
from random import *


#-------Generation password database_name database_user------

filename = '/etc/passwd'
st = os.stat('..')
uid = st.st_uid
gid = pwd.getpwnam("nobody").pw_gid
userinfo = pwd.getpwuid(st.st_uid)
ownername = pwd.getpwuid(st.st_uid).pw_name
gid_ownername = pwd.getpwnam(ownername).pw_gid
#print(ownername)
current_folder_path, current_folder_name = os.path.split(os.getcwd())
characters = string.ascii_letters + string.digits
password =  "".join(choice(characters) for x in range(randint(8, 16)))
database_name= ownername+"_"+current_folder_name[:2]+"by"
database_user= ownername+"_"+current_folder_name[:2]+"by"
privileges = "ALL%20PRIVILEGES"
cmd1 = ('uapi --user=%s Mysql create_database name=%s' %(ownername, database_name))
cmd2 = ('uapi --user=%s Mysql create_user name=%s password=%s' %(ownername, database_user, password))
cmd3 = ('uapi --user=%s Mysql set_privileges_on_database user=%s database=%s privileges=%s' %(ownername, database_user, database_name, privileges))
PIPE = subprocess.PIPE
subprocess.Popen(cmd1, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
subprocess.Popen(cmd2, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
time.sleep(8)
subprocess.Popen(cmd3, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
print "\033[96m Creat database and user!! \033[0m"

#----------------------------------------------------------

url = "https://ru.wordpress.org/wordpress-4.9.8-ru_RU.zip"
file_name = url.split('/')[-1]
u = urllib2.urlopen(url)
f = open(file_name, 'wb')
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0])
print "Downloading: %s Bytes: %s" % (file_name, file_size)
file_size_dl = 0
block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break
    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print ('\033[95m%s\033[0m' %(status)),
print "\033[96m Download successfully!! \033[0m"
f.close()

zip_ref = zipfile.ZipFile(os.path.abspath(file_name), 'r')
zip_ref.extractall(os.getcwd())
zip_ref.close()
print "\033[96m Extract!! \033[0m"

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

f = open (os.path.abspath(r"wordpress/wp-config-sample.php") , "r+" )
config = f.read()
config = re.sub(r'database_name_here','%s'%(database_name), config)
config = re.sub(r'username_here','%s'%(database_user), config)
config = re.sub(r'password_here','%s'%(password), config)
f1 = open (os.path.abspath(r"wordpress/wp-config.php") , "w" )
f1.write(config)
f.close()
f1.close()

src = os.path.abspath("wordpress")
dst = os.getcwd()
copytree(src, dst)

os.chown(os.getcwd(), uid, gid)
for root, dirs, files in os.walk(dst):
  for momo in dirs:
    os.chown(os.path.join(root, momo), uid, gid_ownername)
  for momo in files:
    os.chown(os.path.join(root, momo), uid, gid_ownername)

print "\033[96m Changed ownership successfully!! \033[0m"

os.remove(file_name)
shutil.rmtree("wordpress")
os.remove("wp_autoinstall.py")
