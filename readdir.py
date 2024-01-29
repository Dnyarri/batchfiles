from tkinter import filedialog
import glob

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to process')
if (sourcedir == ''):
    quit()
# Print dir
print('Куда идти?')
print (sourcedir)
# Print file list
for filename in glob.glob(sourcedir + "/**/*.*", recursive=True):   # select all files in all subfolders
    print(f'"Идите в" "{filename}"') # output in quotes for paths with spaces
