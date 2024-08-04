#!/usr/bin/env python3

'''
Replaces filename fragments and formatting I don't like.
Currently removes digits and double dots, and replaces underscores with spaces.

'''

from tkinter import filedialog
from glob import glob
from os import rename

# Open source dir
sourcedir = filedialog.askdirectory(title='Open folder with files to process')
if sourcedir == '':
    quit()

tempfilename = ''

# Process file list
for filename in glob(sourcedir + "/**/*.*", recursive=True):  # select all files in all subfolders

    # now goes the set of renaming criteria etc.

    tempfilename = filename.replace('_', ' ')  # replace underscore with space

    for i in "0123456789":
        tempfilename = tempfilename.replace(i, '')  # replace any digit with nothing

    tempfilename = tempfilename.replace('..', '.')  # replace double dot with single

    rename(f"{filename}", f"{tempfilename}")  # rename it, applying set of renaming criteria etc.
