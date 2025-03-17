#!/bin/bash

url="http://192.168.1.100:8000/file.zip"

seq 1 100 | xargs -P 10 -I {} wget $url -O file_{}.zip