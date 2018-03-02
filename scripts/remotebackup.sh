#!/bin/bash

openstack server start backup 
sleep 2m 
ssh -i /home/ubuntu/.ssh/id_rsa ubuntu@10.10.0.200 '/home/ubuntu/scripts/backupscript.sh' 
sleep 10 
openstack server stop backup 
