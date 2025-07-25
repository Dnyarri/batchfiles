#!/usr/bin/env python3

"""
Batch conversion of .rtf, .doc, .odt and .fb2 files into .docx in selected folder, recursively,
by means of LibreOffice.

May be used for any other conversion LibreOffice can handle (for example, for conversion to pdf) by changing 'extension_list' and 'convert_to_format' appropriately.

Warning: LibreOffice location is hardcoded directly, change it to match you computer.

Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)

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
from tkinter import Button, Label, Tk, filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# List of extensions to convert from
extension_list = {'.rtf', '.doc', '.odt', '.fb2'}

# Extension to convert to
convert_to_format = 'docx'

# Creating dialog
sortir = Tk()
sortir.title('rtf2docx LibreOffice converter')
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

sortir.withdraw()  # Main dialog created and hidden

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to process')
if sourcedir == '':
    sortir.destroy()
    quit()

path = Path(sourcedir)

# Updating dialog
sortir.deiconify()
zanyato.config(text='Allons-y!')
pogovorit.focus()
pogovorit.insert('1.0', 'Allons-y!\n')
sortir.update()
sortir.update_idletasks()

# Creating file list
file_list = (p.resolve() for p in path.rglob('*.*') if p.suffix in extension_list)

# Processing file list
for filename in file_list:
    zanyato.config(text=f' Processing {filename}... ')  # Updating UI
    progressbar.start(50)
    pogovorit.insert('end -1 chars', f' Starting {filename}...  ')
    pogovorit.see('end')
    sortir.update()
    sortir.update_idletasks()

    subprocess.run(f'D:/LibreOffice/program/soffice.exe --headless --convert-to {convert_to_format} "{filename}" --outdir "{(Path(filename)).parent}"')

    progressbar.start(50)  # Updating UI
    pogovorit.insert('end -1 chars', ' Done\n')
    sortir.update()
    sortir.update_idletasks()

zanyato.config(text=f'Finished {sourcedir}')
progressbar.stop()
butt.config(text='Finished, Dismissed!', bg='spring green', state='normal')

sortir.mainloop()
