#!/usr/bin/python

import os, sys, logging, traceback, time, subprocess, shlex
import config as cfg

log = logging

__version__ = '$Id:$'

#### would've been good to use this, however couldnt get execve() to recognize arguments in limited testing
#view_arg="python %s -o'%s'" % (view,dest_folder)

#### define the commands for gphoto2 and feh
arg1=shlex.split("gphoto2 --folder='%s' --capture-tethered --filename='%s' --hook-script='%s'" % (cfg.camera_folder,os.path.join(cfg.dest_folder,cfg.filename_str),cfg.view))
arg2=shlex.split("pkill gphoto2")
arg3=shlex.split("gphoto2 --folder='%s' --get-all-files --filename='%s' --recurse" % (cfg.camera_folder,os.path.join(cfg.dest_folder,cfg.filename_str)))
arg4=shlex.split("gphoto2 --folder='%s' --delete-all-files --recurse" % cfg.camera_folder)
arg5=shlex.split("pkill feh")
arg6=shlex.split("feh -ZXrFnqSfilename '%s'" % cfg.dest_folder)

def wait_timeout(proc, seconds):
    """Wait for process to finish, or raise exception after timeout"""
    start = time.time()
    end = start + seconds
    interval = min(seconds / 1000.0, .25)

    while True:
        result = proc.poll()
        if result is not None:
            return result
        if time.time() >= end:
            proc.kill()
            raise RuntimeError("Process timed out")
        time.sleep(interval)        

def loop_fn():
    """capture event. after a while, close and attempt to download ungrabbed photos, which happens a lot"""
    try:
        capture=subprocess.Popen(arg1)
        wait_timeout(capture,30)
    except RuntimeError:
        pass

    """Download event. Grab tether sync fails from the camera and display."""
    try:
        download=subprocess.Popen(arg3)
        wait_timeout(download,15)
        print "killing existing feh processes"
        subprocess.Popen(arg1)
        time.sleep(0.5)

        feh=subprocess.Popen(arg2)
        print "starting feh with pid: %s" % feh.pid

    except RuntimeError:
        pass
    
    """Delete event. Delete all photos from camera"""
    try:
        delete=subprocess.Popen(arg4)
        wait_timeout(delete,5)
    except RuntimeError:
        pass

    print "looping back"
    loop_fn()    

def main():
    
    loop_fn()
        
if __name__ == '__main__':
    try:
        main()
    except (SystemExit,KeyboardInterrupt):
        exit('\nQuitting\n')    
    except:
        traceback.print_exc(file=sys.stdout)
        
    # prevent window from closing on PCs
    exit()    
