#!/usr/bin/python

import os
import shutil
import argparse

VERBOSE = 0
DEBUG = 0

ITERATIONS = 7
BACKUP_FOLDER = "backups/"
CONFIG = "backup_policy.conf"

SCP_USER = "ubuntu@"

##########################################################
#Parse arguments
parser = argparse.ArgumentParser(prog='backup.py')
parser.add_argument('-v','--verbose',dest="verbose",help="Turn verbosity on",default=False,action="store_true")
parser.add_argument('-d','--debug',dest="debug",help="Turn debuging on",default=False,action="store_true")
parser.add_argument('-c','--config',dest="config",help="config file destination",metavar="FILE",default=CONFIG)
parser.add_argument('-i','--iterations',dest="iterations",type=int,help="Number of iterations of backup folders",metavar='N',default=ITERATIONS)
parser.add_argument('-b','--backup_directory',dest="backup_dir",help="backupfile destinations",metavar="FOLDER",default=BACKUP_FOLDER)

arguments = parser.parse_args()

VERBOSE = arguments.verbose
DEBUG = arguments.debug
ITERATIONS = arguments.iterations
CONFIG = str(arguments.config)
BACKUP_FOLDER = arguments.backup_dir
##########################################################


def verbose(text):
    if VERBOSE:
        print text

def debug(text):
    if DEBUG:
        print text

verbose("verbose is enabled")
debug("debug is enabled")

verbose("Opening config file: " + CONFIG)
with open(CONFIG) as config:
    for line in config:
        debug("Read line: " + line)
        configlist = line.split(":")
        pathlist = configlist[1].split(",")
        host = configlist[0]
        verbose("Host is: " + host)

        
        # 0. check for bacup folder
        host_backup_path = BACKUP_FOLDER + host
        if not os.path.isdir(host_backup_path):
            verbose("creating host backup directory: " + host_backup_path)
            os.makedirs(host_backup_path)



        # 1. remove oldest version of backup
        if os.path.isdir(host_backup_path + "." + str(ITERATIONS)):
            verbose("Deleting oldest version of backup directory")
            shutil.rmtree(host_backup_path + "." + str(ITERATIONS))

        # 2. move folders up one step
        for i in range((ITERATIONS - 1),0,-1):
            if os.path.isdir(host_backup_path + "." + str(i)):
                verbose("Moving " + host_backup_path + " from " + str(i) + " to " +str(i+1))
                shutil.move(host_backup_path + "." + str(i),host_backup_path + "." + str(i + 1))
                
                
        # 3. cp -al current newest folder 
        verbose("Copying main folder with hard links")
        os.system("cp -al " + host_backup_path + " " + host_backup_path + ".1")

        # 4. sync current folder from remote server
        verbose("Synchronizing folders...")
        for folder in pathlist:
            folder = folder.rstrip()
            verbose("-> " + folder)
            if not os.path.isdir(host_backup_path + folder):
                os.makedirs(host_backup_path + folder)
            
            verbose_rsync = ""
            if VERBOSE:
                verbose_rsync = "v"

            command ="rsync -a" + verbose_rsync + " --delete " + SCP_USER + host + ":" + folder + " " + host_backup_path + folder
            debug("Executing: " + command )
            os.system(command)
























