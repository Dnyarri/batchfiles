# Useful batch scripts for files and dirs processing

Some batchfiles are equipped with GUI, some intended to be used as templates for further editing.
Most useful are:  

- **dir OPTIVORBIS ogg** - recompress all .ogg within dir and subdirs, using [OPTIVORBIS](https://git.codeproxy.net/OptiVorbis/OptiVorbis/releases); saves up to 10% of .ogg size.  

- **dir LibreOffice rtf2docx** - batch conversion of .rtf, .doc,  .odt and .fb2 files to .docx using [LibreOffice](https://www.libreoffice.org/). Overcomes clumsy LibreOffice idea of exporting all files into one dir.  

- **dir AdvZIP docx** - recompressing .docx after *dir LibreOffice rtf2docx* using [AdvZIP](https://github.com/amadvance/advancecomp) gives up to 10% space saving.  

- **filenames AdvPNG png** - recompressing .png using [AdvPNG](https://github.com/amadvance/advancecomp) gives up to 5% space saving.  

> [!NOTE]
> Windows users may rename forementioned files from .py to .pyw to avoid starting console.

- **dir RENAME unflibusta** - batch renaming of files according to patterns, like replacing underscores with spaces, removing digits, and so on. Edit rules pattern to your need.

> [!NOTE]
> *dir RENAME unflibusta.py* was initially created to batch fix silly filename convention for files downloaded from [Flibusta](https://flibusta.is/) and is supposed to be edited at will as you encounter any other silly file naming scheme.

[Dnyarri website](https://dnyarri.github.io)
