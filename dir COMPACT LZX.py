#!/usr/bin/env python3

"""
Compress selected dir and subdirs using Microsoft compact.exe LZX compression (LZX supported since Windows 8).
Since compact.exe itself provides recursion and stuff, this program does practically nothing
but provides nice GUI and remembers all the switches for me.

Also supports commandline arguments. Run:

``pythonw.exe "dir COMPACT LZX.py" "target_name"``

to open in "target_name" dir, or add

``pythonw.exe "dir COMPACT LZX.py.py" "%1"``

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
from tkinter import Button, Tk, filedialog
from tkinter.scrolledtext import ScrolledText

"""
run:

``python "dir COMPACT LZX.py" "target_name"``

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

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('Compact dir with LZX')
sortir.geometry('+200+100')
sortir.maxsize(800, 600)

pogovorit = ScrolledText(sortir, height=26, wrap='word', state='normal')
pogovorit.pack(fill='both', side='top', expand=True)

butt = Button(
    sortir,
    text='Busy...',
    font=('arial', 14),
    cursor='hand2',
    justify='center',
    state='disabled',
    command=sortir.destroy,
)
butt.pack(padx=4, pady=2, fill='x', side='bottom', expand=True)

sortir.withdraw()

# Open source dir
sourcedir = filedialog.askdirectory(title='DIR to compress with LZX', initialdir=tryopen, mustexist=True)
if sourcedir == '':
    sortir.destroy()
    quit()

# Updating dialog
sortir.deiconify()
pogovorit.insert('1.0', 'Allons-y!\n')
pogovorit.focus()
sortir.update()
sortir.update_idletasks()

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# Process dir
with subprocess.Popen(
    f'compact.exe /c /s /a /i /f /exe:lzx "{sourcedir}/*"',
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    bufsize=1,
    encoding='cp866',
    text=True,
    startupinfo=startupinfo,
) as p:
    for line in p.stdout:
        pogovorit.insert('end', line)
        pogovorit.see('end')
        sortir.update()
        sortir.update_idletasks()

butt.config(text='Finished, Dismissed!', bg='spring green', state='normal')

sortir.update()
sortir.update_idletasks()

sortir.mainloop()
