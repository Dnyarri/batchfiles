#   Replaces filename fragments and formatting I don't like.
#   Currently removes digits and double dots, and replaces underscores with spaces.

from tkinter import filedialog
from glob import glob
from os import rename

'''
# Open source dir
sourcedir = filedialog.askdirectory(title='Open folder with files to process')
if (sourcedir == ''):
    quit()
'''
sourcedir = 'D:/Ilyich/Literature/Честертон'
tempfilename = ''

# Process file list
for filename in glob(sourcedir + "/**/*.*", recursive=True):    # select all files in all subfolders

    tempfilename = filename.replace('_', ' ')                   # set of unwanted criteria begins
    for i in "0123456789":
        tempfilename = tempfilename.replace(i,'')
    tempfilename = tempfilename.replace('..', '.')

    rename(f"{filename}", f"{tempfilename}")                    # rename it, finally