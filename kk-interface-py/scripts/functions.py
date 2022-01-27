#
# script which contains all of the functions that are called on to perform
# the different necessary tasks in the program such as searching and opening a file
# getting the data from the data file
# or calling the fortran scripts to perform the numerical integration of the
# transform
# many were adapted and inspired by other programs from Dr. Jochen Autschbach
#
#    This file is part of kk-interface-python
#
#    kk-interface-python is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    kk-interface-python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with kk-interface-python.  If not, see <http://www.gnu.org/licenses/>.
#
import sys
from scripts import settings
if sys.version[0][0] == '3':
	from tkinter import *
	from tkinter import filedialog,messagebox
elif sys.version[0][0] == '2':
	from Tkinter import *
	import tkMessageBox as messagebox
	import tkFileDialog as filedialog

import numpy as np
import methods

def search_data(selected_data,exec_btn,lbl_open,check_space,plot_dat_btn,gskk_btn,data_log):
	# open search window
	filename = filedialog.askopenfilename(filetypes = (('omega files','.omega'),
						('lambda files','.lambda'),
						('txt files','.txt'),
						('all files','*')))
	if len(filename) > 0:
		# open file for reading
		fn = open(filename, 'r')
	
		# on the main interface window
		selected_data['state'] = 'normal'
		selected_data.delete('1.0', END)
		selected_data.insert('1.0', fn.read())
		selected_data['state'] = 'disabled'
		fn.close()

		openf = filename
		fnlist = filename.split('/')
		# in charge of displaying an abbreviated
		# file location so that the dimensions of
		# the main window are not changed
		j=-4
		a = '.../'
		i = 0
		for l in fnlist:
			if l == '':
				fnlist.remove(l)

		if len(fnlist) > 4:
			while i <= 3:
				if i == 3:
					a = a + fnlist[j]
				else:
					a = a + fnlist[j] + '/'
				i += 1
				j += 1
		else:
			a = openf

		lbl_open.set(a)
		
		# activates the execute button for execution
		exec_btn['state'] = 'normal'
		check_space['state'] = 'normal'
		plot_dat_btn['state'] = 'normal'
		gskk_btn['state'] = 'normal'

		settings.vardict['openf'] = openf
		settings.vardict['fnlist'] = fnlist[-1]
		print("Opened file "+openf)
		if data_log.get('1.0','1.2') != '>>':
			data_log['state'] = 'normal'
			data_log.delete('1.0',END)
			data_log['state'] = 'disabled'
	return

def spacing_check(points,data_log):
	space = np.zeros(len(points)-1)
	ave = 0
	for i in range(len(points)-1):
		space[i] = abs(points[i][0]-points[i+1][0])
		ave += space[i]
	ave = ave/len(space)
	max_s = max(space)
	min_s = min(space)
	text = '>>The average spacing for the input data file '+ \
		settings.vardict['openf']+' was ' \
		+str(ave)+' with a max value of '+str(max_s)+ \
		' and a min value of '+str(min_s)+'.\n'
	messagebox.showinfo(message='Input data spacing values:\n'+ \
			'Average - '+str(ave)+'\nMax - '+str(max_s)+ \
			'\nMin - '+str(min_s), title='Input data spacing')
	data_log['state'] = 'normal'
	data_log.insert('1.0',text)
	data_log['state'] = 'disabled'
	return

def open_file(op_type,data_log):
	fn = open(settings.vardict['openf'],'r')
	points = []
	for l in fn.readlines():
		l = l.strip()
		# ignore comments and blank lines
		if l != '' and l[0] != '#':
			d = l.split()
			points.append((float(d[0]),float(d[1])))
	fn.close()

	# put them in ascending order
	points.sort()
	
	# make sure we don't have duplicates
	toRemove = []
	for i in range(1, len(points)):
		if points[i][0] == points[i-1][0]:
			toRemove.append(points[i])

	for p in toRemove:
		points.remove(p)

	if op_type == 'space':
		spacing_check(points,data_log)
	return points

def main(data_log,method):
	points = open_file('','')
	
	filen = settings.vardict['fnlist']

	# text variable writes to the log that is kept
	# to make it easier to know what is being done
	if settings.vardict['wave'] == 'Yes':
		w_text = ' as a wave like variable'
		w = 1
	else:
		w_text = ' as a frequency like variable'
		w = 0
	length = int(len(points))

	# checks which transformation method to use
	# writes to a text box the method utilized and on which data set
	# it was applied
	if settings.vardict['real'] == 'Dispersive':
		if method == 'KK':
			f = methods.kk_mod.kkreversemaclaurin(w,points,length)
			text = '>>Reverse Kramers-Kronig transformation '+ \
				'perfomed on '+filen+w_text+' (taken from '+ \
				settings.vardict['openf']+')\n'
		elif method == 'MSKK':
			f = methods.mskk_mod.reversegskk(length, \
					int(settings.vardict['numanchor']), \
					w,points,settings.anchorpoints)
			text = '>>Reverse Kramers-Kronig transformation with '+ \
				'Multiply-Subtractive method '+ \
				'use of anchor'+' points performed on '+ \
				filen+w_text+' (taken from '+ \
				settings.vardict['openf']+')\n'
		elif method == 'CDKK':
			f = methods.cdkk_mod.reversecdkk(length, \
					int(settings.vardict['numanchor']), \
					w,points,settings.anchorpoints)
			text = '>>Reverse Kramers-Kronig transformation with '+ \
				'Chained-Doubly-Subctractive method '+ \
				'use of anchor points performed on '+ \
				filen+w_text+' (taken from '+ \
				settings.vardict['openf']+')\n'
	elif settings.vardict['real'] == 'Absorptive':
		if method == 'KK':
			f = methods.kk_mod.kkmaclaurin(w,points,length)
			text = '>>Kramers-Kronig transformation perfomed on '+ \
				filen+w_text+' (taken from '+ \
				settings.vardict['openf']+')\n'
		elif method == 'MSKK':
			f = methods.mskk_mod.gskk(length, \
				int(settings.vardict['numanchor']), \
				w,points,settings.anchorpoints)
			text = '>>Kramers-Kronig transformation with '+ \
				'Multiply-Subtractive method'+ \
				'use of anchor points performed on '+filen+w_text+ \
				' (taken from '+settings.vardict['openf']+')\n'
		elif method == 'CDKK':
			f = methods.cdkk_mod.cdkk(length, \
					int(settings.vardict['numanchor']), \
					w,points,settings.anchorpoints)
			text = '>>Kramers-Kronig transformation with '+ \
				'Chained-Doubly-Subctractive method '+ \
				'use of anchor points performed on '+ \
				filen+w_text+' (taken from '+ \
				settings.vardict['openf']+')\n'

	# writes method applied to log for reference
	data_log['state']='normal'
	data_log.insert('1.0',text)	
	data_log['state']='disabled'

	# used in offsetting the windows from one another
	i = 0
	while i < 5:
		if i == 4:
			for l in range(len(settings.position)):
				settings.position[l] = 0
		if settings.position[i] == 0:
			settings.position[i] = 1
			index = i
			break
		i += 1
	settings.vardict['index'] = str(index)

	freq = np.zeros(len(points))
	trans = np.zeros(len(points))
	orig = np.zeros(len(points))

	for i in range(len(points)):
		trans[i] = f[i][1]
		freq[i] = points[i][0]
		orig[i] = points[i][1]
	return freq,orig,trans,method

