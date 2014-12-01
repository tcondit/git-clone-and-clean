#!/usr/bin/env python3

# Bare-bones start to the "git clean and clone" utility.
# (Why the eff did I call it stage_crew?)

# TODO refactor everything (much) later

# Next three
#

# Next three (big'uns)
# [done] 1. add configparser and options
#   - location of template files directory
#   - base directory for new story directories
# [done] 2. add argparse
#   - pass story title as argument
#	- avoid '--' - it's a Git tool, so act like one
# 3. 'git init' the new directory

import argparse
import configparser
import os
import os.path
import re
import subprocess
import sys

##
## front matter
##
if sys.version_info.major < 3:
    #raise RuntimeError("Must be using Python 3 or later")
    print("error: must use Python 3")
    sys.exit(0)


##
## argparse
##
parser = argparse.ArgumentParser(description="::TODO:: some helpful text here")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("title", help="make a Git repo from a V1 story title")
args = parser.parse_args()


##
## configparser
##
config = configparser.ConfigParser()
config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stage_crew.ini')

config.read(config_file)
if args.verbose:
    print('config_file={}'.format(config_file))

TEMPLATE_DIR = config['DEFAULT']['template_dir']
if args.verbose:
    print('  TEMPLATE_DIR={}'.format(config['DEFAULT']['template_dir']))

GIT_REPO_BASE_DIR = config['DEFAULT']['git_repo_base_dir']
if args.verbose:
    print('  GIT_REPO_BASE_DIR={}'.format(config['DEFAULT']['git_repo_base_dir']))

# check that TEMPLATE_DIR is a Git repo; write to the directory later, and
# catch exceptions as they happen; TODO refactor
if not os.path.isdir(TEMPLATE_DIR):
    raise IOError("TEMPLATE_DIR not found: {}. Check your INI file.".format(TEMPLATE_DIR))
elif not os.path.isdir(os.path.normpath(os.path.join(TEMPLATE_DIR, '.git'))):
    raise IOError("TEMPLATE_DIR not a Git repo: {}".format(os.path.normpath(os.path.join(TEMPLATE_DIR, '.git'))))

# check that GIT_REPO_BASE_DIR exists, but is NOT a Git repo; write to the
# directory later, and catch exceptions as they happen; TODO refactor
if not os.path.isdir(GIT_REPO_BASE_DIR):
    raise IOError("GIT_REPO_BASE_DIR not found: {}. Check your INI file.".format(GIT_REPO_BASE_DIR))
elif os.path.isdir(os.path.normpath(os.path.join(GIT_REPO_BASE_DIR, '.git'))):
    raise IOError("GIT_REPO_BASE_DIR is already a Git repo: {}".format(os.path.normpath(os.path.join(GIT_REPO_BASE_DIR, '.git'))))


# TODO check that TEMPLATE_DIR is a Git repository; found a nice answer for
# this (git ls-remote --get-url [REMOTE]), but it depends on TEMPLATE_DIR
# having a remote; therefore, I'll add it to a simple search for a .git/
# directory; TODO maybe later

# TODO check that GIT_REPO_BASE_DIR is NOT a Git repository; found a nice
# answer for this (git ls-remote --get-url [REMOTE]), but it depends on
# GIT_REPO_BASE_DIR NOT having a remote; therefore, I'll add it to a simple
# search for a .git/ directory; TODO maybe later


##
## title munging
##
original_title = args.title
new_title = args.title

# strip off leading 'B-': useful for copying and pasting from V1
leader = '^[Bb]-\d{5,6}\D'
if re.search(leader, new_title):
    new_title = new_title[2:]

# convert colons and one or more whitespace to a dash; TODO consider checking
# for other unhelpful characters like parens, commas, etc., later
new_title = new_title.strip()
new_title = new_title.replace(":", " ")
new_title = "-".join(new_title.split())
new_title = new_title.lower()

# without the \D, allows more than 6 digits at the front
story_id = '^\d{5,6}\D'
if not re.search(story_id, new_title):
    print("need a 5- or 6-digit story ID and title")

# check that new_repo_path does not exist; write to the directory later, and
# catch exceptions as they happen; TODO refactor
new_repo_path = os.path.normpath(os.path.join(GIT_REPO_BASE_DIR, new_title))
if os.path.isdir(new_repo_path):
    print('error: directory already exists: {}'.format(new_repo_path))
    # TODO re-raise error here so we exit immediately?
    #raise
    sys.exit(1)
else:


##
## create the repo
##

# http://stackoverflow.com/questions/16363460/set-up-a-default-directory-structure-on-git-init
#
# Note really sure what the eff this guy did
# http://kevinthompson.info/blog/2013/11/11/using-git-repos-as-project-templates.html

oldcwd = os.path.dirname(os.path.abspath(__file__))
#os.chdir(os.path.normpath(os.path.join(oldcwd, new_title)))
os.chdir(new_repo_path)
newcwd = os.path.dirname(os.path.abspath(__file__))
#print('newcwd:{}'.format(newcwd))

# TODO I want to clone an existing repo here, not create a new one
mkrepo = subprocess.check_output(["git", "init"], universal_newlines=True)
print(mkrepo)
if args.verbose:
    print('created Git repo {}'.format(new_title))

os.chdir(oldcwd)
 
