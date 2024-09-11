#!/usr/bin/env python3

'''
Opens a folder, and recursively feeds all .docx files in it to leanify.exe for recompression and reducing file size.
leanify.exe is available from https://github.com/JayXon/Leanify

WARNING:
---------
Source files are replaced! No backup, no renaming!

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "2024.09.10"
__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Production"

import subprocess

from os import name
from glob import glob

from tkinter import Tk
from tkinter import Label
from tkinter import filedialog

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('Recompressing .docx...')
sortir.geometry('+100+100')
sortir.maxsize(800, 600)
zanyato = Label(sortir, wraplength=700, text='Starting...', font=("arial", 12), padx=16, pady=10, justify='center')
zanyato.pack()
sortir.withdraw()

# Main dialog created and hidden
# --------------------------------------------------------------

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to compress DOCX files')
if sourcedir == '':
    sortir.destroy()
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
# Creating subprocess startupinfo for hidden console. Requires
# from os import name
#

startupinfo = None
if name == 'nt':
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

#
# now .popen or .run may be used as below:
# subprocess.run(f'program.exe -switches "{filename}"', startupinfo=startupinfo)
# --------------------------------------------------------------

# Process file list
for filename in glob(f'{sourcedir}/**/*.docx', recursive=True):  # select all files in all subfolders

    zanyato.config(text=f' Processing {filename}... ')  # Updating label, showing processed file name
    sortir.update()
    sortir.update_idletasks()

    # output in quotes for paths with spaces
    subprocess.run(f'leanify.exe -q -i 50 "{filename}"', startupinfo=startupinfo)


# --------------------------------------------------------------
# Destroying dialog

sortir.destroy()
sortir.mainloop()

# Dialog destroyed and closed
# --------------------------------------------------------------
