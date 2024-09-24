#!/usr/bin/env python3

'''
Reverting Latin-transliterated Russian to Russian Russian.
Note that dictionary based on real patterns rather than ISO 9!
Dictionaries are subject to change.

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "2024.09.24"
__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Production"

from tkinter import filedialog
from pathlib import Path

Tre = {
    'Gogol': 'Гоголь',
    'Tatyana': 'Татьяна',
    'Olga': 'Ольга',
    'Darya': 'Дарья',
    'Maria': 'Мария',
    'Group': 'Группа',
    'sch': 'щ',
    'shch': 'щ',
    'Sch': 'Щ',
    'Shch': 'Щ',
    'yay': 'яй',
}

Dvo = {
    'ya': 'я',
    'yo': 'ё',
    'yu': 'ю',
    'ay': 'ай',
    'ey': 'ей',
    'oy': 'ой',
    'iy': 'ий',
    'zh': 'ж',
    'ts': 'ц',
    'ch': 'ч',
    'sh': 'ш',
    'YA': 'Я',
    'YO': 'Ё',
    'YU': 'Ю',
    'ZH': 'Ж',
    'TS': 'Ц',
    'CH': 'Ч',
    'SH': 'Ш',
    'Ya': 'Я',
    'Yo': 'Ё',
    'Yu': 'Ю',
    'Zh': 'Ж',
    'Ts': 'Ц',
    'Ch': 'Ч',
    'Sh': 'Ш',
}

Rez = {
    'a': 'а',
    'b': 'б',
    'c': 'ц',
    'd': 'д',
    'e': 'е',
    'f': 'ф',
    'g': 'г',
    'h': 'х',
    'i': 'и',
    'j': 'й',
    'k': 'к',
    'l': 'л',
    'm': 'м',
    'n': 'н',
    'o': 'о',
    'p': 'п',
    'q': 'кв',
    'r': 'р',
    's': 'с',
    't': 'т',
    'u': 'у',
    'v': 'в',
    'w': 'в',
    'x': 'кс',
    'y': 'ы',
    'z': 'з',
    'A': 'А',
    'B': 'Б',
    'C': 'Ц',
    'D': 'Д',
    'E': 'Е',
    'F': 'Ф',
    'G': 'Г',
    'H': 'Х',
    'I': 'И',
    'J': 'Й',
    'K': 'К',
    'L': 'Л',
    'M': 'М',
    'N': 'Н',
    'O': 'О',
    'P': 'П',
    'Q': 'КВ',
    'R': 'Р',
    'S': 'С',
    'T': 'Т',
    'U': 'У',
    'V': 'В',
    'W': 'В',
    'X': 'КС',
    'Y': 'Ы',
    'Z': 'З',
}

# Open source dir
sourcedir = filedialog.askdirectory(title='Open folder with files to process')
if sourcedir == '':
    quit()

path = Path(sourcedir)

# Process file list
for filename in path.rglob('*.*'):  # select all files in all subfolders

    filename_parent = str((filename).parent)
    filename_str = str((filename).stem)
    fileext_str = str((filename).suffix)

    for was, will in Tre.items():
        filename_str = filename_str.replace(was, will)

    for was, will in Dvo.items():
        filename_str = filename_str.replace(was, will)

    for was, will in Rez.items():
        filename_str = filename_str.replace(was, will)

    filename_dot_ext = f'{filename_parent}/{filename_str}{fileext_str}'

    # print (filename_dot_ext)

    filename.rename(filename_dot_ext)  # rename it. Probably ".replace" is better
