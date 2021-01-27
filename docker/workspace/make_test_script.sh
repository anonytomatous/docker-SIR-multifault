#!/bin/bash

# usage: sh make_test_script.sh 

BASEDIR=$(dirname $(readlink -f "$0"))
# set environment PATH
export CLASSPATH=/root/workspace/mts.jar:/root/workspace/antlr-2.7.6.jar

if [[ "$@" == *"gzip"* ]]; then
    project=gzip
    for versionpath in /root/$project/versions.alt/versions.seeded/v*; do
        version=$(basename $versionpath)
        echo $version

        # make test script using mts tool
        cd /root/$project/testplans.alt

        # gzip: use tsl test suite
        java sir.mts.MakeTestScript -sf $version.tsl.universe -sn test_$version.sh -en /root/$project/versions.alt/versions.seeded/$version/$project.exe
    done
fi

if [[ "$@" == *"grep"* ]]; then
    project=grep
    for versionpath in /root/$project/versions.alt/versions.seeded/v*; do
        version=$(basename $versionpath)
        echo $version

        # make test script using mts tool
        cd /root/$project/testplans.alt

        # grep: use cov test suite (with escape)
        java sir.mts.MakeTestScript -sf $version/v0.cov.universe.esc -sn test_$version.sh -en /root/$project/versions.alt/versions.seeded/$version/$project.exe

        # grep: use extended test suite (cov + tsl)
        # java sir.mts.MakeTestScript -sf /root/$project.universe -sn test_$version.sh -en /root/$project/versions.alt/versions.seeded/$version/$project.exe
    done
fi

if [[ "$@" == *"flex"* ]]; then
    project=flex
    for versionpath in /root/$project/versions.alt/versions.seeded/v*; do
        version=$(basename $versionpath)
        echo $version

        # make test script using mts tool
        cd /root/$project/testplans.alt

        # flex: use cov test suite
        java sir.mts.MakeTestScript -sf $version/v0.cov.universe -sn test_$version.sh -en /root/$project/versions.alt/versions.seeded/$version/$project.exe
    done
fi

if [[ "$@" == *"sed"* ]]; then
    project=sed
    # do not use versions with no universe.single testsuite
    # rm -rf /root/$project/versions.alt/versions.seeded/v4
    rm -rf /root/$project/versions.alt/versions.seeded/v5
    rm -rf /root/$project/versions.alt/versions.seeded/v6
    rm -rf /root/$project/versions.alt/versions.seeded/v7
    for versionpath in /root/$project/versions.alt/versions.seeded/v*; do
        version=$(basename $versionpath)
        echo $version

        # make test script using mts tool
        cd /root/$project/testplans.alt

        # sed: use single test suite
        java sir.mts.MakeTestScript -sf v0/v0_2.universe.single -sn test_$version.sh -en /root/$project/versions.alt/versions.seeded/$version/$project.exe
    done
fi
