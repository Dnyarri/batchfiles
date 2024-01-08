# Feeds selected PNG files to advpng.exe for recompression and reducing file size.
# advpng.exe is available from https://github.com/amadvance/advancecomp
#
#   WARNING:
#   Source files are replaced! No backup, no renaming!

from tkinter import filedialog
import subprocess

# Open source file list
sourcefilelist = filedialog.askopenfilenames(title='Select PNG files to recompress', filetypes=[('PNG files', '*.png')]) # filtering for PNG
if (sourcefilelist == ''):
    quit()

# Process file list string by string in cycle
for filename in sourcefilelist:
    subprocess.run(f'advpng.exe --recompress --shrink-insane --iter 50 "{filename}"')
    # output in quotes for paths with spaces
    # --shrink-insane --iter 50 means Zopfli compression with 50 iterations