#!/bin/bash
export PATH=/home/pavlos/.local/bin/:$PATH
red='\e[1;31m%s\e[0m\n'
green='\e[1;32m%s\e[0m\n'
yellow='\e[1;33m%s\e[0m\n'
blue='\e[1;34m%s\e[0m\n'
magenta='\e[1;35m%s\e[0m\n'
cyan='\e[1;36m%s\e[0m\n'

[ -d "dist/" ] && rm -rf dist/* || printf "$green" "dist directory does not exist!"
[ -f "MANIFEST" ] && rm -f MANIFEST || printf "$green" "MANIFEST does not exist"
python3 setup.py sdist
twine upload dist/*

