#
# wil create a dialog that will display the same help text file as the -h command
# argument
#
#    This file is part of kk-interface-fort
#
#    kk-interface-fort is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    kk-interface-fort is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with kk-interface-fort.  If not, see <http://www.gnu.org/licenses/>.

import sys
if sys.version[0][0] == '2':
	from Tkinter import *
	import Tkinter as tk
elif sys.version[0][0] == '3':
	from tkinter import *
	import tkinter as tk

class Help:
	def __init__(self,parent):
		frame = tk.Frame(parent, borderwidth = 3)

		# creation of tk widgets with some base properties
		help_textb = 	Text(frame, width=86, height = 35)
		help_scroll =	tk.Scrollbar(frame, orient=VERTICAL,
					command = help_textb.yview)
		exit_help =	tk.Button(frame, text = 'Exit Help',
					command = lambda:self.close(parent))
		help_textb['yscrollcommand'] = help_scroll.set
		help_textb.insert('1.0', open('HELP','r').read())
		help_textb['state'] = 'disabled'

		# widget grid command locations
		frame.grid	(column=0, row=0, sticky=(N,W,E,S))
		help_textb.grid	(column=1, row=1, sticky=(W))
		help_scroll.grid(column=2, row=1, sticky=(N,S))
		exit_help.grid	(column=1, row=2, columnspan=2, sticky=(N,W,E,S))

	def close(self,parent):
		parent.destroy()

