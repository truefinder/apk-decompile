__author__ = 'seunghyun.seo'

import shutil
import sys
import os
import subprocess

PATH_APKTOOL = "./apktool2-bin/apktool"
PATH_DEX = "./dex2jar-bin/d2j-dex2jar.sh"
PATH_MONO = "/Applications/Unity/MonoDevelop.app/Contents/Frameworks/Mono.framework/Versions/Current/bin/mono" 
PATH_UNITY_DECODE = "./bin/unity_decode"
PATH_UNITY_LOADER = "./bin/unity_loader.py"
#ANDROID_PLATFORM = "armeabi-v7a" 
ANDROID_PLATFORM = "armeabi-v7a" 

if __name__ == '__main__' :

    if len(sys.argv) < 2 :
        print ("Usage : $python decompile.py workspace/<filename.apk> \n")
        exit(0)


    filepath = sys.argv[1]

    if not os.path.exists(filepath) :
        print ("Eror : %s is not exist" % filepath)
        exit(0)

    print ("[1] Start decompiling ... ")

    savepath = filepath + "-decompiled"
#subprocess.call( [PATH_APKTOOL, 'd', filepath, '-f', '-r', '-o', savepath ] )
    subprocess.call( [PATH_APKTOOL, 'd', filepath, '-f',  '-o', savepath ] )

    print ("[2] Start changing dex to jar sources ... ")

    jarpath = filepath + "-dex2jar.jar"
    subprocess.call([PATH_DEX, filepath, '-f', '-o', jarpath ])

    print ("[3] Start decompile unity dll to .cs source files ..." )
    refpath = savepath + "/assets/bin/Data/Managed/"
    dllpath = savepath + "/assets/bin/Data/Managed/Assembly-CSharp.dll"
    metapath = savepath + "/assets/bin/Data/Managed/Metadata/global-metadata.dat"
    outpath = filepath + "-dll" 

    if os.path.isfile(dllpath):
        print ("Dll found " )
        
        if os.path.exists( outpath ):
            shutil.rmtree( outpath )

        shutil.copytree( refpath, outpath ) 
        # subprocess.call([PATH_MONO, "./bin/ILSpyMac.exe", '-n', 'sources', '-l',  refpath, outpath, '-D', 'Assembly-CSharp.dll' ])
     
    else:
        print ("No Unity dll files ") 
 

    print ("[4] Start to copy .so files to so directory ..." )
    outpath = filepath + "-so" 
    sopath = savepath + "/lib" 

    if os.path.exists( outpath ):
       shutil.rmtree( outpath )

    shutil.copytree( sopath, outpath )


    print ("[5] Start to global-metadata.dat .so to so directory ..." )
    if os.path.isfile(metapath):
        print ("global-metadata found ") 
        platform_path = outpath + "/" + ANDROID_PLATFORM 
        print (platform_path ) ; 
        shutil.copy( metapath, platform_path   ) 

        print ("Il2CppDumper 4.6 / select 3.auto (plug) / Unity version 2018.3 ")
        subprocess.call(['mono', './il2cppdumper/Il2CppDumper.exe']) 


        
        shutil.copy( PATH_UNITY_DECODE, platform_path ) 
        shutil.copy( PATH_UNITY_LOADER, platform_path ) 
        print (platform_path + "/unity_decode" )
        os.chdir( platform_path ) 
        print (os.getcwd() )
        subprocess.call([ "./unity_decode" ], "./global-metadata.dat" )
     
 
    print ("[6] Done")


