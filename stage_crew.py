#!/usr/bin/env python3

# Bare-bones start to the "git clean and clone" utility.
# (Why the eff did I call it stage_crew?)

# Next three (big'uns)
# 1. add configparser and options
#   - location of template files directory
#   - base directory for new story directories
# 2. add argparse
#   - pass story title as argument
#	- avoid '--' - it's a Git tool, so act like one
#

import argparse
import os
import re
import sys

if sys.version_info.major < 3:
    #raise RuntimeError("Must be using Python 3 or later")
    print("error: must use Python 3")
    sys.exit(0)

# process command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("title", help="make a directory from a V1 story title")
# if verbose, report what was done, like
# "created directory 123456-my-shiny-new-story-dir"; else no output
parser.add_argument("-v", "--verbose", action="store_true")
args = parser.parse_args()
#print(args.title)
#sys.exit(0)

original_title = args.title
new_title = args.title

# strip off leading 'B-': useful for copying and pasting from V1
leader = '^[Bb]-'
if re.search(leader, new_title):
    new_title = new_title[2:]

# convert one or more whitespace to a dash
new_title = new_title.strip()
new_title = "-".join(new_title.split())

# without the \D, allows more than 6 digits at the front
story_id = '^\d{5,6}\D'
if re.search(story_id, new_title):
    try:
        if args.verbose:
            #print('creating directory {} from title string "{}"'.format(new_title, original_title))
            print('creating directory {}'.format(new_title))
        os.mkdir(new_title)
    except OSError:
        print("error: directory already exists")
else:
    print("need a story ID and title")
 
