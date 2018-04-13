#!/usr/bin/python

import subprocess
import argparse
import math

VERBOSE = 0
DEBUG = 0

IP = "10.212.136.60"
USER = "prouser"
PASSWORD = "greatpw"

RATE_PER_SERVER = 3
MAX_SERVERS = 1

parser = argparse.ArgumentParser(prog="dynascale.py")
parser.add_argument('-v','--verbose',dest="verbose",help="Turn verbosity on",default=False,action="store_true")
parser.add_argument('-d','--debug',dest="debug",help="Turn debuging on",default=False,action="store_true")
parser.add_argument('-i','--ip',dest='ip', help='Ip address of haproxy server', default=IP)
parser.add_argument('-u','--user',dest='user', help='Username for haproxy authentication', default=USER)
parser.add_argument('-p','--password',dest='password', help='Password for haproxy authentication', default=PASSWORD)

arguments = parser.parse_args()

VERBOSE = arguments.verbose
DEBUG = arguments.debug
IP = arguments.ip
USER = arguments.user
PASSWORD = arguments.password

def verbose(text):
    if VERBOSE:
        print text

def debug(text):
    if DEBUG:
        print text

# 1 Get trafficdata(vurrent rate)
def get_rate(user,password,ip):
    # curl -s http://username:password@ipaddress:1936;/csv
    output = subprocess.check_output(["curl","-s","http://"+ user + ":" + password + "@" + "ip" + ":1936/\;csv"])
    for line in output.split('\n'):
        if "bookface" in line:
            stats_array = line.split(',')
            total_sessions = stats_array[4]
            return float(total_sessions)
def get_rate_alt(user,password,ip):
    return float(3)

# 2 get number of workers in swarm
def get_workers():
    # docker service ls | grep bookface_web | awk '{print $4}' | sed -e 's/.*\///g'
    output = subprocess.check_output([docker service ls | grep bookface_web | awk '{print $4}' | sed -e 's/.*\///g'], shell=true)
    output.rstrip()
    return float(output)

def get_workers_alt():
    return float(2)
    

def scale_up(current,goal):
    for i in range((current + 1), (goal + 1)):
        verbose("Starting server " + str(i))

def scale_down(current,goal):
    for i in range (current, goal, -1):
        verbose("Shutting down server " + str(i))


current_rate = get_rate(USER,PASSWORD,IP)
verbose("Current rate: " + str(current_rate))

current_workers = get_workers()
verbose("Current workers: " + str(current_workers))


# 3 calculate the current needed capacity
needed_capacity = math.ceil(current_rate / RATE_PER_SERVER)
verbose("We need " + str(needed_capacity) + " to handle this rate")

if needed_capacity < MIN_SERVERS:
    verbose("Adjusting needed capacity to minimun: " + str(MIN_SERVERS))
    needed_capacity = MIN_SERVERS
elif needed_capacity > MAX_SERVERS:
    verbose("Adjusting needed capacity to maximum " + str(MAX_SERVERS))

# 4 compare current needed with a actual capacity and take action: reduce or increase or none of the above
if needed_capacity > current_workers:
    verbose("We need to increase the number of servers from " + str(current_workers) + " to " + str(needed_capacity))
    scale_up(int(current_rate),int(needed_capacity))
elif needed_capacity < current_workers:
    verbose("We need to decrease the number of servers from " + str(current_workers) + " to " + str(needed_capacit    y))
    scale_down(int(current_workers),int(needed_capacity))
else:
    verbose("No further tampering needed all is good my man")





























