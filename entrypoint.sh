#!/bin/sh -l

CODEFOLDERS=$1
FILEEXTENSIONS=$2
REGEX=$3
MATCH=$4
LINES=$5

python3 /scanforstring.py -f "$CODEFOLDERS" -e "$FILEEXTENSIONS" -r "$REGEX" -m $MATCH -l $LINES
