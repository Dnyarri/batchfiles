#!/usr/bin/env python3

'''
Opens a folder, and recursively feeds all .docx files in it to advzip.exe for recompression and reducing file size.
advzip.exe is available from https://github.com/amadvance/advancecomp

WARNING:
---------
Source files are replaced! No backup, no renaming!

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "2024.02.27"
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
zanyato = Label(sortir, text='Starting...', font=("arial", 12), padx=16, pady=10, justify='center')
zanyato.pack()
sortir.withdraw()

# Main dialog created and hidden
# --------------------------------------------------------------

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to compress DOCX files')
if (sourcedir == ''):
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
for filename in glob(sourcedir + "/**/*.docx", recursive=True):   # select all files in all subfolders

    zanyato.config(text=f'Processing {filename}...')      # Updating label, showing processed file name
    sortir.update()
    sortir.update_idletasks()

    # output in quotes for paths with spaces
    subprocess.run(f'advzip.exe -q -z -4 -i 20 "{filename}"', startupinfo=startupinfo)


# --------------------------------------------------------------
# Destroying dialog

sortir.destroy()
sortir.mainloop()

# Dialog destroyed and closed
# --------------------------------------------------------------
