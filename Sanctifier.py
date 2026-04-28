#!/usr/bin/env python3

"""
Sanctifier
==========

Sanctify PNG files by converting them to icons
----------------------------------------------

Sanctifier is a simple program for converting a set of PNG files
into a Windows icon ICO file. Resulting compressed icon files
are intended to be used with Windows Vista and above.

Basically it's a GUI implementation of CLI program `Make Icon From PNGs`_
made by Mikael Klasson.

Since I appeared to be unable to make it work, the simplest way to overcome
my personal stupidity was writing my own stupid-friendly GUI.

Main advantage of Sanctifier as an icon assembling tool is that it does
nothing but insert PNG files into Windows ICO skeleton framework.
It does not resize images, it does not change their color mode,
it does not remove colors it considers unnecessary, *etc.*; actually
it does not open images at all. It simply transfers PNG image data "as is"
into icon file. "As is", in particular, means that the better source
PNG compression is, the smaller resulting ICO file will be.

This approach enables you to either make mistakes or, otherwise, be smart
and use best specialized PNG optimizing software, thus making resulting
ICO file size noticeably smaller than that provided by regular icon editors,
based upon regular PNG implementation.

Therefore, suggested workflow is as following:

1. Create a set of images (according to `Icons (Design basics)`_
   16, 32, 48 and 256 pixel sizes seem to be a minimal set,
   although adding 20, 24, 40, 64 and 96 px is often recommended),
   and save a copies of your working images as PNG files **in one folder**.
2. Run a PNG optimizer on these files (`oxipng`_ gives *ca.* 10% savings).
3. Start Sanctifier.py. Immediately a file *"Open"* dialog, allowing
   multiple selection, will pop up.

   .. note:: Select **all** the necessary files at once, then
        press *"Open"* button.
        Sanctifier is a simple program and does not support creating projects,
        selecting files across different folders,
        adding or deleting files later, *etc.*

4. If necessary, change icon images order by changing file order in file list
   by selecting a file name and pressing *Ctrl+Up* or *Ctrl+Down* to move
   selected item up or down; *Ctrl+I* fully inverts the list order.
5. Once satisfied with file list order, press *Enter*;
   icon file *"Save as"* dialog will pop up.
6. If you feel like making one more icon, press *Ctrl+O* to open new file list.
7. Once finished, don't forget to exit Sanctifier by pressing *Ctrl+Q*.

References
----------

1. Original `Make Icon From PNGs`_ program.
2. Microsoft's `Icons (Design basics)`_ recommendations.
3. Efficient yet fast PNG optimizer `oxipng`_ repository.

.. _Make Icon From PNGs: https://github.com/emklasson/make-icon-from-pngs

.. _Icons (Design basics): https://learn.microsoft.com/en-us/windows/win32/uxguide/vis-icons

.. _oxipng: https://github.com/oxipng/oxipng

----
Main site: `The Toad's Slimy Mudhole`_

.. _The Toad's Slimy Mudhole: https://dnyarri.github.io

The Toad's Batchroom repositories: main `@Github`_ and mirror `@Gitflic`_

.. _@Github: https://github.com/Dnyarri/batchfiles

.. _@Gitflic: https://gitflic.ru/project/dnyarri/batchfiles

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2026 Ilya Razmanov'
__credits__ = ['Mikael Klasson', 'Ilya Razmanov']
__license__ = 'unlicense'
__version__ = '26.4.28.18'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from tkinter import Label, Listbox, StringVar, Tk, filedialog


def DisMiss(event=None) -> None:
    """Kill dialog and continue."""

    sortir.destroy()


def getList(event=None):
    """Get source file list."""

    global png_list, png_list_str
    png_list = list(  # askopenfilenames returns tuple, not a list
        filedialog.askopenfilenames(
            parent=sortir,
            title='Select PNG files to sanctify',
            filetypes=[
                ('Portable network graphics', '.png'),
            ],
        )
    )
    if png_list == []:  # User pressed `Esc`
        png_list = ['No PNG file chosen']  # Dummy for `png_list` and `png_list[0]` to have a `len`
        zanyato['text'] = 'Sanctify your PNGs - convert them to ICON!'
        sortir.unbind_all('<Return>')  # User pressed `Esc` in a non-first run
    else:
        sortir.bind_all('<Return>', Sanctify)  # Bind export only for non-empty list
    png_list_str.set(png_list)  # Updating StringVar with new list
    png_listbox.select_set(first=0)
    # ↓ Readopting 'sortir.minsize' to fit the screen.
    png_listbox['width'] = max(60, max(len(filename) for filename in png_list))
    png_listbox['height'] = len(png_list) + 1
    sortir.update()
    fit_width = min(sortir.winfo_reqwidth(), 8 * sortir.winfo_screenwidth() // 10)
    fit_height = min(sortir.winfo_reqheight(), 8 * sortir.winfo_screenheight() // 10)
    sortir.minsize(fit_width, fit_height)


def showSelected(event=None) -> None:
    """Show item, selected in Listbox, in Label below."""

    n = png_listbox.curselection()[0]  # curselection() returns tuple[int,]
    zanyato['text'] = f'Icon № {n + 1} out of {len(png_list)}; PNG file: {png_list[n]}'


def moveUp(event=None) -> None:
    """Move both focus and selection up, no change to list itself."""

    n = png_listbox.curselection()[0]
    if n > 0:
        png_listbox.select_clear(first=0, last=len(png_list) - 1)
        png_listbox.select_set(first=n - 1)
    showSelected()


def moveDown(event=None) -> None:
    """Move both focus and selection down, no change to list itself."""

    n = png_listbox.curselection()[0]
    if n < len(png_list) - 1:
        png_listbox.select_clear(first=0, last=len(png_list) - 1)
        png_listbox.select_set(first=n + 1)
    showSelected()


def makeUp(event=None) -> None:
    """Push selected item up the list by exchanging it with previous one."""

    n = png_listbox.curselection()[0]
    if n > 0:
        png_list[n], png_list[n - 1] = png_list[n - 1], png_list[n]
        png_list_str.set(png_list)  # Updating StringVar with new list
        png_listbox.select_clear(first=0, last=len(png_list) - 1)
        png_listbox.select_set(first=n - 1)
    showSelected()


def makeDown(event=None) -> None:
    """Push selected item down the list by exchanging it with next one."""

    n = png_listbox.curselection()[0]
    if n < len(png_list) - 1:
        png_list[n], png_list[n + 1] = png_list[n + 1], png_list[n]
        png_list_str.set(png_list)  # Updating StringVar with new list
        png_listbox.select_clear(first=0, last=len(png_list) - 1)
        png_listbox.select_set(first=n + 1)
    showSelected()


def makeInverse(event=None) -> None:
    """Reverse file list order at once."""

    png_list.reverse()
    png_list_str.set(png_list)  # Updating StringVar with new list
    showSelected()


def Sanctify(event=None) -> None:
    """Write ICO file."""

    # ↓ Open export file
    output_file = filedialog.asksaveasfilename(
        title='Save Windows ICO file',
        filetypes=[('Windows icon file', '.ico')],
        defaultextension='.ico',
    )
    if output_file == '':
        return None

    # ↓ Writing export file.
    #   Largely based on: https://github.com/emklasson/make-icon-from-pngs
    with open(output_file, 'wb') as icon_file:
        icon_file.write(b'\x00\x00')
        icon_file.write(b'\x01\x00')
        image_count = len(png_list)
        icon_file.write(image_count.to_bytes(2, byteorder='little'))
        image_directory_offset = 6
        image_directory_size = 16 * image_count
        icon_file.write(bytes(image_directory_size))
        png_data_offset = image_directory_offset + image_directory_size
        for png_listname in png_list:
            icon_file.seek(image_directory_offset)
            png = Png(png_listname)
            icon_file.write((png.width % 256).to_bytes(1, byteorder='little'))
            icon_file.write((png.height % 256).to_bytes(1, byteorder='little'))
            colors_in_palette = 0
            icon_file.write(colors_in_palette.to_bytes(1, byteorder='little'))
            icon_file.write(b'\x00')
            color_planes = 0
            icon_file.write(color_planes.to_bytes(2, byteorder='little'))
            bits_per_pixel = 0
            icon_file.write(bits_per_pixel.to_bytes(2, byteorder='little'))
            icon_file.write(png.file_size.to_bytes(4, byteorder='little'))
            icon_file.write(png_data_offset.to_bytes(4, byteorder='little'))
            icon_file.seek(png_data_offset)
            icon_file.write(png.file_data)
            png_data_offset += png.file_size
            image_directory_offset += 16
    zanyato['text'] = f'File {output_file} written'


class Png:
    """Loads a PNG file and extracts basic header and iDAT data.

    Taken from: https://github.com/emklasson/make-icon-from-pngs."""

    width = height = bit_depth = file_size = 0
    has_palette = False
    file_data = bytes(0)

    def __init__(self, filename):
        with open(filename, 'rb') as f:
            header = f.read(8)
            if header != b'\x89PNG\r\n\x1a\n':
                raise RuntimeError('Incorrect PNG header', filename, header)
            f.seek(4, 1)
            chunk_type = f.read(4)
            if chunk_type != b'IHDR':
                raise RuntimeError('Incorrect PNG chunk', filename, chunk_type)
            self.width = int.from_bytes(f.read(4), byteorder='big')
            self.height = int.from_bytes(f.read(4), byteorder='big')
            self.bit_depth = int.from_bytes(f.read(1), byteorder='big')
            color_type = int.from_bytes(f.read(1), byteorder='big')
            self.has_palette = color_type == 3
            f.seek(0)
            self.file_data = f.read()
            self.file_size = f.tell()


if __name__ == '__main__':  # Just to make python help(Sanctifier) work.
    # ↓ Dialog
    sortir = Tk()
    sortir.title('PNG Sanctifier')
    sortir.iconify()  # Not really needed, but I need sortir.deiconify() to get focus

    # ↓ Dummy initialize for starting, made to avoid more complex getList()
    png_list = ['', '']
    # ↓ List-based list-looking StringVar to be displayed in Listbox
    png_list_str = StringVar(value=png_list)

    # ↓ Listbox
    png_listbox = Listbox(
        sortir,
        selectmode='single',
        listvariable=png_list_str,
        font=('helvetica', 10),
        height=len(png_list) + 1,
        selectborderwidth=2,
    )
    png_listbox.grid(row=0, column=0, sticky='we')
    png_listbox.bind('<<ListboxSelect>>', showSelected)
    png_listbox.bind('<Up>', moveUp)
    png_listbox.bind('<Down>', moveDown)
    png_listbox.bind('<Control-Up>', makeUp)
    png_listbox.bind('<Control-Down>', makeDown)
    png_listbox.bind('<Control-i>', makeInverse)
    png_listbox.activate(0)
    png_listbox.select_set(first=0)

    # ↓ Currently selected file info
    zanyato = Label(
        sortir,
        text='Sanctify your PNGs - convert them to ICON!',
        font=png_listbox['font'],
        relief='sunken',
    )
    zanyato.grid(row=1, column=0, sticky='we')

    # ↓ UI hints
    hints = Label(
        sortir,
        text=' Ctrl+Up or Ctrl+Down to move item up or down; Ctrl+I to invert list; Enter to Export ICO; Ctrl+O to open new list; Ctrl+Q to quit ',
        font=('helvetica', 8),
        state='disabled',
    )
    hints.grid(row=2, column=0, sticky='we', pady=(4, 0))

    # ↓ Now getting actual "png_list" and "png_list_str"
    getList()

    sortir.deiconify()  # Without deiconify() it doesn't get focus

    sortir.bind_all('<Control-o>', getList)
    sortir.bind_all('<Control-O>', getList)
    sortir.bind_all('<Control-q>', DisMiss)
    sortir.bind_all('<Control-Q>', DisMiss)
    sortir.bind_all('<Control-w>', DisMiss)
    sortir.bind_all('<Control-W>', DisMiss)

    png_listbox.focus_set()

    sortir.update()
    # ↓ Setting 'sortir.maxsize' to fit 90% of screen
    sortir.maxsize(9 * sortir.winfo_screenwidth() // 10, 9 * sortir.winfo_screenheight() // 10)
    sortir.geometry(f'+{(sortir.winfo_screenwidth() - sortir.winfo_width()) // 2}+64')

    sortir.mainloop()
