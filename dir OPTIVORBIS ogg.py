#!/usr/bin/env python3

"""Batch recompression of .ogg files in selected folder, recursively,
by means of `optivorbis.exe`_

Current script supports commandline arguments.

Run::

    pythonw.exe "dir OPTIVORBIS ogg.py" "target_name"

to open in "target_name" dir, or add::

    pythonw.exe "dir OPTIVORBIS ogg.py" "%1"

to "Send to" or right-click or .bat, or create a shortcut
(use exact files addresses).

.. warning:: program tries to find ``optivorbis.exe`` in CWD and PATH,
    and fail if ``optivorbis.exe`` is absent or placed out of search area.

----
**More Python freeware**: `The Toad's Slimy Mudhole`_

.. _The Toad's Slimy Mudhole: https://dnyarri.github.io/

**Optivorbis download**: `optivorbis.exe`_

.. _optivorbis.exe: https://github.com/OptiVorbis/OptiVorbis/

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024-2026 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '26.10.15.19'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import subprocess
from pathlib import Path
from shutil import which
from sys import argv
from time import time
from tkinter import Button, Label, Tk, filedialog
from tkinter.messagebox import showerror
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# ↓ In case command line or shortcut was used
if len(argv) == 2:
    try_open = argv[1]
    if Path(try_open).exists():
        if Path(try_open).is_file():
            try_open = Path(try_open).parent
    else:
        try_open = Path(try_open).parent
        if not Path(try_open).exists():
            try_open = Path.cwd()
else:
    try_open = None  # Normally makes it start in MRU

# ↓ Trying to find necessary executable
exe = 'optivorbis'
exe_location = which(exe)


def filesize(size: int) -> str:
    """Convert file size ``int`` in bytes to ``str`` in Gb or Mb or Kb with units."""
    return f'{size / 1073741824:.2f} Gb' if (size > 1073741824) else f'{size / 1048576:.2f} Mb' if (size > 1048576) else f'{size / 1024:.2f} Kb' if (size > 1024) else f'{size} bytes'


# ↓ Creating dialog
sortir = Tk()
sortir.title('Recompressing .OGG with OPTIVORBIS')
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

pogovorit.insert('1.0', f'{exe.capitalize()} found: {exe_location}\n')

# ↓ Quit if main exe was not found
if exe_location is None:
    showerror(
        title='Sorry',
        message=f'This program appeared to be unable to locate {exe}',
        detail=f'Either {exe} does not exist in your system,\nor is placed outside searchable PATH.',
    )
    sortir.destroy()
    raise SystemExit

# ↓ Open source dir
source_dir = filedialog.askdirectory(title='DIR to optimize OGG files', initialdir=try_open, mustexist=True)
if source_dir == '':
    sortir.destroy()
    raise SystemExit

# ↓ Creating file list
path = Path(source_dir).resolve()
# ↓ List of OGG files in subfolders. I need `len` for progress bar maximum,
#   therefore I need "solid" list rather than generator.
file_list = [p for p in path.rglob('*.ogg', case_sensitive=False)]
file_number = len(file_list)
progressbar['maximum'] = file_number
counter = 0

# ↓ Updating dialog
sortir.update()
sortir.maxsize(8 * sortir.winfo_screenwidth() // 10, 8 * sortir.winfo_screenheight() // 10)
sortir.geometry(f'+{(sortir.winfo_screenwidth() - sortir.winfo_width()) // 2}+64')

# ↓ Updating scrolled text
zanyato.config(text='Allons-y!')
pogovorit.focus()
pogovorit.insert('end -1 chars', f'Found {file_number} input files\nAllons-y!\n')
sortir.update()
sortir.update_idletasks()

# ↓ `startupinfo` to force subprocess window hide under Windows
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# ↓ Total size of files before and after
total_in = total_out = 0

start = time()

# ↓ Process file list
for counter, filename in enumerate(file_list):  # cycle through OGG files in subfolders
    zanyato.config(text=f' Processing {filename}... ')  # Updating UI, showing processed file name
    progressbar['value'] = counter
    pogovorit.insert('end -1 chars', f' Starting {filename}...  ')
    pogovorit.see('end')
    sortir.update()
    sortir.update_idletasks()

    currentfile = Path(filename).resolve()
    # ↑ file to be processed, resolved just in case
    size_in = Path(currentfile).stat().st_size  # file size
    total_in += size_in
    tempfile = Path(filename.resolve().parent / 'hujwam.ogg')
    # ↑ temp file `hujwam.ogg` in the same dir
    currentfile.replace(tempfile)  # rename `currentfile` to `tempfile`

    # ↓ Note: output in quotes below for paths with spaces
    subprocess.run(f'{exe_location} --quiet --vendor_string_action empty "{tempfile}" "{filename}"', startupinfo=startupinfo)  # noqa: PLW1510
    # ↑ optivorbis.exe writes result from temp back to source location

    size_out = Path(filename).stat().st_size  # file size
    total_out += size_out
    pogovorit.insert('end -1 chars', f' {filesize(size_in)} to {filesize(size_out)}\n')
    sortir.update()
    sortir.update_idletasks()

    tempfile.unlink(missing_ok=True)  # removing temp file

zanyato.config(text=f'Finished {source_dir.replace("/", "\\")}\\')
pogovorit.insert('end -1 chars', f'{exe.capitalize()} processed {file_number} files in {int(time() - start)} seconds\n')
pogovorit.insert('end -1 chars', f'Total {filesize(total_in)} to {filesize(total_out)} (benefit {filesize(total_in - total_out)} ({100 * (total_in - total_out) / total_in:.2f}%))\n')
pogovorit.see('end')
progressbar['value'] = progressbar['maximum']
sortir.after(1000, lambda: progressbar.stop())
sortir.title(f'Recompressing files in "{source_dir.replace("/", "\\")}\\" finished')
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
