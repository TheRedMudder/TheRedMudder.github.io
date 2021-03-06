import os
import errno
import shutil
import glob
import htmlmin
import codecs;
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred
def replacewith(filename,filetype,old_text,new_text):
    f1 = codecs.open(filename + filetype, 'r',"utf-8")
    f2 = codecs.open(filename + '_temp'+filetype, 'w',"utf-8")
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
def replaceAllfolder(filetype,old_text,new_text,walk_dir='.',recursive=True):
    allfoldersub=next(os.walk(walk_dir))[1]
    print(allfoldersub);
    for foldersub in allfoldersub:
        print("Currently in "+foldersub);
        replacefolder(filetype, old_text, new_text,walk_dir+"/" +foldersub+"/");
        if (recursive==True):
            replaceAllfolder(filetype,old_text,new_text,walk_dir+"/" +foldersub);
    if walk_dir == '.':
        replacefolder(filetype, old_text, new_text)
#Removes Extra Index Files
checkforgarbage = glob.glob("*.html");
for checkgarb in checkforgarbage:
    if (("index" in checkgarb) and (len(checkgarb)>10)):
        silentremove(checkgarb);
#Removes Extra Font Files
checkforgarbage = glob.glob("./wp-content/themes/flash/fonts/*.html");
for checkgarb in checkforgarbage:
    if (("fontawesome" in checkgarb) and (len(checkgarb)>10)):
        silentremove(checkgarb);

# Fix Host
replaceAllfolder(".html",'localhost','www.ronjdias.com');
#Fix Dynamic Problem
replaceAllfolder(".html",'?ver=4.7.5','');
replaceAllfolder(".html",'?ver=2.5.3','');
replaceAllfolder(".html",'?ver=1.0.5','');
replaceAllfolder(".html",'?ver=1.4.1','');
replaceAllfolder(".html",'?ver=1.12.4','');
#Fixes Broken Image
replaceAllfolder(".html",'http://www.ronjdias.com/me/wp-content/uploads/2016/09/face.jpg','https://demo.themegrill.com/flash-one-page/wp-content/uploads/sites/93/2016/09/face.jpg');
#Fix Auto Optomize
replaceAllfolder(".css",'localhost/me','www.ronjdias.com/fa');
replaceAllfolder(".css",'?v=4.6.3','');

#Minify Everything
def minitfile(filename,filetype):
    f1 = codecs.open(filename + filetype, 'r',"utf-8")
    f2 = codecs.open(filename + '_temp'+filetype, 'w',"utf-8")
    # Minify Threw Html
    htmlstr = f1.read();
    htmlout=htmlmin.minify((htmlstr), True, False, False, True, False, True, False, (u'pre', u'textarea'),'pre')
    f1.close();
    f2.write(htmlout);
    f2.close()
    shutil.copy(filename + '_temp'+filetype, filename +filetype)
    silentremove(filename + '_temp'+filetype)
    print(filename +filetype+"Done");
def minitfolder(filetype,foldersub=""):
    replacequefiles = glob.glob(foldersub+"*" + filetype)
    for replaceque in replacequefiles:
        minitfile(replaceque[:-len(filetype)], filetype);
# def minitAllfolder(filetype):
#     allfoldersub=next(os.walk('.'))[1]
#     for foldersub in allfoldersub:
#         minitfolder(filetype, "./" +foldersub+"/");
#     minitfolder(filetype,)
def minitAllfolder(filetype,walk_dir='.',recursive=True):
    allfoldersub=next(os.walk(walk_dir))[1]
    print(allfoldersub);
    for foldersub in allfoldersub:
        print("Minify Currently in "+foldersub);
        minitfolder(filetype, walk_dir+"/" +foldersub+"/");
        if (recursive==True):
            minitAllfolder(filetype, walk_dir+"/" +foldersub)
    if walk_dir == '.':
        minitfolder(filetype, )
minitAllfolder('.html');
