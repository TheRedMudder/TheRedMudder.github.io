import os
import errno
import shutil
import glob
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred
def replacewith(filename,filetype,old_text,new_text):
    f1 = open(filename + filetype, 'r')
    f2 = open(filename + '_temp'+filetype, 'w')
    for line in f1:
        f2.write(line.replace(old_text, new_text))
    f1.close()
    f2.close()
    shutil.copy(filename + '_temp'+filetype, filename +filetype)
    silentremove(filename + '_temp'+filetype)
def replacefolder(filetype,old_text,new_text,foldersub=""):
    replacequefiles = glob.glob(foldersub+"*" + filetype)
    for replaceque in replacequefiles:
        replacewith(replaceque[:-len(filetype)],filetype,old_text,new_text)
def replaceAllfolder(filetype,old_text,new_text):
    allfoldersub=next(os.walk('.'))[1]
    print(allfoldersub);
    for foldersub in allfoldersub:
        replacefolder(filetype, old_text, new_text,"./" +foldersub+"/");
    replacefolder(filetype, old_text, new_text)

# Fix Host
replaceAllfolder(".html",'localhost','theredmudder.github.io');
#Fix Dynamic Problem
replaceAllfolder(".html",'?ver=4.7.5','');
#Fixes Broken Image
replaceAllfolder(".html",'http://theredmudder.github.io/me/wp-content/uploads/2016/09/face.jpg','https://demo.themegrill.com/flash-one-page/wp-content/uploads/sites/93/2016/09/face.jpg');
#Removes Extra Index Files
checkforgarbage = glob.glob("*.html");
for checkgarb in checkforgarbage:
    if (("index" in checkgarb) and (len(checkgarb)>10)):
        silentremove(checkgarb);

