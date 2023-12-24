from tkinter import filedialog
import glob

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to process')
if (sourcedir == ''):
    quit()

# Print file list
for filename in glob.glob(sourcedir + "/**/*.*", recursive=True):   # select all files in all subfolders
    print(f'"Идите в" "{filename}"') # output in quotes for paths with spaces
