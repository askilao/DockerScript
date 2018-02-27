#!/bin/bash

if curl -s --head 10.212.136.60 | grep "200 OK" > /dev/null
  then 
    echo "Bookface oppe!" | > /dev/null
  else
    echo "Bookface er nede!" | $(/usr/sbin/ssmtp blinkV2bot@gmail.com)
fi

if curl -s  10.212.136.60 | grep "No connection" > /dev/null
	then
	echo "Ingen kobling til databasen" | $(/usr/sbin/ssmtp blinkV2bot@gmail.com)
fi
