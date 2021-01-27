# TODO: transfer notebook code for creating (observed) faultmap
# goal: get dataframe with failing tests of both single fault and merged faults

# fault map: [faulty version => failing tests] mappings

import os
import glob
import re
import pandas as pd


def get_single_fault_map(project_name, load_expected=False):
    singlefault_versions = [version for version in os.listdir(
        f'./failing_tests/{project_name}') if re.match(r'^v[0-9]+_f[0-9]+$', version) != None]

    rows = []

    for version_id in singlefault_versions:
        with open(f'./failing_tests/{project_name}/{version_id}') as f:
            failing_tests = [l.strip() for l in f.readlines()]

        row = {
            'version_id': version_id,
            'original_version': version_id.split('_')[0],
            'activated_faults': version_id.split('_')[1:],
            'failing_tests': failing_tests,
        }

        if load_expected:
            with open(f'./failing_tests/{project_name}/{version_id}.expected') as f:
                failing_test_expected = [l.strip() for l in f.readlines()]
            row['failing_tests_expected'] = failing_test_expected

        rows.append(row)

    single_fault_map = pd.DataFrame(rows)

    single_fault_map['nonempty'] = \
        single_fault_map.apply(lambda row: len(row.failing_tests) > 0, axis=1)

    if load_expected:
        single_fault_map['identical'] = \
            single_fault_map.apply(lambda row: all(
                i in row.failing_tests_expected for i in row.failing_tests) and all(
                i in row.failing_tests for i in row.failing_tests_expected), axis=1)

        single_fault_map['partial_failure_observed'] = \
            single_fault_map.apply(lambda row: all(
                i in row.failing_tests_expected for i in row.failing_tests), axis=1)

    return single_fault_map


def get_fault_map(project_name):
    # single fault + multi fault versions

    multifault_versions = [version for version in os.listdir(
        f'./failing_tests/{project_name}') if re.match(r'^v[0-9]+_f[0-9]+_', version) != None]

    rows = []
    for version_id in multifault_versions:
        with open(f'./failing_tests/{project_name}/{version_id}') as f:
            failing_tests = [l.strip() for l in f.readlines()]

        rows.append({
            'version_id': version_id,
            'original_version': version_id.split('_')[0],
            'activated_faults': version_id.split('_')[1:],
            'failing_tests': failing_tests,
        })

    single_fault_map = get_single_fault_map(project_name)
    multi_fault_map = pd.DataFrame(rows)
    # multi_fault_map =  attach_validation_result(multi_fault_map, single_fault_map.set_index('version_id'))    

    faultmap = pd.concat([single_fault_map, multi_fault_map], axis=0)
    faultmap['faults_num'] = faultmap['activated_faults'].apply(lambda faults: len(faults))
    faultmap['faultid'] = faultmap['activated_faults'].apply(lambda faults: '_'.join(faults))

    return faultmap

def merge_list(lists):
    merged = []
    for l in lists:
        merged.extend(l)

    return merged

def attach_validation_result(multi_fault_map, single_fault_map):
    rows = []
    for i, row in multi_fault_map.iterrows():
        individual_failing_tests = []
        for fault_name in row.activated_faults:
            component = single_fault_map.loc[f'{row.original_version}_{fault_name}']
            assert len(component.failing_tests) > 0
            individual_failing_tests.append(
                set(component.failing_tests))

        # check overlapping
        # overlapped = len(list(set.union(*individual_failing_tests))) != len(merge_list(individual_failing_tests))
        overlapped_tests = []

        for i in range(len(individual_failing_tests)):
            for j in range(i+1, len(individual_failing_tests)):
                overlapped_tests.extend(list(set.intersection(individual_failing_tests[i], individual_failing_tests[j])))
        
        overlapped_tests = set(overlapped_tests)
        
        subsumed = False

        for tests in individual_failing_tests:
            if len(tests - overlapped_tests) == 0:
                subsumed = True
                break

        # check union
        union = set.union(*individual_failing_tests) == set(row.failing_tests)

        row['overlapped'] = subsumed
        row['union'] = union
        # row['valid'] = union & (not subsumed)
        row['valid'] = union
        rows.append(row)

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = get_fault_map('gzip')
    df.to_csv('all_versions_gzip.csv')