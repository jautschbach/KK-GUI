#
# script responsible for the plotting of the data
# it has the capability of plotting the transform and original data on the 
# same figure
# from this window the transfromed data can also be saved
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
from scripts import settings
if sys.version[0][0] == '3':
    from tkinter import *
    from tkinter import messagebox,ttk,filedialog
    import tkinter as tk
elif sys.version[0][0] == '2':
    from Tkinter import *
    import Tkinter as tk
    import tkMessageBox as messagebox
    import ttk
    import tkFileDialog as filedialog
import matplotlib
matplotlib.use("Agg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator
import matplotlib.pyplot as plt
import numpy as np
import gc



class Plots:
    def __init__(self,parent,freq,orig,trans,method):
        self.parent = parent
        self.method = method
        self.freq = freq
        self.trans = trans
        self.orig = orig
        del freq
        del orig
        del trans
        self.container = tk.Frame(self.parent, borderwidth=3)
        self.container.pack(side=TOP, fill=BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        frame = Single_Plot(self.container,self)
        self.frames[Single_Plot] = frame
        frame.grid(row=0, column=0, sticky=(N,W,E,S))
        
        self.t_index = IntVar()
        self.t_index.set(int(settings.vardict['index']))
        lbl = tk.Label(frame, textvariable = self.t_index)
        self.show_frame(Single_Plot)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def close(self,parent,cont):
        close_text='Data for plot will be erased.\nWish to close window?'
        dialog = messagebox.askyesno(title='Close Data Plot',
                        icon='question',message=close_text)
        if dialog != 0:
            settings.position[int(self.t_index.get())] = 0
            self.a.clear()
            self.f.clf()
            del cont.freq
            del cont.trans
            del cont.orig
            parent.destroy()
            gc.collect()
        else:
            return

    # creates a textbox on the same window as the graph on the right column
    def trans_data(self,t_data):
        self.savelbl =  StringVar()
        self.text_disp =Text(self.container, width = 30, height = 24, state='normal')
        self.save_btn = tk.Button(self.container, textvariable=self.savelbl,
                        command=self.save_data)
        self.text_scroll =   tk.Scrollbar(self.container, orient=VERTICAL,
                        command=self.text_disp.yview)
        self.text_disp['yscrollcommand'] = self.text_scroll.set
        self.data_sep =     ttk.Separator(self.container, orient=VERTICAL)
        self.save_btn.grid      (column=1, row=4, sticky=(W,E))
        self.data_sep.grid      (column=4, row=1, rowspan=25, 
                            sticky=(N,S), padx=3)
        self.text_disp.grid (column=5, row=1, rowspan=25,sticky=(N,W,E,S))
        self.text_scroll.grid   (column=6, row=1, rowspan=25,sticky=(N,S))
        
        self.savelbl.set('Save Data')

        # writes the transformed data to the textbox on the window
        for i in range(len(self.freq)):
            self.text_disp.insert(str(i+1)+'.0', \
                str(self.freq[i])+'\t')
            if i == len(self.freq)-1:
                self.text_disp.insert(str(i+1)+'.15', \
                    str(self.trans[i]))
            else:
                self.text_disp.insert(str(i+1)+'.15', \
                    str(self.trans[i])+'\n')
        self.text_disp['state'] = 'disabled'
        t_data['text'] = 'Hide Transformed\nData'
        t_data['command'] = lambda:self.hide_trans(t_data)

    # destroys all of the widgets associated with the textbox for the 
    # transformed data  
    def hide_trans(self,t_data):
        self.text_disp.destroy()
        self.save_btn.destroy()
        self.text_scroll.destroy()
        self.data_sep.destroy()
        t_data['text'] = 'Show Transformed\nData'
        t_data['command'] = lambda:self.trans_data(t_data)

    # saves the transformed data
    def save_data (self):
        filename = filedialog.asksaveasfilename(filetypes = (('omega files'
                                    ,'.omega'),
                        ('lambda files','.lambda'),
                        ('txt files','.txt'),
                        ('all files','.*')))
        if len(filename) > 0:
            infile = open(filename, 'w')
            infile.write(self.text_disp.get('1.0',END))
            infile.close()
            self.savelbl.set('Data Saved')
        else:
            return

    # saves the graph
    # checks that the save file is a specific format for the savefig command
    # to be able to save the plot
    def save_graph(self,graph):
        filename = filedialog.asksaveasfilename(filetypes = (('eps','.eps'),
                        ('jpeg','.jpeg'),('jpg','.jpg'),
                        ('pdf','.pdf'),('pgf','.pgf'),
                        ('png','.png'),('ps','.ps'),
                        ('raw','.raw'),('rgba','.rgba'),
                        ('svg','.svg'),('svgz','.svgz'),
                        ('tif','.tif'),('tiff','.tiff')))
        matplotfile = ['eps','jpeg','jpg','pdf','pgf','png','ps','raw', \
                        'rgba','svg','svgz','tif','tiff']
        if len(filename) > 0:
            fileext = filename.split('.')
            for i in matplotfile:
                if fileext[1] == i:
                    break
                elif i == matplotfile[-1]:
                    fileformat=matplotfile[0]
                    for l in matplotfile[1:]:
                        fileformat=fileformat+', '+l
                    messagebox.showwarning(title='File format',
                    message='Unsupported file format for'+ \
                        ' graph. Please use one of '+ \
                        'following formats:\n'+ \
                                fileformat)
                    return
            graph.savefig(filename)
        else:
            return

class Single_Plot(tk.Frame,Plots):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.t_index = StringVar()
        self.t_index.set(settings.vardict['index'])
        self.f = Figure(figsize = (9.75,5), dpi = 75)
        self.a = self.f.add_subplot(111)
        f = self.f
        a = self.a

        if settings.vardict['real'] == 'Dispersive':
            funct = 'Reverse '+controller.method+' transform'
            a.plot(controller.freq,controller.orig,'-r',label='Disp.')
            a.plot(controller.freq,controller.trans,'-b',label='Abs.')
        else:
            funct = controller.method+' transform'
            a.plot(controller.freq,controller.trans,'-r',label='Disp.')
            a.plot(controller.freq,controller.orig,'-b',label='Abs.')
        if controller.method != 'KK':
            mskk_text = ' with '+settings.vardict['numanchor']+ \
                                ' anchor points'
            ancfreq = []
            ancval = []
            for i in settings.anchorpoints:
                ancfreq.append(i[0])
                ancval.append(i[2])
            a.plot(ancfreq,ancval,'^k',label='Anchors')
        else:
            mskk_text = ''
        if settings.vardict['axis'] == ''  \
                    and settings.vardict['units'] == '':
            a.set_xlabel('')
        elif settings.vardict['axis'] != ''  \
                    and settings.vardict['units'] == '':
            a.set_xlabel('$'+settings.vardict['axis']+'$')
        elif settings.vardict['axis'] == ''  \
                    and settings.vardict['units'] != '':
            a.set_xlabel('$'+settings.vardict['units']+'$')
        else:
            a.set_xlabel('$'+settings.vardict['axis']+'$'+ \
                    ' ($'+settings.vardict['units']+'$)')
        a.set_title('Dispersion and Absorption functions for ' + \
                settings.vardict['fnlist']+'\nusing '+ \
                            funct + mskk_text)
        a.legend(loc = 'upper right')
        minorLocator = AutoMinorLocator(5)
        a.xaxis.set_minor_locator(minorLocator)
        a.grid(b=TRUE, which='major', axis='x', color='k',
            linestyle='-', linewidth=1)
        a.grid(b=TRUE, which='minor', axis='x', color='k',
            linestyle='--', linewidth=0.5)

        # checks to see if it is necessary to change the y-axis to
        # scientific notation
        if max(controller.orig) >= 1000 or max(controller.trans) >= 1000:
            a.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
        f.set_tight_layout(True)

        # linking the matplotlib graph to the tk canvas to be shown
        # on the window
        canvas = FigureCanvasTkAgg(f, parent)
        canvas.show()
        canvas.get_tk_widget().grid (column=3,row=1,rowspan=25,
                                sticky=(N,W,E,S))
        canvas._tkcanvas.grid       (column=3,row=1,rowspan=25,
                                sticky=(N,W,E,S))
        self.grid_columnconfigure(3, weight = 1)
        for i in range(25):
            self.grid_rowconfigure(i+1, weight = 1)


        lbl = tk.Label(parent, textvariable = self.t_index)
        t_data = tk.Button(parent, text = 'Show Transformed\nData',
                command=lambda:controller.trans_data(t_data))
        savegraph = tk.Button(parent,text='Save graph',
                    command=lambda:self.save_graph(f))
        sep = ttk.Separator(parent, orient=VERTICAL)
        
        t_data.grid(column=1,row=1,sticky=(W,E))
        savegraph.grid  (column=1,row=2,sticky=(W,E))
        sep.grid    (column=2,row=1,rowspan=25,sticky=(N,S),padx=3)
        controller.parent.protocol('WM_DELETE_WINDOW',
                lambda:self.close(controller.parent,controller))

# kept out to decrease memory usage
#class Double_Plot(tk.Frame,Plots):
#   def __init__(self, parent, controller):
#       tk.Frame.__init__(self, parent)
#
#       # keeps track of which data goes with which graph
#       self.t_index = StringVar()
#       self.t_index.set(settings.vardict['index'])
#
#       # initializing matplotlib plot to be linked
#       # to a tk canvas
#       #f = Figure(figsize = (9.75,5.5), dpi = 75)
#       global c
#       global b
#       c.clear
#       b.clear
#       c = v.add_subplot(2, 1, 1)
#       b = v.add_subplot(2, 1, 2)
#
#       # creates arrays that will be 1 dimensional reading from
#       # the storing array indexed column
#       #freq_i = np.zeros(len(freq))
#       #trans_i = np.zeros(len(freq))
#       #orig_i = np.zeros(len(freq))
#       #for i in range(len(freq)):
#       #   freq_i[i] = freq[i]
#       #   trans_i[i] = trans[i]
#       #   orig_i[i] = orig[i]
#
#       # plotting of data where orig is the original file data,
#       # trans is the transformed data and freq is the frequency.
#       # created as a vertical subplot
#
#       # checks the transformation used to apply the correct data
#       # to the graph on each line
#       if controller.method != 'KK':
#           mskk_text = '\nwith '+settings.vardict['numanchor']+ \
#                               ' anchor points'
#           ancfreq = []
#           ancval = []
#           for i in settings.anchorpoints:
#               ancfreq.append(i[0])
#               ancval.append(i[2])
#       else:
#           mskk_text = ''          
#       if settings.vardict['real'] == 'Dispersive':
#           c.plot(controller.freq,controller.orig,'-r')
#           b.plot(controller.freq,controller.trans,'-b')
#           if controller.method != 'KK':
#               b.plot(ancfreq,ancval,'^k',label='Anchors')
#               b.legend(loc='upper right')
#       else:
#           c.plot(controller.freq,controller.trans,'-r')
#           b.plot(controller.freq,controller.orig,'-b')
#           if controller.method != 'KK':
#               c.plot(ancfreq,ancval,'^k',label='Anchors')
#               c.legend(loc='upper right')
#       b.set_title('Absorption')
#       c.set_title('Dispersion of '+settings.vardict['fnlist']+mskk_text)
#
#       # matplotlib configuration options
#       minorLocator = AutoMinorLocator(5)
#       if settings.vardict['axis'] == '' and \
#                   settings.vardict['units'] == '':
#           c.set_xlabel('')
#           b.set_xlabel('')
#       elif settings.vardict['axis'] != '' and \
#                   settings.vardict['units'] == '':
#           c.set_xlabel('$'+settings.vardict['axis']+'$')
#           b.set_xlabel('$'+settings.vardict['axis']+'$')
#       elif settings.vardict['axis'] == '' and \
#                   settings.vardict['units'] != '':
#           c.set_xlabel('$'+settings.vardict['units']+'$')
#           b.set_xlabel('$'+settings.vardict['units']+'$')
#       else:
#           c.set_xlabel('$'+settings.vardict['axis']+'$'+ \
#                   ' ($'+settings.vardict['units']+'$)')
#           b.set_xlabel('$'+settings.vardict['axis']+'$'+ \
#                   ' ($'+settings.vardict['units']+'$)')
#
#       c.xaxis.set_minor_locator(minorLocator)
#       b.xaxis.set_minor_locator(minorLocator)
#       c.grid(b=TRUE, which='major', axis='x', color='k',
#           linestyle='-', linewidth=1)
#       c.grid(b=TRUE, which='minor', axis='x', color='k',
#           linestyle='--',linewidth=0.5)
#       b.grid(b=TRUE, which='minor', axis='x', color='k',
#           linestyle='--',linewidth=0.5)
#       b.grid(b=TRUE, which='major', axis='x', color='k',
#           linestyle='-', linewidth=1)
#
#       # checks to see if it is necessary to change the y-axis to
#       # scientific notation
#       if max(controller.orig) >= 1000 or max(controller.trans) >= 1000:
#           c.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
#           b.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
#       v.set_tight_layout(True)
#       v.subplots_adjust(hspace = 0.5)
#
#       # linking the matplotlib graph to the tk canvas to be shown
#       # on the window
#       canvas = FigureCanvasTkAgg(v, parent)
#       canvas.show()
#       canvas.get_tk_widget().grid (column=3,row=1,rowspan=25,
#                               sticky=(N,W,E,S))
#       canvas._tkcanvas.grid       (column=3,row=1,rowspan=25,
#                               sticky=(N,W,E,S))
#       self.grid_columnconfigure(3, weight = 1)
#       for i in range(25):
#           self.grid_rowconfigure(i+1, weight = 1)
#
#       # button for easy navigation of plots and initializing
#       # trans_data subroutine
#       btn = tk.Button(parent, text = 'Single Plot')
#       btn['command']=lambda:controller.show_frame(Single_Plot)
#       lbl = tk.Label(parent, textvariable = self.t_index)
#       t_data = tk.Button(parent, text = 'Show Transformed\nData',
#               command=lambda:controller.trans_data(t_data))
#       savegraph = tk.Button(parent,text='Save graph',
#                   command=lambda:self.save_graph(v))
#       sep = ttk.Separator(parent, orient=VERTICAL)
#       
#       btn.grid    (column=1,row=1,sticky=(W,E))
#       t_data.grid(column=1,row=2,sticky=(W,E))
#       savegraph.grid  (column=1,row=3,sticky=(W,E))
#       sep.grid    (column=2,row=1,rowspan=25,sticky=(N,S),padx=3)
#
