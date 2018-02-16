#!/bin/bash

#script for installing Docker
echo "Updating apt and adding HTTPS..."
{
apt-get update									#Update apt
apt-get install -y \								#Enable apt for HTTPS
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
} &>/dev/null

echo "Adding Docker official GPG key..."
{
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -		#Adding official GPG key
} &>/dev/null
apt-key fingerprint 0EBFCD88							#Verifying fingerprint

echo "Adding Docker repository..."
{
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
} &>/dev/null

echo "Updating apt and installing docker..."
{
apt-get update									#update
apt-get install -y docker-ce							#install docker
} &>/dev/null
echo "Testing if install successfull"
docker run hello-world								#test if installed

