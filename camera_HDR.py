#!/usr/bin/env python
# Raspberry Pi camera HDR capture and process
# 2015-01-11 Francesco Anselmo
# francesco.anselmo@gmail.com
# francesco.anselmo@arup.com

min_free_space = 100 # minimum free space in MB
ISOs = [100]
speeds = [1000000/8000,1000000/4000,1000000/2000,1000000/1000,1000000/500,
          1000000/250 ,1000000/125, 1000000/60,  1000000/30,  1000000/15,
          1000000/8,   1000000/4,   1000000/2,   1000000,     2000000,
          4000000]
cmd_fmt = "raspistill -v -t 1 -vf -hf -w 1024 -h 768" # raspistill command format
opt_man = "-awb none -ifx none -drc off" # raspistill manual options format
folder = "/opt/camera"

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
    if free_space > min_free_space:
        date_time = time.strftime("%Y-%m-%d_%H%M")
        print(date_time)
        auto_photo_name = os.path.join(folder,"AUTO_"+date_time+".jpg")
        # Automatic photo command
	cmds = [cmd_fmt + " -o " + auto_photo_name ]
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
        cmds.append("luminance-hdr-cli -v -s %s -o %s %s" %(hdr_name, tm_name, os.path.join(folder,"LDR_"+date_time+"_*.jpg")))
        # Print and execute commands
        for cmd in cmds:
            print(cmd)
            os.system(cmd)
    else:
        print("The minimum available storage space needed is %s MB." % free_space) 
        print("The system does not have enough storage space (%s MB). Stopping now." % min_free_space)

if __name__ == "__main__":
    main()
