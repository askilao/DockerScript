#!/usr/bin/python

import os
import shutil
import argparse
import subprocess
import time


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
# Function that checks if a host is up and starts it if not
def status_check(host):
    verbose("Checking if " + host + " is active")
    output = subprocess.check_output(["openstack server list | grep " + host + " | awk '{print$6}'"],shell=True)
    if "SHUTOFF" in output.split('\n'):
        verbose(host + " is shutoff")
        name = subprocess.check_output(["openstack server list | grep " + host + " | awk '{print$4}'"],shell=True)
        verbose("Starting up " + name)
        subprocess.call(["openstack server start " + name],shell=True)
        # Busy Waiting until server is reachable
        while True:
            response = os.system("ping -c 1 " + host)
            if response !=0:
                verbose("Waiting for system to wake up...")
                time.sleep(0.5)
            else:
                verbose("System is up!")
                time.sleep(10)
                break


verbose("Opening config file: " + CONFIG)
with open(CONFIG) as config:
    for line in config:
        debug("Read line: " + line)
        configlist = line.split(":")
        pathlist = configlist[1].split(",")
        verbose("Host is: " + configlist[0])
        host = configlist[0]

        
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
            debug("Checking if " + str(i) + "th folder exists")
            if os.path.isdir(host_backup_path + "." + str(i)):
                verbose("Moving " + host_backup_path + " from " + str(i) + " to " +str(i + 1))
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
            
            verbose_rsync = "v" if VERBOSE else ""
            command ="rsync -a" + verbose_rsync + " --delete " + SCP_USER + host + ":" + folder + " " + host_backup_path + folder
            debug("Executing: " + command)
            os.system(command)
