#!/usr/bin/env python3

"""
Opens a folder, and recursively feeds all .docx and .zip files in it
to `advzip`_ for recompression and reducing file size.

.. warning:: advzip.exe location is hardcoded directly,
    change it to match you computer.

----
**More Python freeware**: `The Toad's Slimy Mudhole`_

.. _The Toad's Slimy Mudhole: https://dnyarri.github.io/

**advzip**: `advzip`_

.. _advzip: https://github.com/amadvance/advancecomp

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024-2026 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '26.5.12.19'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import subprocess
from pathlib import Path
from sys import argv
from tkinter import Button, Label, Tk, filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# ↓ Add required file extensions here
extension_list = (
    '.docx',
    '.zip',
)

# ↓ In case command line or shortcut was used
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

# ↓ Creating dialog
sortir = Tk()
sortir.title('dir AdvZIP docx')
icon_path = Path(__file__).resolve().parent / 'dnyarri.ico'
if icon_path.exists():
    sortir.iconbitmap(icon_path)

zanyato = Label(sortir, wraplength=700, text='Starting...', font=('arial', 12), padx=16, pady=10, justify='center')
zanyato.pack()

progressbar = Progressbar(sortir, orient='horizontal')
progressbar.pack(fill='x', side='top', expand=True)

pogovorit = ScrolledText(sortir, height=26, wrap='word', state='normal')
pogovorit.pack(fill='both', expand=True)

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
butt.pack(fill='x', side='bottom', expand=True)

pogovorit.insert('1.0', 'Allons-y!\n')

sortir.withdraw()  # Main dialog created and hidden

# ↓ Open source dir
source_dir = filedialog.askdirectory(title='DIR to compress DOCX in it', initialdir=try_open, mustexist=True)
if source_dir == '':
    sortir.destroy()
else:
    path = Path(source_dir)
    file_list = [p.resolve() for p in path.rglob('*.*') if p.suffix.lower() in extension_list]
    file_number = len(file_list)
    progressbar['maximum'] = file_number
    counter = 0

    # ↓ Updating dialog
    sortir.update()
    sortir.maxsize(9 * sortir.winfo_screenwidth() // 10, 9 * sortir.winfo_screenheight() // 10)
    sortir.geometry(f'+{(sortir.winfo_screenwidth() - sortir.winfo_width()) // 2}+100')

    # ↓ Updating scrolled text
    zanyato.config(text='Allons-y!')
    pogovorit.focus()
    sortir.update()
    sortir.update_idletasks()

    # ↓ Helping hide console under Windows when it doesn't want to
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # ↓ Creating file list
    file_list = (p.resolve() for p in path.rglob('*.*') if p.suffix.lower() in extension_list)

    # ↓ Processing file list
    for filename in file_list:
        zanyato.config(text=f'Processing {filename}...')  # Updating UI, showing processed file name
        progressbar['value'] = counter
        counter += 1
        pogovorit.insert('end -1 chars', f' Starting {filename}...  ')
        pogovorit.see('end')
        sortir.update()
        sortir.update_idletasks()

        # ↓ Note: output in quotes below for paths with spaces
        subprocess.run(f'advzip.exe -q -z -4 -i 30 "{filename}"', startupinfo=startupinfo)

        pogovorit.insert('end -1 chars', ' Done\n')
        sortir.update()
        sortir.update_idletasks()

    zanyato.config(text=f'Finished {source_dir.replace("/", "\\")}\\')
    progressbar['value'] = progressbar['maximum']
    sortir.after(1000, lambda: progressbar.stop())
    butt.config(text='Finished, Dismissed!', bg='spring green', cursor='hand2', state='normal')

sortir.mainloop()
