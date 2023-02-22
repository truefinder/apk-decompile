__author__ = 'seunghyun.seo'


import sys
import os
import subprocess
import readline


PATH_APKTOOL = "./apktool2-bin/apktool"
PATH_DEX = "./dex2jar-bin/d2j-dex2jar.sh"
PATH_JAVA = "java"


if __name__ == '__main__' :

    if len(sys.argv) < 2 :
        print ("Usage : $python compile.py workspace/<directory-name>-decompiled/ \n")
        exit(0)


    dirpath = sys.argv[1]

    if not os.path.exists(dirpath) :
        print ("Eror : %s is not exist" % dirpath)
        exit(0)

    print ("[1] Start compiling ... ")
    subprocess.call( [PATH_APKTOOL, 'b', '-f', dirpath ] )

    appname = dirpath[dirpath.find('/') +1 : dirpath.find("-decompiled") ]


    print ("[2] Start signing ... ")

    apkpath = dirpath + "/dist/" + appname
    apksigned = apkpath + "-signed.apk"
    deploypath = "deploy/" + appname + "-signed.apk"
    subprocess.call([PATH_JAVA, '-jar', 'bin/signapk.jar', 'bin/testkey.x509.pem', 'bin/testkey.pk8', apkpath, apksigned  ])
    subprocess.call(["cp", apksigned, deploypath ])

    print ("[3] Moved result to ./deploy ")

    subprocess.call(["ls", "-al", deploypath ])

    print ("[3] Done.")

    print ("[4] Install (via ADB)? ")

    yesno = input("(y/n) : ")
    if yesno == 'y':
        subprocess.call(["adb", "install", "-r", deploypath])
    elif yesno == 'n':
        exit(0)
    else :
        exit(0)


