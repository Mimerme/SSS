import curses
from curses.textpad import Textbox, rectangle
from curses import wrapper

def curses_text_input(stdscr, height=1, width=curses.COLS,start_x=1,start_y=1):
    # height = 5;
    # width = 30;
    # start_x = 1
    # start_y = 6
    margin = 1

    editwin = curses.newwin(height, width, start_y, start_x)
    box = Textbox(editwin)
    rectangle(stdscr, start_y - margin, start_x - margin, start_y + height, start_x + width)

    return box