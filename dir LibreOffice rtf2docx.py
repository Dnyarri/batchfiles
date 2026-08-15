#!/usr/bin/env python3

"""Batch conversion of .rtf, .doc, and .odt files into .docx
in selected folder, recursively, by means of `LibreOffice`_.

May be used for any other conversion LibreOffice can handle
(for example, for conversion to pdf) by changing 'convert_from_format'
and 'convert_to_format' appropriately.

.. warning:: LibreOffice location is hardcoded directly,
    change it to match you computer.

----
**More Python freeware**: `The Toad's Slimy Mudhole`_

.. _The Toad's Slimy Mudhole: https://dnyarri.github.io/

**LibreOffice download**: `LibreOffice`_

.. _LibreOffice: https://www.libreoffice.org/download/download-libreoffice/

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024-2026 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '26.8.14.18'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import subprocess
import winreg
from os import name
from pathlib import Path
from shutil import which
from time import time
from tkinter import Button, Label, Tk, filedialog
from tkinter.messagebox import showerror
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# ↓ List of extensions to convert from
convert_from_format = (
    '.rtf',
    '.doc',
    '.odt',
)
# ↓ Extension to convert to
convert_to_format = 'docx'

# ↓ Trying to find LibreOffice
if name == 'nt':
    key_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\soffice.exe'
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ) as key:
            exe_location = winreg.QueryValue(key, '')  # Return file path
    except:  # noqa: E722
        exe_location = None
else:
    exe_location = which('soffice')

# ↓ Creating dialog
sortir = Tk()
sortir.title('rtf2docx LibreOffice converter')
icon_path = Path(__file__).resolve().parent / 'dnyarri.ico'
if icon_path.exists():
    sortir.iconbitmap(icon_path)

zanyato = Label(
    sortir,
    wraplength=700,
    text='Starting...',
    font=('helvetica', 12),
    padx=16,
    pady=10,
    justify='center',
)
zanyato.pack()

progressbar = Progressbar(sortir, orient='horizontal')
progressbar.pack(fill='x', side='top', expand=True)

pogovorit = ScrolledText(
    sortir,
    height=26,
    wrap='word',
    state='normal',
)
pogovorit.pack(fill='both', expand=True)

butt = Button(
    sortir,
    text='Busy...',
    font=('helvetica', 14),
    height=2,
    cursor='wait',
    justify='center',
    state='disabled',
    command=sortir.destroy,
)
butt.pack(fill='x', side='bottom', expand=True)

# ↓ Quit if main exe was not found
if exe_location is None:
    showerror(
        title='Sorry',
        message='This program appeared to be unable to locate LibreOffice!',
        detail='Either LibreOffice is not installed, or... well, I have no idea.',
    )
    sortir.destroy()
    raise SystemExit

# ↓ Open source dir
source_dir = filedialog.askdirectory(title='DIR to process RTF to DOCX')
if source_dir == '':
    sortir.destroy()
    raise SystemExit

# ↓ Creating file list
path = Path(source_dir)
file_list = [p.resolve() for p in path.rglob('*.*') if p.suffix.lower() in convert_from_format]
file_number = len(file_list)
progressbar['maximum'] = file_number
counter = 0

# ↓ Updating dialog
sortir.update()
sortir.maxsize(8 * sortir.winfo_screenwidth() // 10, 8 * sortir.winfo_screenheight() // 10)
sortir.geometry(f'+{(sortir.winfo_screenwidth() - sortir.winfo_width()) // 2}+64')

# ↓ Updating text
zanyato.config(text='Starting LibreOffice...')
pogovorit.focus()
pogovorit.insert('1.0', f'LibreOffice found: {exe_location}\n')
pogovorit.insert('end -1 chars', f'Found {file_number} input files\n')
pogovorit.insert('end -1 chars', 'Allons-y!\n')
sortir.update()
sortir.update_idletasks()

start = time()

# ↓ Processing file list
for counter, filename in enumerate(file_list):
    zanyato.config(text=f' Processing {filename}... ')  # Updating UI
    progressbar['value'] = counter
    pogovorit.insert('end -1 chars', f' Starting {filename}...  ')
    pogovorit.see('end')
    sortir.update()
    sortir.update_idletasks()

    subprocess.run(f'{exe_location} --headless --convert-to {convert_to_format} "{filename}" --outdir "{(Path(filename)).parent}"')  # noqa: PLW1510

    pogovorit.insert('end -1 chars', ' Done\n')
    sortir.update()
    sortir.update_idletasks()

zanyato.config(text=f'Finished {source_dir.replace("/", "\\")}\\')
pogovorit.insert('end -1 chars', f'{exe_location.capitalize()} processed {file_number} files in {int(time() - start)} seconds\n')
pogovorit.see('end')
progressbar['value'] = progressbar['maximum']
sortir.after(1000, lambda: progressbar.stop())
sortir.title(f'Converting files in "{source_dir.replace("/", "\\")}\\" finished')
butt.config(
    text='Finished, Dismissed!',
    background='green1',
    cursor='hand2',
    state='normal',
)
sortir.after(
    1000,
    lambda: butt.config(
        background='green3',
        activebackground='green1',
    ),
)

sortir.mainloop()
