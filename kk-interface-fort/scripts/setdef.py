#
# script responsible for creating and overwriting default settings
# will take what is on the dropdown menus on the main window and save
# them under the user given name
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
	from tkinter import messagebox
	import tkinter as tk
elif sys.version [0][0] =='2':
	from Tkinter import *
	import Tkinter as tk
	import tkMessageBox as messagebox
from scripts import settings
class SetDefault:
	def __init__(self,parent,default_name):
		def_name =	StringVar()
		frame =		tk.Frame(parent, borderwidth = 3)
		name_label =	tk.Label(frame,
					text = 'enter name for default setting')
		default =	tk.Entry(frame, textvariable = def_name)
		save_btn =	tk.Button(frame, text = 'Save Setting')
		save_btn['command'] = lambda:self.save \
					(default.get(),parent,default_name)
		frame.pack()
		name_label.pack()
		default.pack(fill = 'both', expand = True)
		save_btn.pack(fill = 'both', expand = True)
		default.focus()
	
	def save(self,name,parent,default_name):
		infile = open('.default_settings','r')
		all_list = infile.read().split(r'*')
		infile.close()
		overtext = name+',\nsetting already exists.'+ \
				'\nWish to overwrite it?'
		defover = 'Cannot overwrite Default Setting.'
		set_text = 'Will save the following settings for,\n'+name+ \
			'\nAbsorptive/Dispersive - '+settings.vardict['real']+ \
			'\nWavelength-like - '+settings.vardict['wave']+ \
			'\nX-axis label - '+settings.vardict['axis']+ \
			'\nX-axis units - '+settings.vardict['units']+ \
			'\nWish to save settings?'
		for i in range(0,len(all_list),2):
			if name == 'Default Setting':
				overwrite = messagebox.showwarning(title='Overwrite',
								message='defover')
				return
			elif name == all_list[i]:
				overwrite = messagebox.askyesno(title='Overwrite',
						message=overtext, icon='question')
				if overwrite == 0:
					return
				else:
					all_list[i+1] = settings.vardict['real']+ \
						r'%'+settings.vardict['wave']+r'%'+ \
						settings.vardict['axis']+r'%'+ \
						settings.vardict['units']
					for l in range(len(all_list)):
						if l == 0:
							new_list = all_list[l]
						else:
							new_list = new_list+r'*' \
								+all_list[l]
					break
			else:
				overwrite = 0
		dialog = messagebox.askyesno(title='Default Setting', icon='question',
							message=set_text)
		if dialog == 0:
			return
		else:
			if overwrite == 0:
				infile = open('.default_settings','a')
				infile.write(r'*'+name+r'*'+settings.vardict['real']+ \
					r'%'+settings.vardict['wave']+r'%'+ \
					settings.vardict['axis']+r'%'+ \
					settings.vardict['units'])
			else:
				infile = open('.default_settings','w')
				infile.write(new_list)
			infile.close()
			default_name.set(name)
			parent.destroy()
			
