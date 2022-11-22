import curses
from curses import *

import logging
from sss_log import setup_log
setup_log()
from curses.textpad import Textbox, rectangle
# https://epydoc.sourceforge.net/stdlib/curses.textpad.Textbox-class.html

class TextInput:
	def __init__(self, stdscr, start_x,start_y,height,width,margin=1):
		self.dims = {
			"start_x":start_x,
			"start_y":start_y,
			"height":height,
			"width":width,
			"margin":margin
		}

		self.top_txt = ""
		self.bottom_txt = "Bottom Text"
		self.stdscr = stdscr
		lines, cols = self.stdscr.getmaxyx()
		self.txtpane = curses.newwin(height, width, start_y, start_x)
		self.inpane = curses.newwin(height, width, start_y + 2, start_x)

		self.box = Textbox(self.inpane)

	def input(self, title="Placeholder"):
		rectangle(self.stdscr, self.dims["start_y"] - self.dims["margin"] + 2, self.dims["start_x"] - self.dims["margin"], self.dims["start_y"] + 2 + self.dims["height"], self.dims["start_x"] + self.dims["width"])
		self.stdscr.refresh()

		self.inpane.clear()
		self.inpane.refresh()

		self.txtpane.clear()
		self.txtpane.addstr(0,0, title, curses.color_pair(1))
		self.txtpane.refresh()

		self.box.edit()

		self.txtpane.move(0,0)
		self.inpane.move(0,0)
		self.stdscr.move(0,0)

# def show(self, callback=None):
	# 	if self.is_vis:
	# 		return
	#
	# 	self.is_vis = True
	# 	self.pending_callback = callback
	# 	self.need_render = True
	# 	self.box.edit()
	#
	# def hide(self):
	# 	self.is_vis = False
	# 	self.pending_callback = None
	# 	self.top_txt = ""
	#
	#
	# def set_bottom(self, txt):
	# 	self.bottom_txt = txt
	#
	# def render(self):
	# 	if not self.is_vis:
	# 		return
	#
	# 	if not self.need_render:
	# 		return
	#
	# 	logging.debug(self.dims)
	# 	rectangle(self.stdscr, self.dims["start_y"] - self.dims["margin"], self.dims["start_x"] - self.dims["margin"], self.dims["start_y"] + self.dims["height"], self.dims["start_x"] + self.dims["width"])
	#
	# 	# self.txtpane.clear()
	# 	# self.txtpane.addstr(0, 0, self.top_txt, curses.color_pair(1))
	# 	# self.txtpane.addstr(1, 0, self.bottom_txt, curses.color_pair(1))
	# 	# self.txtpane.refresh()
	#
	# def input(self, key_event):
	# 	logging.debug(key_event.isprintable())
	# 	self.need_render = True
	# 	if key_event.isprintable():
	# 		self.top_txt += key_event
	# 	# Escape ASCII
	# 	elif ord(key_event) == 27:
	# 		self.hide()
	# 	# Carriage Return
	# 	elif ord(key_event) == 13:
	# 		self.pending_callback(self.top_txt)
	#
	# def set_help(self, key, help):
	# 	self.curr_help[key] = help
	#
	# def clear_help(self):
	# 	self.curr_help.clear()
