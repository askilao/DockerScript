#!/bin/bash

function check {
     if [ $? -ne 0 ] ; then
         echo "Error occurred getting URL $1:"
         if [ $? -eq 6 ]; then
             echo "Unable to resolve host"
         fi
         if [$? -eq 7 ]; then
             echo "Unable to connect to host"
         fi
         exit 1
     fi

}

declare -a arr=("10.212.136.60" "10.10.0.248:32731" "10.10.0.248:32782")

for i in "${arr[@]}"
do
	curl -s -o "/dev/null" $i
	check;
done
