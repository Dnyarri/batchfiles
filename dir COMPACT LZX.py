# Compress selected dir and subdirs using Microsoft compact.exe LZX compression (LZX supported since Windows 8).
# Since compact.exe itself provides recursion and stuff, this program does practically nothing
# but provides GUI and remembers all the switches for me.

from tkinter import filedialog
from subprocess import run

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to COMPACT')
if (sourcedir == ''):
    quit()
# Process dir
run(f'compact /c /s /a /i /f /exe:lzx "{sourcedir}\*"')