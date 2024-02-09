#!/usr/bin/env python3

# Copyright (C) 2013-2018 Jean-Francois Romang (jromang@posteo.de)
#                         Shivkumar Shivaji ()
#                         Jürgen Précour (LocutusOfPenguin@posteo.de)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import configparser
from pathlib import Path


def write_book_ini():
    """Read the books folder and write the result to book.ini."""
    def is_book(fname):
        """Check for a valid book file name."""
        return fname.endswith('.bin')

    config = configparser.ConfigParser()
    config.optionxform = str

    program_path = Path().cwd()
    books_path = Path(f"{program_path}/books")
    books_ini_path = Path(f"{books_path}/books.ini")

    print("Generating books.ini file now ...")

    for book_file in books_path.glob("*.bin"):
        book_file_name = book_file.name
        print(f"-> Found book file with the name '{book_file.name}'")
        book = book_file_name[2:-4]
        config[book_file_name] = {}
        config[book_file_name]['small'] = book[:6]
        config[book_file_name]['medium'] = book[:8].title()
        config[book_file_name]['large'] = book[:11].title()

    with open(books_ini_path, "w") as configfile_object:
        config.write(configfile_object)
    print(f"{books_ini_path} has been written!")


write_book_ini()
