# Opens a folder, and recursively feeds all OGG files in it to optivorbis.exe for recompression and reducing file size. optivorbis.exe is available from https://git.codeproxy.net/OptiVorbis/OptiVorbis/releases
# WARNING: Source files are replaced, no backup, no renaming

from tkinter import filedialog
import glob
import subprocess
import os

# Open source dir
sourcedir = filedialog.askdirectory(title='Open folder with OGG files to process')
if (sourcedir == ''):
    quit()

# Process file list
for filename in glob.glob(sourcedir + "/**/*.ogg", recursive=True):   # select all OGG files in all subfolders
    os.rename(f"{filename}", "D:/hujwam.ogg")
    subprocess.run(f'"optivorbis.exe" "D:/hujwam.ogg" "{filename}"') # output in quotes for paths with spaces
    os.remove("D:/hujwam.ogg")