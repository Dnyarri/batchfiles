# Converts all the RTF, DOC and ODT within dir and subdirs to DOCX
# Main idea not mine, pulled from internet, I just added UI and added/changed some other stuff

import os
from subprocess import run
from tkinter import filedialog

# Open source dir
convert_dir = filedialog.askdirectory(title='Open DIR to process')
if (convert_dir == ''):
    quit()

for root, dirs, files in os.walk(convert_dir):
    for name in files:
        if name.endswith(".rtf") or name.endswith(".doc") or name.endswith(".odt"):
            # filepath+name
            file = root+"/"+name
            destination = root
            run(["D:/LibreOffice/program/soffice.exe", "--headless", "--convert-to", "docx", file, "--outdir", destination])    # with subprocess.Popen seem to get lost somewhere in the process
        else:
            pass