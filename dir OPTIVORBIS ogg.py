<<<<<<< HEAD
<<<<<<< HEAD:readdir optimize OGG with optivorbis.py
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
=======
=======
>>>>>>> 90ee2294f96f3dd1f07dff25b191e4a652df6286
# Opens a folder, and recursively feeds all OGG files in it to optivorbis.exe for recompression and reducing file size.
# optivorbis.exe is available from https://git.codeproxy.net/OptiVorbis/OptiVorbis/releases
#
#   WARNING:
#   Source files are replaced! No backup, no renaming!

from tkinter import filedialog
from glob import glob
from subprocess import run
import os

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to compress OGG files')
if (sourcedir == ''):
    quit()

# Process file list
for filename in glob(sourcedir + "/**/*.ogg", recursive=True):   # select all OGG files in all subfolders
    os.rename(f"{filename}", "D:/hujwam.ogg")
    run(f'"optivorbis.exe" "D:/hujwam.ogg" "{filename}"') # output in quotes for paths with spaces
<<<<<<< HEAD
<<<<<<< HEAD
    os.remove("D:/hujwam.ogg")
Beep(300, 1200)
>>>>>>> 4805b6d (update):readdir OPTIVORBIS ogg.py
=======
    os.remove("D:/hujwam.ogg")
>>>>>>> ef33c03 (update)
=======
    os.remove("D:/hujwam.ogg")
>>>>>>> 90ee2294f96f3dd1f07dff25b191e4a652df6286
