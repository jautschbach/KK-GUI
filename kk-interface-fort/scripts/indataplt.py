#
# will graph the data file that has been initially selected for the user to be able
# to visually see the data that has been selected
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
	import tkinter as tk
elif sys.version[0][0] == '2':
	from Tkinter import *
	import Tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
						NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator
import numpy as np

class InputDataPlot:
	def __init__(self,parent,points):
		frame = tk.Frame(parent)
		frame.pack()
		f = Figure(figsize = (9.75,5), dpi = 75)
		a = f.add_subplot(111)
		p_len = len(points)
		x = np.zeros(len(points))
		y = np.zeros(len(points))
		for i in range(p_len):
			x[i] = points[i][0]
			y[i] = points[i][1]
		a.plot(x,y,'-r')
		a.set_title('Input data plot')
		minorLocator = AutoMinorLocator(5)
		a.xaxis.set_minor_locator(minorLocator)
		a.grid(b=TRUE, which='major', axis='x', color='k',
			linestyle='-', linewidth=1)
		a.grid(b=TRUE, which='minor', axis='x', color='k',
			linestyle='--', linewidth=1)
		f.set_tight_layout(True)

		canvas = FigureCanvasTkAgg(f, frame)
		canvas.show()
		canvas.get_tk_widget().pack(side=tk.TOP,
			fill=tk.BOTH, expand=True)
		toolbar = NavigationToolbar2TkAgg(canvas, frame)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

