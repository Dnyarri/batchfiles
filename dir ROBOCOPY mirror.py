#!/usr/bin/env python3

'''
Simple GUI to Windows robocopy.exe
Good example of redirecting console output to tkinter ScrolledText.
Unfortunately, it's also a good example of slowness of such an approach - simple .bat file is definitely faster.
Not recommended for real everyday use, yet good as a template.

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
sortir.title('Mirror dir with robocopy')
sortir.geometry('+200+100')

pogovorit = ScrolledText(sortir, height=26, wrap='word', state='normal')
pogovorit.pack(fill=BOTH, side=TOP, expand=True)

butt = Button(
    sortir, text='Bye', font=('arial', 14), cursor='hand2', justify='center', state='disabled', command=sortir.destroy
)
butt.pack(padx=4, pady=2, fill=X, side=BOTTOM, expand=True)

sortir.withdraw()

# Open source dir
sourcedir = filedialog.askdirectory(title='Source DIR')
if sourcedir == '':
    sortir.destroy()
    quit()

# Open copy dir
copydir = filedialog.askdirectory(title='Target DIR')
if copydir == '':
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
    f'robocopy "{sourcedir}" "{copydir}" /MIR /R:10 /W:5 /V /ETA',
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    bufsize=-1,
    encoding='cp866',
    text=True,
    startupinfo=startupinfo,
) as p:
    for line in p.stdout:
        pogovorit.insert('end', line)
        pogovorit.see('end')
        sortir.update()
        sortir.update_idletasks()

butt.config(state='normal')

sortir.update()
sortir.update_idletasks()

sortir.mainloop()
