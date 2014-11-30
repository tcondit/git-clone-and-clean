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
# 3. 'git init' the new directory

import argparse
import configparser
import os
import re
import sys

# front matter
if sys.version_info.major < 3:
    #raise RuntimeError("Must be using Python 3 or later")
    print("error: must use Python 3")
    sys.exit(0)

# check configs
config = configparser.ConfigParser()
config.read('stage_crew.ini')
TEMPLATE_DIR = print(config['DEFAULT']['template_dir'])
GIT_REPO_BASE_DIR = print(config['DEFAULT']['git_repo_base_dir'])


# TODO check that TEMPLATE_DIR and GIT_REPO_BASE_DIR are directories

# TODO check that TEMPLATE_DIR and GIT_REPO_BASE_DIR exist

# TODO check that TEMPLATE_DIR is a Git repository

# TODO check that GIT_REPO_BASE_DIR is NOT a Git repository


# process command-line arguments
parser = argparse.ArgumentParser(description="::TODO:: some helpful text here")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("title", help="make a Git repo from a V1 story title")
args = parser.parse_args()

original_title = args.title
new_title = args.title

# strip off leading 'B-': useful for copying and pasting from V1
leader = '^[Bb]-\d{5,6}\D'
if re.search(leader, new_title):
    new_title = new_title[2:]

# convert colons and one or more whitespace to a dash
new_title = new_title.strip()
new_title = new_title.replace(":", " ")
new_title = "-".join(new_title.split())

# without the \D, allows more than 6 digits at the front
story_id = '^\d{5,6}\D'
if re.search(story_id, new_title):
    try:
        if args.verbose:
            #print('creating directory {} from title string "{}"'.format(new_title, original_title))
            print('creating git repo {}'.format(new_title))
        os.mkdir(new_title)
    except OSError:
        print("error: directory already exists")
else:
    print("need a 5- or 6-digit story ID and title")
 
