# from the downloaded 'raw' project, construct multi-fault dataset
import os
import sys
import re
import glob
import subprocess
import shlex
import shutil

from util import source_file_names, get_test_number, linking_command_pattern


def modify_makefile(seeded_path, project_name):
    with open(os.path.join(seeded_path, 'Makefile')) as f:
        lines = f.readlines()

    for i, l in enumerate(lines):
        if linking_command_pattern[project_name] in l and '-lgcov' not in l:
            lines[i] = l = l.rstrip() + ' -lgcov' + '\n'

        # remove solaris-system-dependent library options
        lines[i] = l = l.replace('-lkstat', '')
        lines[i] = l = l.replace('-lkvm', '')
        lines[i] = l = l.replace('-lelf', '')

    with open(os.path.join(seeded_path, 'Makefile'), 'w') as f:
        f.writelines(lines)


def clean_script(test_script_path):
    with open(test_script_path, 'r') as f:
        lines = f.readlines()

    # /usr/bin/csh -> /bin/bash
    for i, l in enumerate(lines):
        if '/usr/bin/csh' in l:
            lines[i] = l.replace('/usr/bin/csh', '/bin/bash')

    with open(test_script_path, 'w') as f:
        f.writelines(lines)


def clean_faultseed(fault_seed_path):
    with open(fault_seed_path) as f:
        lines = f.readlines()

    for i, l in enumerate(lines):
        if '/*' in l:
            lines[i] = l.replace('/*', '//').replace('*/', '')

    with open(fault_seed_path, 'w') as f:
        f.writelines(lines)


def add_faultseed_to_source(seeded_path, project_name):
    source_file_path = glob.glob(os.path.join(
        seeded_path, source_file_names[project_name]))
    assert len(source_file_path) == 1
    source_file_path = source_file_path[0]
    with open(source_file_path) as f:
        lines = f.readlines()

    has_faultseed = False
    for i, l in enumerate(lines):
        if 'FaultSeeds.h' in l:
            has_faultseed = True

    if not has_faultseed:
        lines.insert(0, '#include "FaultSeeds.h"\n')

    with open(source_file_path, 'w') as f:
        f.writelines(lines)


def add_longlong_definition(seeded_path, project_name):
    """
    The following protects users who use other than Sun compilers
    (eg, GNU C) that don't support long long, and need to include
    this header file
    """
    longlong_definition = "typedef long long longlong_t;\n"

    header_file_path = os.path.join(seeded_path, f'{project_name}.h')
    with open(header_file_path, 'r') as f:
        lines = f.readlines()

    if longlong_definition in ''.join(lines):
        return

    for i, line in enumerate(lines):
        if '#include <sys/types.h>' in line:
            lines.insert(i+1, longlong_definition)
            break

    with open(header_file_path, 'w') as f:
        f.writelines(lines)


def check_is_in_subdir(commands):
    for l in commands[::]:
        if 'cd' in l and '#' not in l and '..' not in l:
            return True
        if 'cd' in l and '..' in l:
            return False
    return False


def split_test_cases(test_script_path, project_name):
    clean_script(test_script_path)

    dirpath, script_name = os.path.split(test_script_path)
    script_name = script_name.split('.')[0]

    with open(test_script_path) as f:
        lines = f.readlines()

    tc_run_commands = dict()
    index = 0
    while index < len(lines):
        commands = []
        test_out_name = None
        test_num = None
        if '>>>running' in lines[index]:
            commands.append(lines[index])
            index += 1
            while index < len(lines) and not '>>>running' in lines[index]:
                l = lines[index]
                if '.exe' in l:
                    test_out_name = re.search(
                        r'../outputs/((?:test|t)[0-9]+[^\s]*)', l).group(1)
                    if '.out' in test_out_name:
                        l = l.replace('.out', '')
                        test_out_name = test_out_name.replace('.out', '')

                    test_num = get_test_number(test_out_name)

                l = l.replace(
                    '../inputs', '../../inputs').replace('../outputs', '../../outputs').replace('../testplans.alt', '../../testplans.alt')

                if 'outputs/backup' in l:
                    backupfile_name = re.search(
                        r'outputs/(backup.[0-9]+)', l).group(1)
                    l = l.replace(backupfile_name, f'backup.{test_num}')

                if 'outputs/out0.' in l:
                    covfile_name = re.search(
                        r'outputs/(out0.[0-9]+)', l).group(1)
                    l = l.replace(covfile_name, f'out0.{test_num}')

                if 'outputs/err0.' in l:
                    covfile_name = re.search(
                        r'outputs/(err0.[0-9]+)', l).group(1)
                    l = l.replace(covfile_name, f'err0.{test_num}')

                commands.append(l)
                index += 1
            assert test_out_name != None

            tc_run_commands[test_out_name] = commands
        else:
            index += 1

    test_case_dir = os.path.join(dirpath, script_name)
    if os.path.exists(test_case_dir):
        shutil.rmtree(test_case_dir)
    os.mkdir(test_case_dir)

    print(f'split test cases from {test_script_path}: {len(tc_run_commands)}')

    for tc_name in tc_run_commands:
        with open(os.path.join(test_case_dir, tc_name + '.sh'), 'w') as f:
            f.write('#!/bin/bash\n')
            f.write('\n')
            f.writelines(tc_run_commands[tc_name])
