# Feeds selected PNG files to truepng.exe for recompression and reducing file size.
#   WARNING:
#   Source files are replaced! No backup, no renaming!

from tkinter import filedialog
from subprocess import run

# Open source file list
sourcefilelist = filedialog.askopenfilenames(title='Select PNG files to recompress', filetypes=[('PNG files', '*.png')]) # filtering for PNG
if (sourcefilelist == ''):
    quit()

# Process file list string by string in cycle
for filename in sourcefilelist:
    run(f'truepng.exe /o4 "{filename}"')
    # output in quotes for paths with spaces
    # /o4 supposed to be /zc9 /zm1-9 /zs0,1,3 /fe /a1 /i0 /md remove all