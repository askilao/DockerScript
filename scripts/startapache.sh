#!/bin/bash

while read line
 do
    ssh ubuntu@"$line" "wwwhosts; sudo service apache2 start;" < /dev/null 
done < "$1"
