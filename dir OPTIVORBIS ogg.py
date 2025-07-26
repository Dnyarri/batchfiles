#!/usr/bin/env python3

"""
Opens a folder, and recursively feeds all OGG files in it to
optivorbis.exe
for recompression and reducing file size.

optivorbis.exe is available from https://github.com/OptiVorbis/OptiVorbis/

WARNING:
Source files are replaced! No backup, no mercy!

Also supports commandline arguments. Run:

``pythonw.exe "dir OPTIVORBIS ogg.py" "target_name"``

to open in "target_name" dir, or add

``pythonw.exe "dir OPTIVORBIS ogg.py" "%1"``

to "Send to" or right-click or .bat (use exact addresses of pythonw and this file)

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2025.07.25'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import subprocess
from pathlib import Path
from sys import argv
from tkinter import Button, Label, Tk, filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

"""
run:

``python "dir OPTIVORBIS ogg.py" "target_name"``

to open in "target_name" dir
"""
if len(argv) == 2:
    tryopen = argv[1]
    if Path(tryopen).exists():
        if Path(tryopen).is_file():
            tryopen = Path(tryopen).parent
    else:
        tryopen = Path(tryopen).parent
        if Path(tryopen).exists():
            tryopen = tryopen
        else:
            tryopen = Path.cwd()
else:
    tryopen = None  # Normally makes it start in MRU

# Creating dialog
sortir = Tk()
sortir.title('Recompressing .OGG...')
sortir.geometry('+100+100')
sortir.maxsize(800, 600)
zanyato = Label(sortir, wraplength=700, text='Starting...', font=('arial', 12), padx=16, pady=10, justify='center')
zanyato.pack()

progressbar = Progressbar(sortir, orient='horizontal', mode='indeterminate')
progressbar.pack(fill='x', side='top', expand=True)

pogovorit = ScrolledText(sortir, height=26, wrap='word', state='normal')
pogovorit.pack(fill='both', expand=True)

butt = Button(
    sortir,
    text='Busy...',
    font=('arial', 14),
    cursor='hand2',
    justify='center',
    state='disabled',
    command=sortir.destroy,
)
butt.pack(fill='x', side='bottom', expand=True)

pogovorit.insert('1.0', 'Allons-y!\n')

sortir.withdraw()  # Main dialog created and hidden

# Open source dir
sourcedir = filedialog.askdirectory(title='DIR to optimize OGG files', initialdir=tryopen, mustexist=True)
if sourcedir == '':
    sortir.destroy()
    quit()

path = Path(sourcedir)

# Updating dialog
sortir.deiconify()
zanyato.config(text='Allons-y!')
pogovorit.focus()
sortir.update()
sortir.update_idletasks()

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# Process file list
for filename in path.rglob('*.ogg', case_sensitive=False):  # cycle through OGG files in subfolders
    zanyato.config(text=f' Processing {filename}... ')  # Updating UI, showing processed file name
    progressbar.start(50)
    pogovorit.insert('end -1 chars', f' Starting {filename}...  ')
    pogovorit.see('end')
    sortir.update()
    sortir.update_idletasks()

    currentfile = Path(filename).resolve()  # file to be processed
    tempfile = Path(filename.resolve().parent / 'hujwam.ogg')  # temp file hujwam.ogg
    currentfile.replace(tempfile)  # move file to temp

    # Note: output in quotes below for paths with spaces
    subprocess.run(f'optivorbis.exe --quiet --vendor_string_action empty "{tempfile}" "{filename}"', startupinfo=startupinfo)
    # optivorbis.exe writes result from temp back to source location

    progressbar.start(50)
    pogovorit.insert('end -1 chars', ' Done\n')
    sortir.update()
    sortir.update_idletasks()

    tempfile.unlink(missing_ok=True)  # removing temp file

zanyato.config(text=f'Finished {sourcedir}')
progressbar.stop()
butt.config(text='Finished, Dismissed!', bg='spring green', state='normal')

sortir.mainloop()
