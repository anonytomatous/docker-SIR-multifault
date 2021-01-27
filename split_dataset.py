import json
import os
import sys
import argparse

from collections import defaultdict

def split_dataset_by_faultnum(dataset):
    dataset_by_faultnum = defaultdict(lambda: defaultdict(str))

    for version_id in dataset:
        datapoint = dataset[version_id]
        faultid = version_id.split('-')[-1]
        faults = faultid.split('_')

        dataset_by_faultnum[len(faults)-1][version_id] = datapoint

    return dataset_by_faultnum



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--cov_dir', '-c', default='coverage_files/gzip/v1/f2_f4', required=True)
    parser.add_argument('file', default='./gzip.json')
    args = parser.parse_args()

    with open(args.file) as f:
        dataset = json.load(f)

    datasets = split_dataset_by_faultnum(dataset)

    for i in range(len(datasets)):
        with open(args.file[:-5] + f'-faults-{i+1}.json', 'w') as f:
            json.dump(datasets[i], f, indent=4)
