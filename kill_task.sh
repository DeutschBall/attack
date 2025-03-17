#!/bin/bash
if [ "$#" -lt 1 ]; then
    echo "error: insufficient arguments"
    echo "usage: "
    echo "./kill_task.sh <pid>"
    exit 1
fi

kill -9 $1