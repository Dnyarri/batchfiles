#!/usr/bin/env python3

'''
Compress selected dir and subdirs using Microsoft compact.exe LZX compression (LZX supported since Windows 8).
Since compact.exe itself provides recursion and stuff, this program does practically nothing
but provides nice GUI and remembers all the switches for me.

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "2024.05.19"
__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Production"

from tkinter import Tk, filedialog, Button, X, BOTH, TOP, BOTTOM

from tkinter.scrolledtext import ScrolledText

import subprocess

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('Compact dir with LZX')
sortir.geometry('+200+100')

pogovorit = ScrolledText(
    sortir, 
    height=26, 
    wrap='word', 
    state='normal'
)
pogovorit.pack(fill=BOTH, side=TOP, expand=True)

butt = Button(
    sortir,
    text='Bye',
    font=('arial', 14),
    cursor='hand2',
    justify='center',
    state='disabled',
    command=sortir.destroy
)
butt.pack(padx=4, pady=2, fill=X, side=BOTTOM, expand=True)

sortir.withdraw()

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to compress with LZX')
if (sourcedir == ''):
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
with subprocess.Popen(f'compact /c /s /a /i /f /exe:lzx "{sourcedir}/*"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, encoding='cp866', text=True, startupinfo=startupinfo) as p:
    for line in p.stdout:
        pogovorit.insert('end', line)
        pogovorit.see('end')
        sortir.update()
        sortir.update_idletasks()

butt.config(state='normal')

sortir.update()
sortir.update_idletasks()

sortir.mainloop()