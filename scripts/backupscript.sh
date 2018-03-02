#!/bin/bash

sudo mysqldump --opt --master-data=2 --flush-logs --all-database | ssh ubuntu@10.10.1.70 "cat > ~/backups/backup_$(date +"%d_%m_%y_%R").sql"

