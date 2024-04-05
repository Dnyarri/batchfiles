#!/usr/bin/env python

'''
Opens a folder, and recursively feeds all OGG files in it to optivorbis.exe for recompression and reducing file size.
optivorbis.exe is available from https://git.codeproxy.net/OptiVorbis/OptiVorbis/releases

WARNING:
Source files are replaced! No backup, no renaming!

WARNING:
Drive D: is used for temp file. Edit this if you don't have one.

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "2024.02.27"
__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Production"

import os

from glob import glob
import subprocess

from tkinter import Tk
from tkinter import Label
from tkinter import filedialog

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('Recompressing .OGG...')
sortir.geometry('+100+100')
zanyato = Label(sortir, text='Starting...', font=("arial", 12), padx=16, pady=10, justify='center')
zanyato.pack()
sortir.withdraw()

# Main dialog created and hidden
# --------------------------------------------------------------

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to compress OGG files')
if (sourcedir == ''):
    quit()

# --------------------------------------------------------------
# Updating dialog

sortir.deiconify()
zanyato.config(text='Allons-y!')
sortir.update()
sortir.update_idletasks()

# Dialog shown and updated
# --------------------------------------------------------------

# --------------------------------------------------------------
# Creating subprocess startupinfo for hidden console.
#

startupinfo = None
if os.name == 'nt':
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

#
# now .popen or .run may be used as below:
# subprocess.run(f'program.exe -switches "{filename}"', startupinfo=startupinfo)
# --------------------------------------------------------------

# Process file list
for filename in glob(sourcedir + "/**/*.ogg", recursive=True):   # select all OGG files in all subfolders

    zanyato.config(text='Processing ' + filename + '...')      # Updating label, showing processed file name
    sortir.update()
    sortir.update_idletasks()

    os.rename(f"{filename}", "D:/hujwam.ogg")
    # output in quotes for paths with spaces
    subprocess.run(f'"optivorbis.exe" "-q" "D:/hujwam.ogg" "{filename}"', startupinfo=startupinfo)
    os.remove("D:/hujwam.ogg")

# --------------------------------------------------------------
# Destroying dialog

sortir.destroy()
sortir.mainloop()

# Dialog destroyed and closed
# --------------------------------------------------------------
