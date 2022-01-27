#
# this script is used to set the anchorpoint values that will be used in the
# MSKK or CDKK methods that can be switched and used independently
# these can be switched by use of a button on the GUI that is created from this script
# which will in turn change the text on the main GUI to the respective value
# when the button on the main GUI is activated it will execute the respective
# transformation method
# can also calculate the chebyshev zero-nodes and adjust them for the data that is
# loaded on the main GUI
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
    import tkFileDialog as filedialog
    import ttk
    import tkMessageBox as messagebox
elif sys.version[0][0] == '3':
    from tkinter import *
    from tkinter import filedialog,ttk,messagebox
    import tkinter as tk
import numpy as np
import math as mt
from scripts import settings,functions
from fortran_scripts import methods
class GSKK:
    def __init__(self,parent,mskk_btn,mskkcdkk):
        self.vardict = settings.vardict
        self.mskk_btn = mskk_btn
        self.mskkcdkk = mskkcdkk
        self.savelbl = StringVar()
        self.num =   IntVar()
        self.switch_name = StringVar()
        self.exc_name = StringVar()
        anlbltext = 'Enter number of anchor points.'
        self.frame =    tk.Frame(parent, borderwidth=3)
        anlbl =     tk.Label(self.frame, text = anlbltext)
        annum =     tk.Entry(self.frame,textvariable = self.num, width = 3)
        mkgrid =    tk.Button(self.frame, text = 'Make Grid')
        mkgrid['command'] =     lambda:self.makegrid(True,0)
        open_data =     tk.Button(self.frame, text = 'Open anchor file')
        open_data['command'] =  self.open_anchor_file
        self.save_btn = tk.Button(self.frame, state = 'disabled',
                        textvariable = self.savelbl)
        cheby_btn = tk.Button(self.frame, text = 'Find Chebyshev zero-nodes',
                        command = lambda:self.cheby(parent))
        self.switch_btn=tk.Button(self.frame, state = 'disabled', 
                    textvariable = self.switch_name)
        self.frame.grid(column = 0, row = 0, sticky = (N,W,E,S))
        anlbl.grid(column = 1, row = 1, sticky = (W))
        annum.grid(column = 2, row = 1, sticky = (W,E))
        mkgrid.grid(column = 1, row = 2, columnspan = 2, sticky = (W,E))
        open_data.grid(column = 1, row = 3, columnspan = 2, sticky = (W,E))
        self.save_btn.grid(column = 1, row = 5, columnspan = 2, sticky = (W,E))
        cheby_btn.grid(column = 1, row = 4, columnspan = 2, sticky = (W,E))
        self.switch_btn.grid(column=1, row=6, columnspan=2, sticky=(W,E))
        annum.focus()
        # widgets that will be used later
        self.anc_entry = []
        self.fomega_entry = []
        self.btn = []

    # creates grid that can be used to fill in the anchorpoints manually
    # if an file with the anchorpoints is opened then it will fill in those
    # values in the file by default
    def makegrid(self,new,anchors):
        if len(self.anc_entry) > 0:
            for i in range(len(self.anc_entry)):
                self.anc_entry[i].destroy()
                self.fomega_entry[i].destroy()
        if len(self.btn) > 0:           # will destroy the extra buttons that
            for i in range(len(self.btn)):  # are created to fill the extra space
                self.btn[i].destroy()
        self.vardict['numanchor'] = str(self.num.get())
        self.anc_entry = []
        self.fomega_entry = []
        anc_var = []
        fomega_var = []
        # creates blank buttons for even spacing of grid
        # nothing happens when pressed
        if self.num.get() > 6:
            for i in range(self.num.get() - 5):
                if len(self.btn) < (self.num.get() - 5):
                    for j in range((self.num.get()-5)- \
                                len(self.btn)):
                        self.btn.append('')
                self.btn[i] = tk.Button(self.frame,state='disabled')
                self.btn[i].grid(column = 1, row = i+7, columnspan = 2,
                        sticky = (W,E))
        # to create an arbitrary grid a list is written with all the
        # widgets to be used and their respective properties
        for i in range(self.num.get()):
            self.anc_entry.append('')
            self.fomega_entry.append('')
            anc_var.append('')
            fomega_var.append('')
            self.anc_entry[i]= tk.Entry(self.frame,
                            textvariable = anc_var[i])
            self.fomega_entry[i] =  tk.Entry(self.frame,
                            textvariable = fomega_var[i])
            self.anc_entry[i].grid     (column = 3, row = i+2,
                            sticky = (N,W,E,S))
            self.fomega_entry[i].grid       (column = 4, row = i+2,
                            sticky = (N,W,E,S))
            # responsible for writing inputted anchor values to the
            # grid for use in transform
            if new:
                self.columns = 2
            else:
                self.anc_entry[i].insert(END, anchors[i][0])
                self.fomega_entry[i].insert(END, anchors[i][1])

        self.savelbl.set('Use anchor points')
        self.save_btn['command'] = self.savepoints
        self.save_btn['state'] = 'normal'
        weven_lbl =     tk.Label(self.frame, text = 'Omega/Wave anchor')
        fomega_lbl =    tk.Label(self.frame, text = 'Anchor Value')
        weven_lbl.grid(column = 3, row = 1, sticky = (W,E))
        fomega_lbl.grid(column = 4, row = 1, sticky = (W,E))

    # simple function to open the file with the anchorpoints
    # will count the number of columns that there are in the data file
    # if there are three an extra array is created to be able to hold it in memory
    # and later accessed rather than calculating a new column with datfit.py
    def open_anchor_file(self):
        anchorfile = []
        self.other_column = []      # takes the extra column if there are three
        filename = filedialog.askopenfilename()
        if len(filename) > 0:
            fn = open(filename,'r')
            for i in fn.readlines():
                i = i.strip()
                d = i.split()
                if len(d) == 3:
                    anchorfile.append((d[0],d[2]))
                    self.other_column.append(d[1])
                    self.columns = 3
                elif len(d) == 2:
                    anchorfile.append((d[0],d[1]))
                    self.columns = 2
                else:
                    warntext = 'Make sure the file selected\n'+ \
                        'has two or three columns to be \n'+ \
                        'written to the table correctly.'
                    messagebox.showwarning(message = warntext,
                        title = 'Check number of columns')
                    return
            self.num.set(len(anchorfile))
            self.makegrid(False,anchorfile)
            self.savelbl.set('Use anchor points')
        else:
            return

    # will write the data on the grid entry boxes to a global variable set on
    # settings.py script to be used in other places of the program more simply
    # will also activate some buttons that will be used to distinguish
    # between the MSKK and CDKK methods
    def savepoints(self):
        points = functions.open_file('','')
        freq = np.zeros(len(points))
        for i in range(len(points)):
            freq[i] = points[i][0]
        zerolist = np.zeros(self.num.get())
        for i in range(self.num.get()):
            zerolist[i] = float(self.anc_entry[i].get())
        fittedanchors = np.zeros((self.num.get(),3))

        # checks for the number of columns that exist
        # will only be three if a data file with three columns is opened
        # if it is not then the datfit.py script will fit the freq/wave column to
        # the data that has been given on the main GUI screen
        f = methods.fit_data.fit(len(points),self.num.get(),freq,zerolist)
        fitData = []
        if self.columns != 3:
            for i in range(len(f)):
                fittedanchors[i][:] = [f[i][0],f[i][1], \
                            self.fomega_entry[i].get()]
        else:
            for i in range(len(f)):
                if zerolist[i] - f[i][0] >= 1e-6:
                    fitData.append(True)
                else:
                    fitData.append(False)
            for val in range(len(fitData)):
                if fitData[val]:
                    text = "The selected file has not\n"+ \
                            "been fitted to data.\n"+ \
                            "Wish to do so now?"
                    ask = messagebox.askyesno(title='Fitted data',
                                        icon='question',message=text)
                    if ask != 0:                        
                        for i in range(len(f)):
                            fittedanchors[i][:] = [f[i][0],f[i][1], \
                                        self.fomega_entry[i].get()]
                    else:
                        for i in range(len(self.other_column)):
                            fittedanchors[i][:] = [zerolist[i], \
                                        self.other_column[i], \
                                        self.fomega_entry[i].get()]
                    break
        for i in range(1,len(fittedanchors)):
            for j in range(len(fittedanchors)-i):
                temp = []
                for val in fittedanchors[j]:
                    temp.append(val)
                if fittedanchors[j][1] < fittedanchors[j+1][1]:
                    continue
                else:
                    fittedanchors[j][:] = fittedanchors[j+1][:]
                    fittedanchors[j+1][:] = temp

        self.mskk_btn['state'] = 'normal'
        self.mskkcdkk.set('Execute\nMSKK')
        self.switch_name.set('Use CDKK')
        self.switch_btn['state'] = 'normal'
        self.switch_btn['command'] = self.switch
        settings.anchorpoints = fittedanchors
        settings.vardict['method'] = 'MSKK'
        self.savelbl.set('Using current anchors')

    # script to create window to be able to calculate the chebyshev zero-nodes
    # with the given data loaded on the main GUI
    # could implement script to find the transformation values to give
    # the complete anchor points values
    def cheby(self,parent):
        win = tk.Toplevel(parent)
        x = parent.winfo_rootx() + parent.winfo_width() + 3
        y = parent.winfo_rooty() - 28
        win.geometry('+'+str(x)+'+'+str(y))
        self.wmin = DoubleVar()
        self.wmax = DoubleVar()
        self.ancnum = IntVar()

        self.cframe = tk.Frame(win, borderwidth = 3)
        lbl1 = tk.Label(self.cframe, text = u'\u03c9'+' Min')
        lbl2 = tk.Label(self.cframe, text = u'\u03c9'+' Max')
        lbl3 = tk.Label(self.cframe, text = 'Number of\nanchor points')
        entry1 = tk.Entry(self.cframe, textvariable = self.wmin, width = 10)
        entry2 = tk.Entry(self.cframe, textvariable = self.wmax, width = 10)
        entry3 = tk.Entry(self.cframe, textvariable = self.ancnum, width = 10)
        btn1 = tk.Button(self.cframe, text = 'Find zero-nodes',
            command = self.findanchors)

        self.cframe.grid(column = 0, row = 0, sticky = (N,S,W,E))
        lbl1.grid   (column = 1, row = 1, sticky = (N,W,E,S))
        lbl2.grid   (column = 2, row = 1, sticky = (N,S,W,E))
        lbl3.grid   (column = 3, row = 1, columnspan = 2, sticky = (N,W,E,S))
        entry1.grid (column = 1, row = 2, sticky = (W))
        entry2.grid (column = 2, row = 2, sticky = (W))
        entry3.grid (column = 3, row = 2, columnspan = 2, sticky = (W))
        btn1.grid   (column = 1, row = 3, columnspan = 4, sticky = (N,W,E,S))

        entry1.focus()

    # executes script to find chebyshev zero-nodes
    def findanchors(self):
        points = functions.open_file('','')
        freq = np.zeros(len(points))
        for i in range(len(points)):
            freq[i] = points[i][0]
        zerolist = np.zeros(self.ancnum.get())
        xmax = self.wmax.get()
        xmin = self.wmin.get()
        n = self.ancnum.get()
        for i in range(n):
            zerolist[i] = mt.sqrt(((xmax*xmax - xmin*xmin) * \
                mt.cos((2*i*mt.pi+mt.pi)/(2*n)) + (xmax*xmax + xmin*xmin))/2.0)
        sep =       ttk.Separator(self.cframe,orient=HORIZONTAL)
        sep_lbl =   tk.Label(self.cframe,text='Chebyschev anchor points')
        

        text =      Text(self.cframe,width=10,height=5)
        text_scroll =   tk.Scrollbar(self.cframe,orient=VERTICAL,
                    command=text.yview)
        use_btn =   tk.Button(self.cframe,text='Use for\ntransform',
                    command=lambda:self.use(zerolist))
        savecheby = tk.Button(self.cframe,text='Save\npoints',
                    command=lambda:self.savechebypoints(text))
        f_text = ''
        for i in zerolist:
            f_text = f_text+str(i)+'\n'
        text['yscrollcommand'] = text_scroll.set
        text['state'] = 'normal'
        text.delete('1.0',END)
        text.insert('1.0',f_text)
        text['state'] = 'disabled'
        sep.grid    (column=1,row=4,columnspan=5,sticky=(W,E),pady=5)
        sep_lbl.grid    (column=1,row=5,columnspan=2,sticky=(W))
        text.grid   (column=1,row=6,columnspan=2,rowspan=2,sticky=(N,W,E,S))
        text_scroll.grid(column=3,row=6,rowspan=2,sticky=(N,S,W))
        use_btn.grid    (column=4,row=6,sticky=(N,W,E,S))
        savecheby.grid  (column=4,row=7,sticky=(N,W,E,S))
    
    # writes calculated chebyshev zero-nodes to the grid so that
    # they can be used in the transformation
    def use(self,f):
        anchors = np.zeros((len(f),2))
        for i in range(len(f)):
            anchors[i][0] = f[i]
        self.columns = 2
        self.num.set(len(f))
        self.makegrid(False,anchors)

    # saves calculated chebyshev zero-nodes to a file
    def savechebypoints(self,text):
        filename = filedialog.asksaveasfilename()
        if len(filename) > 0:
            fn = open(filename,'w')
            fn.write(text.get("1.0",END))
            fn.close()
        else:
            return
    
    # script that will change the method from MSKK to CDKK or vice-versa
    def switch(self):
        if settings.vardict['method'] == 'MSKK':
            self.switch_name.set('Use MSKK')
            self.mskkcdkk.set('Execute\nCDKK')
            settings.vardict['method'] = 'CDKK'
        else:
            self.switch_name.set('Use CDKK')
            self.mskkcdkk.set('Execute\nMSKK')
            settings.vardict['method'] = 'MSKK'

