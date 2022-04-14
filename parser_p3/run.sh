#!/bin/bash

#Usage
function print_usage(){
    printf "\tUsage: $0 <source_file>\n"
}

if [ "$#" -ne 1 ]; then
    printf "[ERROR] Invalid Number of Arguments\n"
    print_usage

elif [ ! -f "$1" ]; then
    printf "[ERROR] No such file ("$1") in the current directory\n"
    print_usage
    exit
else
    python3 parser.py "$1"
fi
