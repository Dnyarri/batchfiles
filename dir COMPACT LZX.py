#!/usr/bin/env python3

"""GUI for selecting folder to compress with Microsoft ``compact.exe``
LZX compression (LZX supported since Windows 8).

Since ``compact.exe`` itself provides recursion and stuff,
this script does practically nothing but provides nice GUI
and remembers all the switches.

Current script supports commandline arguments.

Run::

    pythonw.exe "dir COMPACT LZX.py" "target_name"

to open in "target_name" dir, or add::

    pythonw.exe "dir COMPACT LZX.py.py" "%1"


to "Send to" or right-click or .bat, or create a shortcut
(use exact files addresses).

----
**More Python freeware**: `The Toad's Slimy Mudhole`_

.. _The Toad's Slimy Mudhole: https://dnyarri.github.io/

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024-2026 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2026.3.3'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import subprocess
from pathlib import Path
from sys import argv
from tkinter import Button, Tk, filedialog
from tkinter.scrolledtext import ScrolledText

if len(argv) == 2:
    try_open = argv[1]
    if Path(try_open).exists():
        if Path(try_open).is_file():
            try_open = Path(try_open).parent
    else:
        try_open = Path(try_open).parent
        if Path(try_open).exists():
            try_open = try_open
        else:
            try_open = Path.cwd()
else:
    try_open = None  # Normally makes it start in MRU

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('Compact dir with LZX')

pogovorit = ScrolledText(sortir, height=26, wrap='word', state='normal')
pogovorit.pack(fill='both', side='top', expand=True)

butt = Button(
    sortir,
    text='Busy...',
    font=('arial', 14),
    height=2,
    cursor='wait',
    justify='center',
    state='disabled',
    command=sortir.destroy,
)
butt.pack(padx=4, pady=2, fill='x', side='bottom', expand=True)

sortir.withdraw()

# Open source dir
source_dir = filedialog.askdirectory(title='DIR to compress with LZX', initialdir=try_open, mustexist=True)
if source_dir == '':
    sortir.destroy()

# Updating dialog
sortir.title(f'Compacting "{source_dir}/" with LZX')
sortir.deiconify()

# Center window horizontally, +100 vertically
sortir.update()
sortir.maxsize(9 * sortir.winfo_screenwidth() // 10, 9 * sortir.winfo_screenheight() // 10)
sortir.geometry(f'+{(sortir.winfo_screenwidth() - sortir.winfo_width()) // 2}+100')

# Updating scrolled text
pogovorit.insert('1.0', 'Allons-y!\n')
pogovorit.focus()
sortir.update()
sortir.update_idletasks()

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# Process dir
with subprocess.Popen(
    f'compact.exe /c /s /a /i /f /exe:lzx "{source_dir}/*"',
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

sortir.title(f'Compacting "{source_dir}/" finished')
butt.config(text='Finished, Dismissed!', bg='spring green', cursor='hand2', state='normal')

sortir.update()
sortir.update_idletasks()

sortir.mainloop()
