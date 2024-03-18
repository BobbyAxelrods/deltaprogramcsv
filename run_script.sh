#!/bin/bash

#Function to run script 

run_script(){
    python main.py
}

# Run script 

run_script

#Check exit status 

exit_status=$?

#retry logi
retry_interval=14400
# 14400 for 4 hours 

while [ $exit_status -ne 0 ]; do
    echo "Script failed. Retrying 4 hours .."
    sleep $retry_interval
    run_script
    exit_status=$?
done