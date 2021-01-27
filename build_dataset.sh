#!/bin/bash

mkdir -p dataset/

targets="gzip grep flex sed"
for project in $targets 
do
    python build_dataset.py -p $project --outfile dataset/$project.json
    python split_dataset.py dataset/$project.json
    rm dataset/$project.json
done