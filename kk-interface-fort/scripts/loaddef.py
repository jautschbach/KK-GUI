#
# script responsible for switching between different user default settings
# which are save in the .default_settings file
# will create a small dialog window with a dropdown menu that can be used
# to select diferent default settings
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
if sys.version[0][0] == '3':
	from tkinter import *
	from tkinter import ttk,messagebox
	import tkinter as tk
elif sys.version[0][0] == '2':
	from Tkinter import *
	import Tkinter as tk
	import tkMessageBox as messagebox
	import ttk
from scripts import settings
class LoadDefault:
	def __init__(self,parent,default_name,real,wave,axis,units):
		self.name_load =StringVar()
		frame =		tk.Frame(parent, borderwidth=3)
		name_label =	tk.Label(frame,
					text = 'Select defualt setting to use'+
						'\nfrom dropdown menu')
		load_name =	ttk.Combobox(frame, textvariable = self.name_load)
		load_btn =	tk.Button(frame, text = 'Load settings')
		load_btn['command'] = lambda:self.load(parent,default_name, \
						real,wave,axis,units)
		self.name_load.set('Default Setting')
		infile = open('.default_settings','r')
		all_list = infile.read().split(r'*')
		infile.close()
		self.defsettings = {}
		for i in range(0,len(all_list),2):
			self.defsettings[all_list[i]] = all_list[i+1]
		load_name['values'] = list(self.defsettings.keys())
		frame.pack()
		name_label.pack()
		load_name.pack(fill = 'both', expand = True)
		load_btn.pack(fill = 'both', expand = True)

	def load(self,parent,default_name,real,wave,axis,units):
		dial_text = 'Load default settings of,\n'+self.name_load.get()
		dialog = messagebox.askyesno(title='Load Settings', icon='question',
							message=dial_text)
		if dialog == 0:
			return
		else:
			def_list = self.defsettings[self.name_load.get()].split(r'%')
			settings.vardict['real'] = (def_list[0])
			settings.vardict['wave'] = (def_list[1])
			settings.vardict['axis'] = (def_list[2])
			settings.vardict['units']= (def_list[3])
			default_name.set(self.name_load.get())
			real.set(def_list[0])
			wave.set(def_list[1])
			axis.set(def_list[2])
			units.set(def_list[3])
		parent.destroy()

