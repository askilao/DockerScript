#!/bin/bash
#PATH=/home/ubuntu/bin:/home/ubuntu/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
status_Check() {
VAR=$(openstack server list --name $1 | awk 'NR>3{print$6}')
if [ "$VAR" = "SHUTOFF" ]; 
	then
		#echo ""$2" $line - restarting..." | $(/usr/sbin/ssmtp blinkV2bot@gmail.com) 
		echo "$(date) Server $line was shut off, restarting..." >> /home/ubuntu/status_log.txt
		openstack server start $line
fi
if [ "$VAR" = "PAUSED" ]; 
	then
		echo "$(date) Server $line was paused, unpausing..." >> /home/ubuntu/status_log.txt
		openstack server unpause $line
fi
if [ "$VAR" = "LOCKED" ]; 
	then
		echo "$(date) Server $line was locked, unlocking..." >> /home/ubuntu/status_log.txt
		openstack server unlock $line
fi
#if [ "$VAR" = "ACTIVE" ]; 
#	then
#		#echo "EVERYTHING IS A-OK BRO"  #>> /home/ubuntu/status_log.txt
#fi

}

#source ~/IMT3003_V18_group17-openrc.sh
declare -a arr=("Kyrre fucka til" "Stuxnet rammet" "Need more dedicated RAM on" "Dan Børge brekker seg inni" "All servers must die" "ADRIAN HVA HAR DU GJORT" "Frode skrev config til")
string=${arr[$RANDOM % ${#arr[*]}]};
while read line
	do
		status_Check $line "$string"
	done < "$1"

