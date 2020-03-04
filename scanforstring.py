#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import os
import re
import json
import traceback
from datetime import datetime

try:
    from argparse import ArgumentParser as ArgParser
except ImportError:
    from optparse import OptionParser as ArgParser

__version__ = "1.0.0"

codefolders="."
fileextensions=".c,.java,.py"
regex=".*[Cc]opyright.*"
nomatch=False
numlines=0

def version():
    print("{}: {}".format(os.path.basename(__file__), __version__))
    raise SystemExit()

def scanargs():
    global codefolders, fileextensions, regex, numlines, nomatch
    description = (
            'Scan for String Action\n'
            '-----------------------------------------------'
            '-----------\n'
            )
    parser = ArgParser(description=description)
    try:
        parser.add_argument = parser.add_option
    except AttributeError:
        pass

    parser.add_argument('-v', '--version', action='store_true', help='Show version numbers and exit')
    parser.add_argument('-f', '--codefolders', help='Source code folders to scan separated by ":", e.g. /user/code1:/user/code2', default=codefolders)
    parser.add_argument('-e', '--fileextensions', help='File Extensions for these folders separated by ",", e.g. .c,.java,.py', default=fileextensions)
    parser.add_argument('-r', '--regex', help='Regex that defines the string, e.g. ".*[Cc]opyright.*"', default=regex)
    parser.add_argument('-n', '--nomatch', action='store_true', help='Default is to find files that match, this finds files that don\'t match')
    parser.add_argument('-l', '--lines', help='Read the first N lines of the file to find the string (0 = entire file)', default=numlines)
    options = parser.parse_args()
    if isinstance(options, tuple):
        args = options[0]
    else:
        args = options
    del options

    if args.version:
        version()
    
    if args.codefolders:
        codefolders = args.codefolders.split(":")

    if args.fileextensions:
        fileextensions = args.fileextensions.split(",")

    if args.regex:
        regex = args.regex

    if args.lines:
        numlines = int(args.lines)

    if args.nomatch:
        nomatch = args.nomatch

    should_exit = False

    # Do any input validation here...
    if should_exit == True:
        raise SystemExit()


def main():
    try:
        scanargs()
        yescount = 0
        nocount = 0
        totalcount = 0
        errorfiles = list()
        matchfiles = list()
        nomatchfiles = list()
        regextest = re.compile(regex)
        print(f"Scanning {len(codefolders)} folders for source file extensions {fileextensions}")
        if numlines == 0:
            print(f"looking for \"{regex}\" in the file")
        else:
            print(f"looking for \"{regex}\" in the first {numlines} lines of code")
        for folder in codefolders:
            reporoot = os.path.abspath(folder)
            print(f"Scanning folder {reporoot}")
            for root, dirs, files in os.walk(folder):
                for filename in files:
                    if filename.endswith(tuple(fileextensions)):
                        filepath = os.path.join(root,filename)
                        reporelpath = filepath.replace(reporoot, "")
                        count = 0
                        found = False
                        sawfile = False
                        totalcount = totalcount + 1
                        with open(filepath) as f:
                            try:
                                for line in f:
                                    count = count + 1
                                    if regextest.match(line):
                                        yescount = yescount + 1
                                        found = True
                                        sawfile = True
                                        break
                                    if numlines != 0:
                                        if count > numlines:
                                            nocount = nocount + 1
                                            sawfile = True
                                            break
                            except Exception as e:
                                # print(f"{e}")
                                # traceback.print_exc()
                                errorfiles.append(reporelpath)
                        if sawfile == False:
                            nocount = nocount + 1
                        if found == False:
                            nomatchfiles.append(reporelpath)
                        else:
                            matchfiles.append(reporelpath)
        if nomatch == True:
            print(f"No match {nomatchfiles} - {len(nomatchfiles)}")
        else:
            print(f"Match {matchfiles} - {len(matchfiles)}")
        print(f"Files that failed: {errorfiles}")
        print(f"Total Files: {totalcount} Match: {yescount} NoMatch: {nocount} (includes {len(errorfiles)} errors)") 

    except KeyboardInterrupt:
        print("\nCancelling...\n")
    except Exception as ex:
        print("\nCaught Exception: {}".format(ex))
        traceback.print_exc()


if __name__ == '__main__':
    main()



