#!/usr/bin/python

import os
import shutil
import argparse
import subprocess

VERBOSE = 0
DEBUG = 0

SSH_USER = "ubuntu@"

##########################################################
#Parse arguments
parser = argparse.ArgumentParser(prog='run_on_all.py')
parser.add_argument('-v','--verbose',dest="verbose",help="Turn verbosity on",default=False,action="store_true")
parser.add_argument('-d','--debug',dest="debug",help="Turn debuging on",default=False,action="store_true")
parser.add_argument('-c','--command', help="What command to run",nargs='+')

arguments = parser.parse_args()

VERBOSE = arguments.verbose
DEBUG = arguments.debug
COMMAND = ' '.join(arguments.command) #Ignore spacing in argument

def verbose(text):
    if VERBOSE:
        print text

def debug(text):
    if DEBUG:
        print text

verbose("Verbose is enabled")
debug("Debug is enabled")

#Get all IPs, except Manager (itself)
serverlist = subprocess.check_output(["openstack server list --status active | grep imt | grep -v ManagerMasterv2 | awk '{print $8}' | sed -e 's/.*=//;s/,//'"],shell=True)
serverlist = serverlist.rstrip()
serverlist = serverlist.split('\n')


verbose("arg is: " + str(COMMAND))

#Loops all instances and sends the desired command, ignoring output and disconnecting each session preemptivly (ssh -f)
for ip in serverlist:
    ip = SSH_USER + ip
    subprocess.check_output(["ssh -f " + ip + " " + COMMAND + " > /dev/null 2>&1 "],shell=True)
    verbose("host: " + ip)
