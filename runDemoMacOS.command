#!/usr/bin/env bash

echo "dirname : [$(dirname "$0")]"

cd "$(dirname "$0")"

python3 demo.py

# Pearbaby note: I just use this script to run the Python more
#                easily since my install got absolutely cooked
#                when I tried to install a wrapper module for 
#                the NASA CEARUN FORTRAN code. Every time I 
#                tried to right click to run any .py file the 
#                Python launcher would hang forever. Meh...
