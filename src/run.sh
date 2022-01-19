#!/usr/bin/bash
echo "inside run.sh"
echo "$NODE_TYPE"
if [ "$NODE_TYPE" == "MASTER" ]
then
    echo "starting master from run.sh"
    python3.9 ./src/master.py
    # python3.9 ./src/master.py > ~/shared/output.txt
elif [ "$NODE_TYPE" == "WORKER" ]
then
    python3.9 ./src/worker.py 
else
    exit
fi
