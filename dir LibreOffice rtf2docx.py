# Main idea not mine, pulled from internet, I just added UI and fixed some minor stuff

import os
import subprocess
from tkinter import filedialog
from winsound import Beep

# Open source dir
convert_dir = filedialog.askdirectory(title='Open DIR to process')
if (convert_dir == ''):
    quit()

for root, dirs, files in os.walk(convert_dir):
    for name in files:
        if name.endswith(".rtf"):
            # filepath+name
            file = root+"/"+name
            destination = root
            subprocess.call(["D:/LibreOffice/program/soffice.exe", "--headless", "--convert-to", "docx", file, "--outdir", destination])    # with subprocess.Popen seem to get lost somewhere in the process
        else:
            pass

Beep(300, 1200)