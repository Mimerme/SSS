import curses
from curses import *
from select import select
from tkinter import W
from pywin32_testutil import str2bytes

import math
import pdb
import os

3# Curses Widgets
from curses_help_pane import HelpPane
from curses_text_input import TextInput

# For logging to file
import logging
from sss_log import setup_log
setup_log()

# For sound interfacing + processing
import numpy as np
import pygame

# For Live DLL IPC
import win32file
import win32

def init_mail():
    MAILSLOT = "\\\\.\\mailslot\\AYOLiveFileDropDest"
    file_handle = win32file.CreateFile(
        MAILSLOT, 
        win32file.GENERIC_WRITE,
        win32file.FILE_SHARE_READ,
        None,
        win32file.OPEN_EXISTING,
        win32file.FILE_ATTRIBUTE_NORMAL,
        0
    )
    return file_handle

def write_slot(hSlot, lpszMessage):
	WriteFile(hSlot,lpszMessage,(
		len(lpszMessage)+1))

class FileBrowser:
    def __init__(self, cache, stdscr):
        stdscr.move(0,0)
        self.lines, self.cols = stdscr.getmaxyx()

        # The cache is loaded by the main() function
        self.cache = cache
        self.idxs = list(self.cache.keys())

        # UI state variables go here
        self.selected = 1
        self.pg_start = 0
        self.stdscr = stdscr
        self.active_filters = []

        # Curses + UI initialization
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)


        logging.debug("Initialiing curses filebrowser")
        #logging.debug("console width: {}".format(cols))
        #logging.debug("browser width: {}".format(math.floor(cols*RATIO)))
        # logger.debug("browser : {}".format(math.floor(2*cols/RATIO)))

        SPLIT_RATIO = 2/3
        self.browser = curses.newwin(self.lines-1, math.floor(self.cols*SPLIT_RATIO), 0, 0)
        self.sidepane = curses.newwin(self.lines-1, math.floor(self.cols*(1.0-SPLIT_RATIO)), 0, math.floor(self.cols*SPLIT_RATIO))

        self.helppane = HelpPane(stdscr)
        self.helppane.set_help("/", "Name Search")
        self.helppane.set_help("A", "Tag")
        self.helppane.set_help("T", "Name Search")
        self.helppane.set_help("Y", "Clipboard/AHK")
        self.helppane.set_help("Space", "Play Audio")

        self.txtpane = TextInput(stdscr, 5, 20, 1, self.cols - 10)
        self.need_render = True


    def render(self):
        if not self.need_render:
            return

        # Render the browser window
        self.browser.clear()
        for l in range(self.browser.getmaxyx()[0]):
            idx = self.idxs[self.pg_start + l]
            idx = os.path.basename(idx)
            file_length = 0
            metaddata = 0

            if l == self.selected:    
                self.browser.addstr(l, 1, idx, curses.color_pair(1))
            else:
                self.browser.addstr(l, 1, idx, curses.color_pair(0))
        self.browser.refresh()

        # Render the tag window
        self.sidepane.clear()
        self.sidepane.addstr(0, 1, "FUCK OBAMA", curses.color_pair(0))
        self.sidepane.refresh()


        # Text Pane should always render on top of the help pane
        self.helppane.render()

        self.need_render = False


    def drop_into_live(self, path):
        if len(path) > 424:
            logging.error("Path Length Must Be Shorter Than 424")
            return

        win32file.WriteFile(file_handle, path);




    def action_play_audio(self, idx):
        buffer = np.sin(2 * np.pi * np.arange(44100) * 440 / 44100).astype(np.float32)
        sound = pygame.mixer.Sound(buffer)
        sound.play(0)
        pygame.time.wait(int(sound.get_length() * 1000))

    def action_show_metadata(self, idx):
        pass

    def action_add_tag(self, idx):
        pass

    def input(self, key_event):
        self.need_render = True

        if key_event == ('KEY_UP' or 'w'):
            self.selected -= 1
        elif key_event == ('KEY_DOWN' or 's'):
            self.selected += 1
        elif key_event == 'q':
            exit()
        elif key_event == "KEY_ENTER" or key_event == " ":
            self.action_play_audio(0)
        elif key_event == "/" :
            self.txtpane.input(title="Name Search")
        elif key_event == "a" :
            self.txtpane.input(title="Add Tag")
        elif key_event == "t" :
            self.txtpane.input("Tag Search")
        elif key_event == "y" :
            self.txtpane.input("Clipboard/AHK")

        logging.info(key_event)

class Filter:
    def filter_item(self, item, shared_state=None):
        pass
