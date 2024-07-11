#!/usr/bin/env python3

'''
Opens a folder, and recursively feeds all flac files in it to ffmpeg.exe
for conversion to ogg 48 kHz, removing built-in preview and other junk.

ffmpeg.exe is available from https://github.com/BtbN/FFmpeg-Builds/
("shared" release)

Resulting ogg files are placed side by side with flac source files.

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "2024.07.11"
__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Production"

from tkinter import Tk, filedialog, Button, Label, X, BOTH, BOTTOM
from tkinter.scrolledtext import ScrolledText

from pathlib import Path

import subprocess

# Creating dialog
sortir = Tk()
sortir.title('flac2ogg 48 kHz')
sortir.geometry('+100+100')
sortir.maxsize(800, 600)
zanyato = Label(sortir, wraplength=800, text='Starting...', font=('arial', 12), padx=16, pady=10, justify='center')
zanyato.pack()
    
pogovorit = ScrolledText(sortir, height=26, wrap='word', state='normal')
pogovorit.pack(fill=BOTH, expand=True)

butt = Button(
    sortir,
    text='Busy...',
    font=('arial', 14),
    cursor='hand2',
    justify='center',
    state='disabled',
    command=sortir.destroy
)
butt.pack(fill=X, side=BOTTOM, expand=True)

pogovorit.insert('1.0', 'Allons-y!\n')

sortir.withdraw()   # Main dialog created and hidden

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to process FLAC to OGG')
if (sourcedir == ''):
    sortir.destroy()
    quit()

path=Path(sourcedir)

# Updating dialog
sortir.deiconify()
zanyato.config(text='Allons-y!')
pogovorit.focus()
sortir.update()
sortir.update_idletasks()

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# Process file list
for filename in path.rglob('*.flac', case_sensitive=False):  # cycle through flac files in subfolders

    zanyato.config(text=f'Processing {filename}...')    # Updating UI, showing processed file name
    pogovorit.insert('end -1 chars', f' Starting {filename}...  ')
    pogovorit.see('end')
    sortir.update()
    sortir.update_idletasks()

    currentfile = Path(filename).resolve()  # file to be processed
    currentdir = Path(filename).resolve().parent    # dir with current file
    currentfile_noext = str(Path(filename).resolve().stem)  # file to be processed without extension
    oggfile = f'{currentdir}\\{currentfile_noext}.ogg'  # resulting file name
    
    # print(f'{currentfile}\n{oggfile}')

    # Note: output in quotes below for paths with spaces
    subprocess.run(f'ffmpeg.exe -loglevel quiet -i "{currentfile}" -map 0:a:? -c:a: libvorbis -aq 10 -ar 48000 -vn -sn -map_metadata:s:0 0:s:0 -metadata comment="" -metadata encoder="" -metadata description="" -metadata copyright="" -metadata encoded_by="" "{oggfile}"', startupinfo=startupinfo)

    # currentfile.unlink(missing_ok=True)        # removing source file

    pogovorit.insert('end -1 chars', ' Done\n')
    sortir.update()
    sortir.update_idletasks()

zanyato.config(text=f'Finished {sourcedir}')
butt.config(text='Dismissed!', state='normal')

sortir.mainloop()
