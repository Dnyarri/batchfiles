# Opens a folder, and recursively feeds all .docx files in it to advzip.exe for recompression and reducing file size.
# advzip.exe is available from https://github.com/amadvance/advancecomp
#
#   WARNING:
#   Source files are replaced! No backup, no renaming!

from tkinter import filedialog
from glob import glob
from subprocess import run

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to compress DOCX files')
if (sourcedir == ''):
    quit()

# Process file list
for filename in glob(sourcedir + "/**/*.docx", recursive=True):   # select all files in all subfolders
    run(f'advzip.exe -z -4 -i 20 "{filename}"') # output in quotes for paths with spaces