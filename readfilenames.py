from tkinter import filedialog

# Open source file list
sourcefilelist = filedialog.askopenfilenames(title='Select OGG files to recompress', filetypes=[('OGG Vorbis files', '*.ogg')]) # originally intended for OGG, change to anything else
if (sourcefilelist == ''):
    quit()

# Print file list tuple
print(sourcefilelist)

# Print file list string by string in cycle
for i in sourcefilelist:
    print(f'"Идите в" "{i}"') # output in quotes for paths with spaces