import curses
from curses import *

class HelpPane:
	def __init__(self, stdscr):
		self.curr_help = {}
		self.stdscr = stdscr
		lines, cols = self.stdscr.getmaxyx()
		self.helppane = curses.newwin(2, cols, lines-2, 0)

	def render(self):
		lines, cols = self.stdscr.getmaxyx()
		key_txt = ""
		desc_txt = ""

		# Calculate the layout of the bottom text bar
		# First row is for the key
		# Seconds row is the the short desc. Can be truncated if needed 

		# max length of each item on the bar based on the longest element
		max_lengths = int(cols / len(self.curr_help))
		# divs = len(self.curr_help.keys())

		for key in self.curr_help.keys():
			desc = self.curr_help[key]

			# Truncate everything too large
			keyname_len = len(key)
			desc_len = len(desc)

			# Fill in the padding evenly
			keyname_pad = max_lengths - keyname_len
			desc_pad = max_lengths - desc_len

			key_left = int(keyname_pad / 2)
			desc_left = int(desc_pad / 2)

			key_right = keyname_pad - key_left
			desc_right = desc_pad - desc_left

			

			key_str = " " * key_left + key[:max_lengths] + " " * key_right
			desc_str = " " * desc_left + desc[:max_lengths] + " " * desc_right

			key_txt += key_str 
			desc_txt +=desc_str

		self.helppane.clear()
		self.helppane.addstr(0, 0, key_txt, curses.color_pair(1))
		self.helppane.addstr(1, 0, desc_txt, curses.color_pair(1))
		self.helppane.refresh()

	def set_help(self, key, help):
		self.curr_help[key] = help

	def clear_help(self):
		self.curr_help.clear()
