#!/usr/bin/env python3

'''
Opens a folder, and recursively feeds all flac files in it to ffmpeg.exe
for conversion to ogg 16 bit 44.1 kHz, removing built-in preview and other junk.

ffmpeg.exe is available from https://github.com/BtbN/FFmpeg-Builds/
("shared" release)

Resulting ogg files are placed side by side with flac source files.

Also supports commandline arguments. Run:

``pythonw.exe "dir ffmpeg flac2ogg 44.py" "target_name"``

to open in "target_name" dir, or add

``pythonw.exe "dir ffmpeg flac2ogg 44.py" "%1"``

to "Send to" or right-click or .bat (use exact addresses of pythonw and this file)

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "2024.11.16"
__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Production"

import subprocess
from pathlib import Path
from sys import argv
from tkinter import BOTH, BOTTOM, Button, Label, PhotoImage, Tk, X, filedialog
from tkinter.scrolledtext import ScrolledText

'''
run:

``python "dir ffmpeg flac2ogg 44.py" "target_name"``

to open in "target_name" dir

'''

# Add required file extensions here
extension_list = ['.flac', '.wav', '.dsf', '.ape']

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
    tryopen = Path.cwd()

# Creating dialog
sortir = Tk()
sortir.title('flac2ogg 44.1 kHz')
sortir.geometry('+100+100')
sortir.maxsize(800, 600)
sortir.iconphoto(True, PhotoImage(data=b'P6\n2 2\n255\n\xff\x00\x00\xff\xff\x00\x00\x00\xff\x00\xff\x00'))
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
    command=sortir.destroy,
)
butt.pack(fill=X, side=BOTTOM, expand=True)

pogovorit.insert('1.0', 'Allons-y!\n')

sortir.withdraw()  # Main dialog created and hidden

# Open source dir
sourcedir = filedialog.askdirectory(title='DIR to convert FLAC to OGG 16 bit 44.1 kHz', initialdir=tryopen, mustexist=True)
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

# Creating file list
file_list = (p.resolve() for p in path.rglob('*.*') if p.suffix in extension_list)

# Processing file list
for filename in file_list:

    zanyato.config(text=f'Processing {filename}...')  # Updating UI, showing processed file name
    pogovorit.insert('end -1 chars', f' Starting {filename}...  ')
    pogovorit.see('end')
    sortir.update()
    sortir.update_idletasks()

    currentfile = Path(filename).resolve()  # file to be processed
    currentdir = Path(filename).resolve().parent  # dir with current file
    currentfile_noext = str(Path(filename).resolve().stem)  # file to be processed without extension
    oggfile = f'{currentdir}\\{currentfile_noext}.ogg'  # resulting file name

    # Note: output in quotes below for paths with spaces
    subprocess.run(
        f'ffmpeg.exe -loglevel quiet -i "{currentfile}" -map 0:a:? -c:a: libvorbis -aq 10 -af aresample=out_sample_fmt=s16:out_sample_rate=44100 -vn -sn -map_metadata:s:0 0:s:0 -metadata comment="" -metadata encoder="" -metadata description="" -metadata copyright="" -metadata encoded_by="" "{oggfile}"',
        startupinfo=startupinfo,
    )

    # currentfile.unlink(missing_ok=True)        # removing source file

    pogovorit.insert('end -1 chars', ' Done\n')
    sortir.update()
    sortir.update_idletasks()

zanyato.config(text=f'Finished {sourcedir}')
butt.config(text='Finished, Dismissed!', state='normal')

sortir.mainloop()
