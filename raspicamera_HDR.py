#!/usr/bin/env python
# Raspberry Pi camera HDR capture and process
# 2015-01-11 Francesco Anselmo
# francesco.anselmo@gmail.com
# francesco.anselmo@arup.com

min_free_space = 100 # minimum free space in MB
ISOs = [100]
speeds = [1000000/8000,1000000/4000,1000000/2000,1000000/1000,1000000/500,
          1000000/250 ,1000000/125, 1000000/60,  1000000/30,  1000000/15,
          1000000/8,   1000000/4,   1000000/2,   1000000,     
          2000000,
          4000000
         ]
cmd_fmt = "raspistill -v -t 1 -vf -hf -w 1024 -h 768" # raspistill command format
#opt_man = "-mm average -awb sun -ifx none -drc off" # raspistill manual options format
opt_man = "-mm spot -awb none -cfx 128:128 -ifx none -drc off"
folder = "/opt/camera"
remove_previous_ldr = True
link_to_webserver = True

import ctypes
import os
import platform
import sys
import time
import picamera

def get_free_space_mb(folder):
    """ Return folder/drive free space (in Mega bytes)
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value/1024/1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize/1024/1024

def main():
    free_space = get_free_space_mb(os.getcwd())
    print("Free space: " + str(free_space) + " MB.")
    time.sleep(2)
    if free_space > min_free_space:
        date_time = time.strftime("%Y-%m-%d_%H%M")
        print(date_time)
        auto_photo_name = os.path.join(folder,"AUTO_"+date_time+".jpg")
        # Automatic photo command
	cmds = [cmd_fmt + " -o " + auto_photo_name ]
        if link_to_webserver:
            if platform.system() != 'Windows':
                cmds.append("rm -f /usr/share/nginx/www/img/current.jpg")
                cmds.append("ln -s %s %s" % (auto_photo_name, os.path.join("/usr/share/nginx/www/img","AUTO"+date_time+".jpg")))
                cmds.append("ln -s %s %s" % (auto_photo_name, "/usr/share/nginx/www/img/current.jpg"))
        # Remove previous LDR images to save space if requested
        if remove_previous_ldr:
            LDR_files = os.path.join(folder,"LDR*.*")
            if platform.system() == 'Windows':
                cmds.append("delete %s" % LDR_files)
            else:
                cmds.append("rm -f %s" % LDR_files)
        # LDR bracketed photo sequence command
        for ISO in ISOs:
            for speed in speeds:
                ldr_photo_name = os.path.join(folder,"LDR_"+date_time+"_"+str(ISO)+"_"+str(speed).zfill(7)+".jpg")
                cmds.append(cmd_fmt + " " + opt_man + " -ISO "+str(ISO)+" -ss "+str(speed)+" -o "+ldr_photo_name) 
        # Enfuse command
        enfuse_name = os.path.join(folder,"ENFUSE_"+date_time+".jpg")
        cmds.append("enfuse -v -o %s %s" % (enfuse_name, os.path.join(folder,"LDR_"+date_time+"_*.jpg")))
        # HDR command
        hdr_name = os.path.join(folder,"HDR_"+date_time+".hdr")
        tm_name = os.path.join(folder,"HDR_"+date_time+".jpg")
        cmds.append("luminance-hdr-cli -v -s %s -o %s -t mantiuk08 %s" %(hdr_name, tm_name, os.path.join(folder,"LDR_"+date_time+"_*.jpg")))
        # pfsinme *.jpg | pfssize --maxx 1200 | pfsalign -v -c min | pfshdrcalibrate -r linear -v --bpp 16 | pfsout --radiance result.hdr
        # Falsecolour commands
        for maxlum in (1,10,100,1000,10000):
            fc_hdr_name = os.path.join(folder,"FC_"+date_time+"_"+str(maxlum).zfill(5)+".hdr")
            fc_ldr_name = os.path.join(folder,"FC_"+date_time+"_"+str(maxlum).zfill(5)+".tif")
            cmds.append("falsecolor -i %s -l cd/m2 -n 10 -s %s > %s" % (hdr_name,maxlum,fc_hdr_name))
            cmds.append("ra_tiff -z %s %s" % (fc_hdr_name, fc_ldr_name))
            if platform.system() == 'Windows':
                cmds.append("delete %s" % fc_hdr_name)
            else:
                cmds.append("rm -f %s" % fc_hdr_name)
        # Print and execute commands
        for cmd in cmds:
            print(cmd)
            os.system(cmd)
    else:
        print("The minimum available storage space needed is %s MB." % free_space) 
        print("The system does not have enough storage space (%s MB). Stopping now." % min_free_space)

if __name__ == "__main__":
    main()
