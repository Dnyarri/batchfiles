from tkinter import filedialog
import glob
import subprocess

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to process')
if sourcedir == '':
    quit()

# Process file list
for filename in glob.glob(sourcedir + "/**/*.ogg", recursive=True):  # select all OGG files in all subfolders
    subprocess.run(
        f'"C:/Program Files/Windows Media Player/wmplayer.exe" "{filename}"', shell=True
    )  # output in quotes for paths with spaces
    # C:\Program Files\Windows Media Player\wmplayer.exe with changed slashes
