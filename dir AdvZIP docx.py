from tkinter import filedialog
from glob import glob
from subprocess import run
from winsound import Beep

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to process')
if (sourcedir == ''):
    quit()

# Process file list
for filename in glob(sourcedir + "/**/*.docx", recursive=True):   # select all files in all subfolders
    run(f'advzip -z -4 -i 20 "{filename}"') # output in quotes for paths with spaces
Beep(300, 1200)