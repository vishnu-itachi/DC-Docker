#!/usr/bin/bash
echo "inside run.sh"
echo "$NODE_TYPE"
if [ "$NODE_TYPE" == "MASTER" ]
then
    python3.9 ./src/master.py
elif [ "$NODE_TYPE" == "WORKER" ]
then
    python3.9 ./src/worker.py > ~/shared/output.txt
else
    exit
fi
