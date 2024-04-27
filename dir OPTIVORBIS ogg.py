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
__version__ = "2024.04.27"
__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Production"

from tkinter import Tk, filedialog, Label, X, BOTH, LEFT

from tkinter.ttk import Progressbar

from tkinter.scrolledtext import ScrolledText

import os

from glob import glob
import subprocess

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('Recompressing .OGG...')
sortir.geometry('+100+100')
zanyato = Label(sortir, text='Starting...', font=("arial", 12), padx=16, pady=10, justify='center')
zanyato.pack()
    
progressbar =  Progressbar(sortir, orient="horizontal", mode="indeterminate")
progressbar.pack(fill=X)

pogovorit = ScrolledText(sortir, height=26, wrap='word', state='normal')
pogovorit.pack(fill=BOTH, side=LEFT, expand=True)
pogovorit.insert('1.0', 'Allons-y!\n')

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

    zanyato.config(text=f'Processing {filename}...')      # Updating label, showing processed file name
    progressbar.start(50)
    pogovorit.insert('end -1 chars', f' Starting {filename}... ')
    sortir.update()
    sortir.update_idletasks()

    os.rename(f"{filename}", "D:/hujwam.ogg")
    # output in quotes for paths with spaces
    subprocess.run(f'"optivorbis.exe" "-q" "D:/hujwam.ogg" "{filename}"', startupinfo=startupinfo)
    os.remove("D:/hujwam.ogg")

        
    progressbar.start(50)
    pogovorit.insert('end -1 chars', ' Done\n')

# --------------------------------------------------------------
# Destroying dialog

sortir.destroy()
sortir.mainloop()

# Dialog destroyed and closed
# --------------------------------------------------------------
