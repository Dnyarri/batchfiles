#!/usr/bin/env python3

'''
Feeds selected PNG files to advpng.exe for recompression and reducing file size.
advpng.exe is available from https://github.com/amadvance/advancecomp

WARNING:
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

import os

import subprocess

from tkinter import Tk
from tkinter import Label
from tkinter import filedialog

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('Recompressing .PNG...')
sortir.geometry('+100+100')
zanyato = Label(sortir, text='Starting...', font=("arial", 12), padx=16, pady=10, justify='center')
zanyato.pack()
sortir.withdraw()

# Main dialog created and hidden
# --------------------------------------------------------------

# Open source file list
sourcefilelist = filedialog.askopenfilenames(
    title='Select PNG files to recompress', filetypes=[('PNG files', '*.png')]
)  # filtering for PNG
if sourcefilelist == '':
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


# Process file list string by string in cycle
for filename in sourcefilelist:

    zanyato.config(text='Processing ' + filename + '...')  # Updating label, showing processed file name
    sortir.update()
    sortir.update_idletasks()

    subprocess.run(f'advpng.exe --recompress --shrink-insane --iter 50 --quiet "{filename}"', startupinfo=startupinfo)
    # output in quotes for paths with spaces
    # --shrink-insane --iter 50 means Zopfli compression with 50 iterations

# --------------------------------------------------------------
# Destroying dialog

sortir.destroy()
sortir.mainloop()

# Dialog destroyed and closed
# --------------------------------------------------------------
