#!/usr/bin/env python3

"""Batch conversion of .rtf, .doc, and .odt files into .docx
in selected folder, recursively, by means of `LibreOffice`_.

May be used for any other conversion LibreOffice can handle
(for example, for conversion to pdf) by changing 'extension_list'
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
__version__ = '26.5.12.19'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import subprocess
from pathlib import Path
from tkinter import Button, Label, Tk, filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# List of extensions to convert from
extension_list = (
    '.rtf',
    '.doc',
    '.odt',
)

# Extension to convert to
convert_to_format = 'docx'

# Creating dialog
sortir = Tk()
sortir.title('rtf2docx LibreOffice converter')
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

sortir.withdraw()  # Main dialog created and hidden

# Open source dir
source_dir = filedialog.askdirectory(title='Open DIR to process')
if source_dir == '':
    sortir.destroy()
else:
    # Creating file list
    path = Path(source_dir)
    file_list = [p.resolve() for p in path.rglob('*.*') if p.suffix.lower() in extension_list]
    file_number = len(file_list)
    progressbar['maximum'] = file_number
    counter = 0

    # Updating dialog
    sortir.deiconify()

    # Center window horizontally, +100 vertically
    sortir.update()
    sortir.maxsize(9 * sortir.winfo_screenwidth() // 10, 9 * sortir.winfo_screenheight() // 10)
    sortir.geometry(f'+{(sortir.winfo_screenwidth() - sortir.winfo_width()) // 2}+100')

    # Updating text
    zanyato.config(text='Allons-y!')
    pogovorit.focus()
    pogovorit.insert('1.0', 'Allons-y!\n')
    sortir.update()
    sortir.update_idletasks()

    # Processing file list
    for filename in file_list:
        zanyato.config(text=f' Processing {filename}... ')  # Updating UI
        progressbar['value'] = counter
        counter += 1
        pogovorit.insert('end -1 chars', f' Starting {filename}...  ')
        pogovorit.see('end')
        sortir.update()
        sortir.update_idletasks()

        subprocess.run(f'D:/LibreOffice/program/soffice.exe --headless --convert-to {convert_to_format} "{filename}" --outdir "{(Path(filename)).parent}"')

        pogovorit.insert('end -1 chars', ' Done\n')
        sortir.update()
        sortir.update_idletasks()

    zanyato.config(text=f'Finished {source_dir.replace("/", "\\")}\\')
    progressbar['value'] = progressbar['maximum']
    sortir.after(1000, lambda: progressbar.stop())
    butt.config(text='Finished, Dismissed!', bg='spring green', cursor='hand2', state='normal')

sortir.mainloop()
