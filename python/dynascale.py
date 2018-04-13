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
MAX_SERVERS = 10
MIN_SERVERS = 1

parser = argparse.ArgumentParser(prog="scale.py") #prog= definerer usage

parser.add_argument('-v','--verbose',dest="verbose",help="Turn verbosity on",default=False,action="store_true")
parser.add_argument('-d','--debug',dest="debug",help="Turn debig info on",default=False,action="store_true")

parser.add_argument('-i','--ip',dest="ip",help="IP adr of Haproxy server",default=IP)
parser.add_argument('-u','--user',dest="user",help="Username for HAproxy auth",default=USER)
parser.add_argument('-p','--password',dest="password",help="Password for HAproxy auth",default=PASSWORD)

arguments = parser.parse_args()

VERBOSE = arguments.verbose
DEBUG = arguments.debug
IP = arguments.ip
USER = arguments.user
PASSWORD = arguments.password

def verbose(text):
    if VERBOSE:
        print text

def debut(text):
    if DEBUG:
        print text

#### Helper functions
def get_rate(user,password,ip):
    #output saves content of csv file from HAproxy: curl -s http://user:pw@ip:port/;csv
    output = subprocess.check_output(["curl","-s","http://" + user + ":" + password + "@" + ip + ":1936/\;csv"]) 
    for line in output.split('\n'):
        if "bookface" in line: #look for string
            stats_array = line.split(',')
            total_sessions = stats_array[4] #finds current rate in col 5
            return float(total_sessions)

#alt rate for testing purposes
def get_rate_alt(user,password,ip):
    return 3.0

#find numbers of workers
def get_workers():
    output = subprocess.check_output(["docker service ls | grep bookface_web | awk '{print $4}' | sed -e 's/.*\///g'"],shell=True,executable='/bin/bash')
    output.rstrip()
    return float(output)

def get_workers_alt():
    return float(2)

def scale_up(current,goal):
    #scales number of replicas accordingly
    subprocess.call(["docker service scale bf_bookface_web=" + str(goal)],shell=True)
    for i in range((current + 1),(goal + 1)):
        verbose("Starting server " + str(i))
<<<<<<< HEAD
    os.system("docker service update --replicas=" + str(goal) + "bf_bookface_web")
=======
>>>>>>> afec2c8b6df0fb5e47d5cf647c5408b5c188b6c6

def scale_down(current,goal):
    subprocess.call(["docker service scale bf_bookface_web=" + str(goal)],shell=True)
    for i in range(current,goal,-1): #teller nedover
        verbose("Shutting down server " + str(i))
<<<<<<< HEAD
    os.system("docker service update --replicas=" + str(goal) + "bf_bookface_web")
=======
>>>>>>> afec2c8b6df0fb5e47d5cf647c5408b5c188b6c6



#1 get current rate
current_rate = get_rate(USER,PASSWORD,IP)
verbose("Current rate: " + str(current_rate))

#2 get number of workers
current_workers = get_workers()
verbose("Current workers: " + str(current_workers))

#3 calculate the current needed capacity
#del rate paa ant server og rund opp
needed_capacity = math.ceil(current_rate / RATE_PER_SERVER)
verbose("We need " + str(needed_capacity) + " to handle this rate")

if needed_capacity < MIN_SERVERS:
    verbose("Adjusting needed capacity to minimum: " + str(MIN_SERVERS))
    needed_capacity = MIN_SERVERS
elif needed_capacity > MAX_SERVERS:
    verbose("Adjusting needed capacity to maximum: " + str(MAX_SERVERS))
    needed_capacity = MAX_SERVERS

#4 compare current needed with actual capacity and tace action: reduce/increase/do nothing
if needed_capacity > current_workers:
    verbose("We need to increase the number of servers from " + str(current_workers) + " to " + str(needed_capacity))
    scale_up(int(current_workers),int(needed_capacity))
elif needed_capacity < current_workers:
    verbose("We need to decrease the number of servers from " + str(current_workers) + " to " + str(needed_capacity))
    scale_down(int(current_workers),int(needed_capacity))
else:
    verbose("Current workers is adequate, no action needed")
