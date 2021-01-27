# Multi-faults dataset for C programs

The target program code and seeded faults are originally downloaded from [SIR Repository](https://sir.csc.ncsu.edu/). Currently, this multi-faults dataset contains following subject programs, the early versions of linux utilities:

```
- gzip v1.5
- grep v1.2
- flex v1.1
- sed v2.0
```

## Prerequisite

* Docker

* Python version > 3.6

## Get started

In host,
```shell
docker build --tag sir-dataset:latest ./docker/
docker run -dt --name sir -v $(pwd)/docker/workspace:/root/workspace -v $(pwd)/coverage_files:/root/coverage_files -v $(pwd)/failing_tests:/root/failing_tests -v $(pwd)/faulty_lines:/root/faulty_lines sir-dataset:latest
docker exec -it sir bash
```

running this command will instantiate a docker container. The container is set as an environment for running and collect execution profiles of subject programs from SIR repository.


## Measure the coverage of test cases on programs with combined faults 

### 1. Run setup command for target projects

In the path `/root/workspace` of the Docker container, run `setup.sh` to generate test suite for each project, and modify original programs to collect coverage on each execution. You can just run the setup script with no argument,

```shell
bash setup.sh
```

or specify target projects as arguments.

```shell
bash setup.sh gzip grep flex sed
# bash setup.sh grep flex sed (exclude gzip)
# bash setup.sh sed (only sed)
```

### 2. Execute test suite on programs with possible combinations of faults

If you want to use all target projects for generating multi-faults versions, the following command combines 1-4 seeded faults for each original version, and generate failing test results and collect coverage by executing the combined versions.

```shell
bash execute.sh
```

or you can separately generate multi-faults versions for the desired number of faults and the specific project name

```shell
python3.6 execute.py --fault_num[-n] N --project[-p] [project_name] --coverage

# example: python3.6 execute.py -n 2 -p gzip --coverage
```

uses all possible pairs of faults that have at lease one failing test (fault-revealing test).


## Build dataset Json file for Failure Clustering Experiment

In host (the repository root), running below command

```shell
sh build_dataset.sh
```
creates json files for all target projects that contains both clusterable multi-fault versions and single-fault versions with multiple failing tests.

If you want to individually construct dataset, directly use the `build_dataset.py` and `split_dataset.py` scripts.

```shell
python build_dataset.py --project[-p] [project_name] --outfile [result_file_name]
python split_dataset.py [result_file_name]  # this splits the faulty versions contained in the dataset by number of faults

# example: python build_dataset.py -p gzip --outfile dataset/gzip.json
# example: python split_dataset.py dataset/gzip.json
```

This will generate the list of faulty versions with multiple failing tests, either from single fault or multiple faults in `json` format. (Below is an example)

```json
    ...,
    "gzip-v1-f4_f13_f16": {
        "coverage": "[repo_root]/coverage_files/dataframes/gzip/v1/f4_f13_f16.pkl",
        "setup_command": "echo 'no setup command yet'",
        "cleanup_command": "",
        "failing_tests": {
            "gzip-v1-f4": "[repo_root]/failing_tests_valid/gzip/v1_f4_f13_f16_f4",
            "gzip-v1-f13": "[repo_root]/failing_tests_valid/gzip/v1_f4_f13_f16_f13",
            "gzip-v1-f16": "[repo_root]/failing_tests_valid/gzip/v1_f4_f13_f16_f16"
        },
        "faulty_components": {
            "gzip-v1-f4": "[repo_root]/faulty_lines/gzip/v1/f4",
            "gzip-v1-f13": "[repo_root]/faulty_lines/gzip/v1/f13",
            "gzip-v1-f16": "[repo_root]/faulty_lines/gzip/v1/f16"
        },
        "faulty_components_level": 1
    },
    ...

```

This `json` file can be used in [Hybiscus](https://github.com/anonytomatous/Hybiscus) Failure Clustering experiment.