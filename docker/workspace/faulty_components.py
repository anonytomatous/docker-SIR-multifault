# for each (single-fault) version, save the row id of faulty component to the file
# /root/faulty_lines/{project}/{original_version}/{fault_id} (in docker)
# ex) /root/faulty_lines/gzip/v1/f1

import os
import glob
import argparse
import shutil
import pandas as pd
import re

import logging

from collections import defaultdict
from util import source_file_names


def extract_faulty_lines(v, faulty_lines_dict):
    project = v.project_name
    version = v.version
    faulty_lines_dict[version] = dict()

    logging.basicConfig(
        filename=f'logs/faulty_lines_{project}.log', filemode='w', level=logging.INFO)

    # from the seeded source path, extract each fault's location (use FaultSeeds.h)
    logging.info(version)
    logging.info(v.faults)

    for i in range(len(v.faults)):
        faultid = f'f{i+1}'
        fault_name = v.faults[i]

        source_file_path = glob.glob(os.path.join(
            v.seeded_path, source_file_names[v.project_name]))
        assert len(source_file_path) == 1
        source_file_path = source_file_path[0]

        with open(source_file_path) as f:
            lines = f.readlines()

        faulty_lines = []
        index = 0
        while index < len(lines):
            l = lines[index]

            if re.search(r'\#\s*ifndef', l) != None and fault_name in l:
                index += 1
                while re.search(r'\#\s*else', lines[index]) == None and re.search(r'\#\s*endif', lines[index]) == None:
                    index += 1

                if re.search(r'\#\s*else', lines[index]) != None:
                    has_else_branch = True
                else:
                    has_else_branch = False

                if has_else_branch:
                    index += 1
                    while re.search(r'\#\s*endif', lines[index]) == None:
                        logging.info(lines[index])
                        faulty_lines.append(index+1)
                        index += 1

            elif re.search(r'\#\s*ifdef', l) != None and fault_name in l:
                index += 1
                while re.search(r'\#\s*else', lines[index]) == None and re.search(r'\#\s*endif', lines[index]) == None:
                    logging.info(lines[index])
                    faulty_lines.append(index+1)
                    index += 1

                if re.search(r'\#\s*else', lines[index]) != None:
                    has_else_branch = True
                else:
                    has_else_branch = False

                if has_else_branch:
                    index += 1
                    while re.search(r'\#\s*endif', lines[index]) == None:
                        index += 1

            index += 1

        logging.info(faulty_lines)
        faulty_lines_dict[version][faultid] = faulty_lines
