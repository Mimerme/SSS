import pygame
import curses_file_browser
from curses_file_browser import FileBrowser

import curses
from curses import wrapper

import audiofile
import argparse
import glob
import os
import numpy as np
import pdb
import time

import logging
from sss_log import setup_log
setup_log()



parser = argparse.ArgumentParser(
    prog = 'SimpleSampleSorter',
    description = 'Manage/Sort Audio Samples and Supported Ableton Files',
    epilog = 'Copyright lolol')
parser.add_argument('-d', '--rootdir')
args = parser.parse_args()

cached_wavs = {}
UI_UPDDATE_RATE = 10

def main(stdscr):
    # Clear screen
    stdscr.clear()
    stdscr.addstr(0, 1, 'Initializing audio mixer (pygame)...')
    stdscr.refresh()

    stdscr.clear()
    stdscr.addstr(1, 1, 'Initializing logger...')
    stdscr.refresh()


    # Bootstrap process
    pygame.mixer.init(size=32)
    stdscr.addstr(2, 1, 'Discovering .wav files...')
    audiofiles = glob.glob("**/*.wav", root_dir=args.rootdir, recursive=True)
    stdscr.refresh()
    for file in audiofiles:
        signal, sampling_rate = audiofile.read(file)
        cached_wavs[file] = (signal, sampling_rate)
    stdscr.addstr(3, 1, '{} .wav files have been cached in memory. This totals to {} memory'.format(len(cached_wavs), 'n/a'))
    stdscr.addstr(4, 1, 'Made with love and hate </3')
    stdscr.refresh()
    logging.info("Finished Initialization. Sup")
    logging.info("Loaded {} *.wav files".format(len(cached_wavs)))
    time.sleep(0)
    time.sleep(1)

    # The meaty part
    # Draw the first frame and then handoff into the event loop
    filebrowser = FileBrowser(cached_wavs, stdscr)
    filebrowser.render()
    stdscr.refresh()

    # Render Loop Here <-------------------
    # currently just a browser with some vim-like features
    while True:
        filebrowser.input(stdscr.getkey())
        filebrowser.render()
        stdscr.refresh()


wrapper(main)

