#!/usr/bin/env python
# Raspberry Pi camera HDR automatic capture
# 2015-01-11 Francesco Anselmo
# francesco.anselmo@gmail.com
# francesco.anselmo@arup.com

min_free_space = 100 # minimum free space in MB
#cmd_fmt = "raspistill -mm matrix -cfx 34:51 -awb off -v -t 1 -vf -hf -w 1024 -h 768" # raspistill command format
cmd_fmt = "raspistill -mm average -awb sun -v -t 1 -vf -hf -w 1024 -h 768" # raspistill command format
folder = "/opt/camera"
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
        # Print and execute commands
        for cmd in cmds:
            print(cmd)
            os.system(cmd)
    else:
        print("The minimum available storage space needed is %s MB." % free_space) 
        print("The system does not have enough storage space (%s MB). Stopping now." % min_free_space)

if __name__ == "__main__":
    main()
