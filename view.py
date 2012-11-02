#!/usr/bin/python

import os, sys, logging, traceback, time, subprocess, shlex
import config as cfg

log = logging

__version__ = '$Id:$'


def init():
    print 'passing'

def start():
    print 'starting'

def stop():
    print 'stopping'    

def download():
    
    arg1=shlex.split("pkill feh")
    arg2=shlex.split("feh -ZXrFnqSfilename '%s'" % cfg.dest_folder)
    
    print "killing existing feh processes"
    subprocess.Popen(arg1)
    time.sleep(0.5)

    feh=subprocess.Popen(arg2)
    print "starting feh with pid: %s" % feh.pid

def error():
    print 'unrecognized error. meh'

actions={
    "init":init(),
    "start":start(),
    "stop":stop(),
    "download":download()}

def main():
    try:
        print os.environ['ACTION']
        print actions['%s' % os.environ['ACTION']]

        actions['%s' % os.environ['ACTION']]
    except KeyError:
        error()
        

if __name__ == '__main__':
    try:
        main()
    except (SystemExit,KeyboardInterrupt):
        exit('\nQuitting\n')    
    except:
        traceback.print_exc(file=sys.stdout)
        
    # prevent window from closing on PCs
    exit()    
