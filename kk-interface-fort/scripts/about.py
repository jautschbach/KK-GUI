#
# small class that will show a toplevel window giving the general information
# of the program and some other legal stuff
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
#
import sys
if sys.version[0][0] == '2':
	from Tkinter import *
	import Tkinter as tk
elif sys.version[0][0] == '3':
	from tkinter import *
	import tkinter as tk

class About:
	def __init__(self,parent):
		frame = tk.Frame(parent)
		
		# creation of tk widgets with some base properties
		textb = 	Text(frame, width = 86, height = 35)
		scroll=		tk.Scrollbar(frame, orient = VERTICAL,
					command=textb.yview)
		exit = 		tk.Button(frame,text = 'Exit',
					command = lambda:self.close(parent))

		textb['yscrollcommand'] = scroll.set
		textb.insert('1.0', open('ABOUT','r').read())
		textb['state'] = 'disabled'

		# widget grid command locations
		frame.grid	(column=0, row=0, sticky=(N,W,E,S))
		textb.grid	(column=1, row=1, sticky=(W))
		scroll.grid	(column=2, row=1, sticky=(N,S))
		exit.grid	(column=1, row=2, columnspan=2, sticky=(N,W,E,S))

	def close(self,parent):
		parent.destroy()

