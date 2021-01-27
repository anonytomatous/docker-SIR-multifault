# TODO
# parse fault map from info/ directory
# create /root/failing_tests/[version_name].expected - expected failing tests list

import os
import glob
import re
import argparse
from collections import defaultdict
from util import sort_string_by_number, string2number

# For single fault

def load_actual_test_failures(failing_tests_path, project, version):
    # version name format: v*_f*_f*... (ex. v1_f2_f13: faults 2, 13 enabled on v1)
    faulty_versions = [os.path.join(failing_tests_path, project, v) for v in os.listdir(os.path.join(failing_tests_path, project)) if re.match(f'{version}_' + r'f[0-9]+$', v)]
    print(faulty_versions)
    fault_map_actual = dict()

    for version_path in faulty_versions:
        if '.expected' in version_path:
            continue
        version_name = version_path.split('/')[-1]
        fault_map_actual[version_name] = sort_string_by_number([l.strip() for l in open(version_path).readlines()])

    return fault_map_actual

def convert_make_testnum(test_num):
    if test_num > 13 and test_num < 45:
        new_test_num = test_num + 1
    else:
        new_test_num = test_num + 797
    
    return str(new_test_num)

def load_expected_test_failures(project, version, test_suite_name, target_faulty_versions):
    fault_map_path = os.path.join('/root', project, 'info', version, f'fault-matrix.{test_suite_name}')
    fault_map_raw_lines = open(fault_map_path).readlines()
    fault_map = dict()

    for version_name in target_faulty_versions:
        fault_map[version_name] = []
    
    index = 0
    while index < len(fault_map_raw_lines):
        l = fault_map_raw_lines[index]
        if 'unitest' in l:
            test_name = re.search(r'uni(test[0-9]+):', l).group(1)
            if project == 'make':
                # a dirty way 
                test_name = test_prefix[project] + convert_make_testnum(string2number(test_name))
                # test_name = test_prefix[project] + str(string2number(test_name))
            else:
                test_name = test_prefix[project] + str(string2number(test_name)+1)
        
            for _ in range(len(target_faulty_versions)):
                vname = fault_map_raw_lines[index+1].split(':')[0]
                version_name = f'{version}_{vname.replace("v", "f")}'
                try: 
                    result = int(fault_map_raw_lines[index+2].strip())
                except ValueError as e:
                    print(e)
                    print(target_faulty_versions)
                    print(index)
                    exit(0)

                if result == 1:
                    fault_map[version_name].append(test_name)
                index += 2
            
        index += 1
            
    return fault_map

fault_map_info = {
    'gzip': 'v0.tsl.universe',
    'grep': 'v0.cov.universe',
    'make': 'v0.cov.universe',
    'flex': 'v0.cov.universe',
    'sed': '',  # no ground-truth fault map for sed
}

test_prefix = {
    'gzip': 'test',
    'grep': 't',
    'make': 't',
    'flex': 't',
    'sed': 't',
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', '-p', default='gzip')
    parser.add_argument('--versions', '-v', nargs='*')
    args = parser.parse_args()
    
    project = args.project
    
    for version in args.versions:
        fault_map_actual = load_actual_test_failures('/root/failing_tests', project, version)

        fault_map_expected = load_expected_test_failures(project, version, fault_map_info[project], fault_map_actual.keys())
        print(fault_map_expected)
        for version_name in fault_map_expected:
            with open(f'/root/failing_tests/{project}/{version_name}.expected', 'w') as f:
                f.writelines([testname + '\n' for testname in fault_map_expected[version_name]])

