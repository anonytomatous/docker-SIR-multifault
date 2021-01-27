#!/bin/bash

targets="gzip grep flex sed"
for project in $targets
do
    python3.6 execute.py -n 2 -p $project --coverage
    python3.6 execute.py -n 3 -p $project --coverage
    python3.6 execute.py -n 4 -p $project --coverage
done