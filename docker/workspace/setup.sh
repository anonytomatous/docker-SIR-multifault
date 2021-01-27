#!/bin/bash

echo $#

if [[ $# -eq 0 ]]; then
    targets="gzip grep flex sed"
else
    targets="$@"
fi

export experiment_root=/root

bash make_test_script.sh $targets

pip install -r /root/workspace/requirements.txt

if [[ $targets == *"gzip"* ]]; then
    # Replace errorneous test scripts with manually fixed ones
    cp -f /root/workspace/test_fix/gzip/cpotr.sh /root/gzip/testplans.alt/testscripts/
    cp -f /root/workspace/test_fix/gzip/cpotr1.sh /root/gzip/testplans.alt/testscripts/
    cp -f /root/workspace/test_fix/gzip/cpotr2.sh /root/gzip/testplans.alt/testscripts/
    
    python3.6 execute.py --preprocess -p gzip
    python3.6 execute.py -n 1 -p gzip --coverage
fi

if [[ $targets == *"grep"* ]]; then
    python3.6 execute.py --preprocess -p grep
    python3.6 execute.py -n 1 -p grep --coverage
fi

if [[ $targets == *"flex"* ]]; then
    python3.6 execute.py --preprocess -p flex
    python3.6 execute.py -n 1 -p flex --coverage
fi

if [[ $targets == *"sed"* ]]; then
    python3.6 execute.py --preprocess -p sed
    python3.6 execute.py -n 1 -p sed --coverage
fi
