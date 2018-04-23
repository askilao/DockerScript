#!/usr/bin/python

#Generates a .conf file listing relevant machines that needs to have a backup.

import os
import argparse
import subprocess

VERBOSE = 0
DEBUG = 0

BACKUP_CONFIG="backup_policy.conf"
EXCLUDED='nobackup' # tag on server that should be excluded from backup

parser = argparse.ArgumentParser(prog='backup_hosts.py')
parser.add_argument('-v','--verbose',dest="verbose",help='Turn verbosity on',default=False,action="store_true")
parser.add_argument('-d','--debug',dest="debug",help='Turn debug_messages on',default=False,action="store_true")
parser.add_argument('-e','--excluded',dest="excluded",help='Tag for filtering out what not to back up',metavar="STRING",default=EXCLUDED)
arguments = parser.parse_args()

VERBOSE = arguments.verbose
DEBUG = arguments.debug
EXCLUDED = arguments.excluded

def verbose(text):
    if VERBOSE:
        print text

def debug(text):
    if DEBUG:
        print text

# 1 get list of active servers and find the one elegible for backup (nobackup tag)
verbose("Getting active IPs...")
serverlist = subprocess.check_output(["openstack server list --status active | grep -v " + EXCLUDED + " | grep imt3003 |awk '{print $8}' | sed -e 's/.*=//;s/,//'"],shell=True)
serverlist = serverlist.rstrip()
serverlist = serverlist.split('\n')

try:
    os.remove("backup_policy.conf")
except OSError:
    pass

backupfile = open(BACKUP_CONFIG, "a+")

for ip in serverlist:
    verbose(str(ip))
    backupfile.write(str(ip) + ":/etc,/home/ubuntu\n")

backupfile.close()
