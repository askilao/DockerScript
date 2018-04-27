#!/bin/bash

Wget https://releases.hashicorp.com/consul/1.0.7/consul_1.0.7_linux_amd64.zip 
if hash unzip 2>/dev/null; then
		unzip consul_1.0.7_linux_amd64.zip 
else
		apt install -y unzip
fi

unzip consul_1.0.7_linux_amd64.zip

mv consul /usr/local/bin/
mkdir /opt/consul 
