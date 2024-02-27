#!/usr/bin/env python

'''
Batch conversion of *.rtf, *.doc and *.odt into .docx in selected folder, recursively,
by means of LibreOffice.

Warning: LibreOffice location is hardcoded directly, change it to match you computer.

Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)

Versions:
2024.02.26  GUI added, minimizing import, versioning changed to YYYY.MM.DD

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "2024.02.26"
__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Production"

from os import walk
from subprocess import run

from tkinter import Tk
from tkinter import Label
from tkinter import filedialog

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('Converting to .docx...')
sortir.geometry('+100+100')
zanyato = Label(sortir, text = 'Starting...', font=("arial", 12), padx=16, pady=10, justify='center')
zanyato.pack()
sortir.withdraw()

# Main dialog created and hidden
# --------------------------------------------------------------

# Open source dir
workingdir = filedialog.askdirectory(title='Open DIR to process')
if (workingdir == ''):
    quit()

# --------------------------------------------------------------
# Updating dialog

sortir.deiconify()
zanyato.config(text = 'Allons-y!')
sortir.update()
sortir.update_idletasks()

# Dialog shown and updated
# --------------------------------------------------------------

for root, dirs, files in walk(workingdir):
    for filename in files:
        if filename.endswith(".rtf") or filename.endswith(".doc") or filename.endswith(".odt") or filename.endswith(".fb2"):
            # filepath+filename
            file = root+"/"+filename
            destination = root

            zanyato.config(text = 'Processing ' + file + '...')      # Updating label, showing processed file name
            sortir.update()
            sortir.update_idletasks()

            run(["D:/LibreOffice/program/soffice.exe", "--headless", "--convert-to", "docx", file, "--outdir", destination])    # with subprocess.Popen seem to get lost somewhere in the process
        else:
            pass


# --------------------------------------------------------------
# Destroying dialog

sortir.destroy()
sortir.mainloop()

# Dialog destroyed and closed
# --------------------------------------------------------------
