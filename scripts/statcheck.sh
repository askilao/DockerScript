#!/bin/bash
curl -s -u prouser:greatpw  10.212.136.60:1936/\;csv > httpstat.csv

CONN_RATE=$(csvtool col 34 httpstat.csv | sed '9q;d')
echo "$(date +%s),$CONN_RATE" >> haproxystat.dat


