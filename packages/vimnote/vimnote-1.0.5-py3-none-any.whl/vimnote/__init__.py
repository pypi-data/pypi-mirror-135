#!/usr/bin/env python3.10

from .bookview import BookView
from .noteview import NoteView
from .tableview import TableView
from .config import get_config
from .exceptions import ExitException, OpenBookException, CloseBookException, EditNoteException

import sys
import os
import curses
import logging
import subprocess as sp

from typing import List, Any

CONFIG = get_config(os.path.expanduser('~/.config/vimnote'))

__help__ = '''vimnote - a vim-based TUI notetaking application
USAGE: vimnote              - launch into vimnote
       vimnote [book name]  - launch into vimnote and open a book immediately'''

class suspend_curses():
    # see https://stackoverflow.com/a/20769213/16834825 for justification/implementation
    def __enter__(self):
        curses.endwin()

    def __exit__(self, exc_type, exc_val, tb):
        newscr = curses.initscr()
        newscr.clear()
        newscr.refresh()
        curses.doupdate()

def real_main(stdscr, book):
    stdscr.clear()
    curses.curs_set(False)
    curses.use_default_colors()
    stdscr.refresh() # required for some reason, otherwise doesn't refresh until first keypress

    # logging.basicConfig(filename='log.log', level=logging.DEBUG)

    if book is None:
        view = BookView(stdscr, CONFIG)
    else:
        view = NoteView(stdscr, CONFIG, book)

    while True:
        view.draw()

        # break on keyboard interrupt
        try:
            key = stdscr.getch()
        except KeyboardInterrupt:
            break

        # if the terminal has been resized, clear stdscr and pad to avoid solitaire-ing
        if key == curses.KEY_RESIZE:
            stdscr.clear()
            view.pad.clear()
        stdscr.refresh()

        # else let the view handle it
        try: view.handle_keypress(key)
        except ExitException: break
        except OpenBookException as e:
            stdscr.clear()
            stdscr.refresh()
            view = NoteView(stdscr, CONFIG, e.title)
        except CloseBookException:
            stdscr.clear()
            stdscr.refresh()
            view = BookView(stdscr, CONFIG)
        except EditNoteException as e:
            with suspend_curses():
                sp.run(['vim', os.path.join(CONFIG['notedir'], e.book, e.title + '.vmnt')])
            view = NoteView(stdscr, CONFIG, e.book)

def main():
    os.environ['ESCDELAY'] = '25' # avoid long delay after hitting escape
    book = None
    if len(sys.argv) > 1:
        book = ' '.join(sys.argv[1:])
    if book in ('--help', '-h'):
        print(__help__)
    else:
        curses.wrapper(real_main, book)

if __name__ == '__main__':
    main()
