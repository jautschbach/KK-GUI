#!/usr/bin/env python
#
# kk-interface-python is a program that creates a GUI for the Kramers-Kronig 
# transforms and reverse-transforms for either a frequency-like or 
# wavelength-like variables using FORTRAN code to perform the transforms.
#
# Along with this the Multiply Subtractive Kramers-Kronig Transform method 
# proposed by Palmer, Williams, Budde and the Chained Doubly-Subtractive
# Kramers-Kronig method proposed by Rudolph and Autschbach was implemented.
#
# All of the methods listed above use the Maclaurin series to perform the 
# integration as proposed by Ohta and Ishida.
#
# To be able to perform the intgration using the above methods the input data
# should be in an evenly spaced grid with respect to the frequency or 
# wavelength variable.
#
# reference:
# Ohta K, Ishida H. Comparison Among Several Numerical Integration Methods for
#     Kramers-Kronig Transformation. Appl Spectrosc 1988;42:952-957.
# Palmer KF, Williams MZ, Budde BA. Multiply subtractive Kramers-Kronig analysis
#     of optical data. Appl Opt 1998;37:2660-2673.
# Rudolph M, Autschbach J. Fast Generation of Nonresonant and Resonant Optical
#     Rotatory Dispersion Curves with the Help of Circular Dichroism Calculations
#     and Kramers-Kronig Transformations. Chirality 2008;20:995-1008.
#
# Copyright (C) 2017 Herbert Ludowieg
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
#
from sys import platform
import sys

# checks if the import file kktransform based on the system being used
# if there is an error it will give an error message and quit the application
import matplotlib
matplotlib.use("Agg")
if len(sys.argv) > 1:
    if sys.argv[1] == '-h':
        op_text = '-----COMMAND LINE OPTIONS------------------\n'+ \
                    '-help     opens HELP text\n'+ \
                    '-lice     opens LISENCE for kk-inter.py\n'+ \
                    '-about    opens ABOUT text\n'+ \
                    '-make     opens make instructions'
        print(op_text)
        sys.exit()
    elif sys.argv[1] == '-help':
        print(open('HELP','r').read())
        sys.exit()
    elif sys.argv[1] == '-about':
        print(open('ABOUT','r').read())
        sys.exit()
    elif sys.argv[1] == '-lice':
        print(open('LICENSE','r').read())
        sys.exit()
    elif sys.argv[1] == '-make':
        if platform == 'linux' or platform == 'linux2':
            print(open('LIN-make','r').read())
        elif platform == 'win32':
            print(open('WIN-make','r').read())
        else:
            print('ERROR could not recognize OS as Linux or Windows')
        sys.exit()
    elif sys.argv[1] != '':
        print('ERROR cannot parse command\nType -h for options')
        sys.exit()
    
#import python modules
import methods

# check the version of python used and adjusts imports accordingly
if sys.version[0][0] == '3':
    from tkinter import *
    from tkinter import ttk, filedialog, messagebox
    from tkinter.font import nametofont, Font
    import tkinter as tk
elif sys.version[0][0] == '2':
    from Tkinter import *
    import ttk
    import tkFileDialog as filedialog
    import Tkinter as tk
    import tkMessageBox as messagebox
    from tkFont import nametofont, Font

import numpy as np
#try:
from scripts import gskk,help,about,indataplt,setdef, \
                loaddef,plot,settings,functions
##except:
#   print('ERROR in importing files from scripts directory.\n'+
#   'Make sure the the scripts file directory is in the same directory\n'+ \
#   'As the kk-inter.py file and that all of the files are contained\n'+ \
#   'about.py,functions.py,gskk.py,help.py,indataplt.py,loaddef.py,\n'+ \
#   'plot.py,setdef.py,settings.py,transdatawin.py\n')
#   print('\nAttempt to import the files manually on the python cli\n'+ \
#   'to see which is giving an error.\n\n')
#   sys.exit()
settings.init()
settings.position = [0,0,0,0,0]
# initializing page setup for program uses a single page
class KK_Interface(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args,**kwargs)
        tk.Tk.wm_title(self, 'Kramers-Kronig Transformations')
        container = tk.Frame(self, relief='flat', borderwidth=3)
        container.pack(side=TOP, fill=BOTH, expand=False)
        self.geometry('+0+0')
        frame = Search_Data(container, self)
        frame.grid(row=0, column=0, sticky=(N,W,E,S))
        self.protocol('WM_DELETE_WINDOW', self.close)
        frame.tkraise()

    def close(self):
        close_text = 'Are you sure you want to quit?\n'+ \
                'All unsaved data will be lost.'
        dialog = messagebox.askyesno(title='Quit Application',
                        icon='question', message=close_text)
        if dialog != 0:
            self.destroy()

    
# start page of program
# class includes all of the widgets to be used
# and their properties
class Search_Data(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        # initializing values
        lbl_open =  StringVar()
        self.real_data =    StringVar()
        self.wave =         StringVar()
        self.axis =         StringVar()
        self.units =        StringVar()
        self.default_name = StringVar()
        self.mskkcdkk =     StringVar()

        # default starting properties
        try:
            infile = open('.default_settings','r')
        except:
            infile = open('.default_settings','a')
            infile.write(r'Default Setting*Dispersive%No%\omega%s^{-1}')
        infile.close()
        self.real_data.set('Dispersive')
        self.wave.set('No')
        self.axis.set('\omega')
        self.units.set('s^{-1}')
        self.default_name.set('Default Setting')
        self.mskkcdkk.set('Execute\nMSKK')

        # creation of tk widgets with some base properties
        self.search_lbl =   tk.Label(self, text='Data taken from:')
        self.open_lbl =     tk.Label(self, textvariable = lbl_open)
        self.search_btn =   tk.Button(self, text = 'Load Data')
        self.search_btn['command'] = lambda: functions.search_data \
                    (self.selected_data,self.exec_btn,lbl_open, \
                            self.check_space, \
                            self.plot_dat_btn,self.gskk_btn,self.data_log)
        self.lis_btn =      tk.Button(self, text = 'LICENSE', 
                            command=self.license)
        self.selected_data= Text(self, width = 35, height = 22, 
                                state = 'disabled')
        self.exec_btn =     tk.Button(self, text = 'Execute\nKK Transform', 
                            state = 'disabled')
        self.exec_btn['command'] =  lambda: self.plot(self.data_log,'KK')
        self.mskk_btn =     tk.Button(self, textvariable = self.mskkcdkk,
                            state = 'disabled') 
        self.mskk_btn['command'] =  lambda: self.plot \
                                    (self.data_log,settings.vardict['method'])
        self.selec_scroll=  tk.Scrollbar(self, orient = VERTICAL, 
                            command = self.selected_data.yview)
        self.help_btn =     tk.Button(self, text='HELP', 
                            command = lambda:self.help('help'))
        self.about_btn =    tk.Button(self, text='ABOUT',
                            command = lambda:self.help('about'))
        self.data_log =     Text(self, width = 67, height = 10, 
                state = 'disabled')
        self.log_scroll =   tk.Scrollbar(self, orient=VERTICAL, 
                            command=self.data_log.yview)
        self.realdata_lbl = tk.Label(self, 
                text = 'Dispersive or Absorptive data?')
        self.realdata_comb= ttk.Combobox(self, textvariable=self.real_data)
        self.wave_lbl =     tk.Label(self, text = 'Wavelength like variable?')
        self.wave_comb =    ttk.Combobox(self, textvariable=self.wave)
        self.axis_lbl =     tk.Label(self, text = 'Select x-axis label')
        self.axis_comb =    ttk.Combobox(self, textvariable=self.axis)
        self.units_lbl =    tk.Label(self, text = 'Select x-axis units')
        self.units_comb =   ttk.Combobox(self, textvariable = self.units)
        self.check_space =  tk.Button(self,text='Check input\ndata spacing',
                command = lambda:functions.open_file('space',data_log),
                    state = 'disabled')
        self.plot_dat_btn = tk.Button(self, text = 'Plot input\ndata',
                command = self.indata_plot, state = 'disabled')
        self.gskk_btn = tk.Button(self, text = 'Use MSKK/CDKK method',
                    command = self.gskk
                    , state = 'disabled')
        self.save_default = tk.Button(self,text='Save settings\nas default',
                command = lambda:self.default('set'))
        self.load_default = tk.Button(self, text = 'Load default\nsettings',
                command = lambda:self.default('load'))
        self.default_lbl =  tk.Label(self, textvariable=self.default_name)

        # widget specific properties
        self.selected_data['yscrollcommand'] = self.selec_scroll.set
        self.data_log['yscrollcommand'] = self.log_scroll.set       
        self.realdata_comb['values'] = ['Dispersive','Absorptive']
        self.wave_comb['values'] = ['Yes','No']
        self.axis_comb['values'] = ['Energy',r'\nu',r'\tilde \nu','\omega']
        self.units_comb['values'] = ['s^{-1}','cm^{-1}','10^{3}cm^{-1}','eV','nm']
        self.realdata_comb['state'] = 'readonly'
        self.wave_comb['state'] = 'readonly'

        # set a base font for all objects
        baseFont = nametofont("TkDefaultFont")
        baseFont.configure(family='gothic',size=10)

        # widget grid command locations
        # arranged by increasing column and row 
        self.search_lbl.grid        (column=1, row=1, sticky=(W))
        self.open_lbl.grid      (column=1, row=2, columnspan=3, sticky=(W))
        self.selected_data.grid (column=1, row=3, rowspan=14, 
                        sticky=(N,S,E,W))
        self.data_log.grid      (column=1, row=17, columnspan=4, 
                        sticky=(W,E))
        self.selec_scroll.grid  (column=2, row=3, rowspan=14, sticky=(N,S,W))
        self.search_btn.grid        (column=3, row=1, sticky=(N,S,E,W))
        self.lis_btn.grid       (column=4, row=1, sticky=(N,S,E,W))
        self.help_btn.grid      (column=3, row=3, sticky=(W,E))
        self.check_space.grid   (column=3, row=4, sticky=(W,E))
        self.plot_dat_btn.grid  (column=4, row=4, sticky=(W,E))
        self.gskk_btn.grid      (column=3, row=5, columnspan=2,
                        sticky=(W,E))
        self.exec_btn.grid      (column=3, row=6, sticky=(N,S,W,E))
        self.mskk_btn.grid  (column=4, row=6, sticky=(N,S,W,E))
        self.default_lbl.grid   (column=3, row=7, columnspan=2, sticky=(W))
        self.realdata_lbl.grid  (column=3, row=8, columnspan=2, sticky=(W,E))
        self.realdata_comb.grid (column=3, row=9, columnspan=2, sticky=(W,E))
        self.wave_lbl.grid      (column=3, row=10, columnspan=2, 
                        sticky=(W,E))
        self.wave_comb.grid     (column=3, row=11, columnspan=2, 
                        sticky=(W,E))
        self.axis_lbl.grid      (column=3, row=12, columnspan=2, 
                        sticky=(W,E))
        self.axis_comb.grid     (column=3, row=13, columnspan=2, 
                        sticky=(W,E))
        self.units_lbl.grid     (column=3, row=14, columnspan=2, 
                        sticky=(W,E))
        self.units_comb.grid        (column=3, row=15, columnspan=2, 
                        sticky=(W,E))
        self.save_default.grid  (column=3, row=16, sticky=(W,E))
        self.about_btn.grid     (column=4, row=3, sticky=(W,E))
        self.load_default.grid  (column=4, row=16, sticky=(W,E))
        self.log_scroll.grid        (column=5, row=17, sticky=(N,S,W))

        settings.vardict = {'numanchor':'0','real':'','wave':'','axis':'', \
                    'units':'','index':'0','mskk/cdkk':'none'}

        self.selected_data['state'] = 'normal'
        self.selected_data.insert('1.0','kk-interface-python\n\n'+ \
                    'Copyright(C) 2016 Herbert Ludowieg\n\n'+ \
                    'This program comes with ABSOLUTELY\n'+ \
                    'NO WARRANTY; for details look\n'+ \
                    'at the textbox below which shows\n'+ \
                    'sections 15 and 16 taken from the\n'+ \
                    'LICENSE which can be accesed\n'+ \
                    'through the LICENSE button.\n\n'+ \
                    'This is free software, and you are\n'+ \
                    'welcome to redistribute it under\n'+ \
                    'certain terms and conditions as\n'+ \
                    'per given under the GNU General\n'+ \
                    'Public License included under the\n'+ \
                    'LICENSE button on this GUI.\n\n'+ \
                    'For details on the program and\n'+ \
                    'a general description click on the\n'+ \
                    'ABOUT button.\n\n'+ \
                    'For help with execution click on\n'+ \
                    'the HELP button.')
        self.selected_data['state'] = 'disabled'
        self.data_log['state'] = 'normal'
        self.data_log.insert('1.0','  15. Disclaimer of Warranty.\n\n'+ \
'  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY\n'+ \
'APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE\n'+ \
'COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS"\n'+ \
'WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED,\n'+ \
'INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF\n'+ \
'MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE\n'+ \
'RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.\n'+ \
'SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL\n'+ \
'NECESSARY SERVICING, REPAIR OR CORRECTION.\n\n'+ \
'  16. Limitation of Liability.\n\n'+ \
'  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN\n'+ \
'WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES\n'+ \
'AND/OR CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU\n'+ \
'FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR\n'+ \
'CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE\n'+ \
'THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA\n'+ \
'BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD\n'+ \
'PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER\n'+ \
'PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF\n'+ \
'THE POSSIBILITY OF SUCH DAMAGES.\n\n'+ \
'  17. Interpretation of Sections 15 and 16.\n\n'+ \
'  If the disclaimer of warranty and limitation of liability\n'+ \
'provided above cannot be given local legal effect according to\n'+ \
'their terms, reviewing courts shall apply local law that most\n'+ \
'closely approximates an absolute waiver of all civil liability in\n'+ \
'connection with the Program, unless a warranty or assumption of\n'+ \
'liability accompanies a copy of the Program in return for a fee.')
        self.data_log['state'] = 'disabled'

    # makes the properties for the toplevel window for the Plots class
    def plot(self,data_log,method):
        settings.vardict['real'] = self.real_data.get()
        settings.vardict['wave'] = self.wave.get()
        settings.vardict['axis'] = self.axis.get()
        settings.vardict['units'] = self.units.get()

        f = functions.main(data_log,method)
        self.plot_win = tk.Toplevel(self)

        x = 3 + self.winfo_rootx() + self.winfo_width() + \
                        (int(settings.vardict['index']) * 50)
        y = self.winfo_rooty() + (int(settings.vardict['index']) * 50) - 32
        self.plot_win.geometry('+'+str(x)+'+'+str(y))
        self.app = plot.Plots(self.plot_win,f[0],f[1],f[2],f[3])
    
    # sets the properties of the toplevel window for the Help class
    def help(self,arg):
        self.help_win = tk.Toplevel(self)
        self.help_win.geometry('+50+74')
        if arg == 'help':
            self.app = help.Help(self.help_win)
        elif arg == 'about':
            self.app = about.About(self.help_win)
    
    def indata_plot(self):
        self.in_plot = tk.Toplevel(self)
        self.in_plot.geometry('+100+124')
        points = functions.open_file('plot','')
        self.app = indataplt.InputDataPlot(self.in_plot,points)
    
    def default(self,type):
        settings.vardict['real'] = self.real_data.get()
        settings.vardict['wave'] = self.wave.get()
        settings.vardict['axis'] = self.axis.get()
        settings.vardict['units'] = self.units.get()
        win = tk.Toplevel(self)
        x = self.winfo_rootx() - 3
        y = self.winfo_rooty() + self.winfo_height()
        win.geometry('+'+str(x)+'+'+str(y))
        if type == 'set':
            self.app = setdef.SetDefault(win,self.default_name)
        elif type == 'load':
            self.app = loaddef.LoadDefault(win,self.default_name, \
                    self.real_data,self.wave,self.axis,self.units)
    
    def gskk(self):
        self.gskk_win = tk.Toplevel(self)
        x = self.winfo_rootx()
        y = 3 + self.winfo_rooty() + self.winfo_height()
        self.gskk_win.geometry('+'+str(x)+'+'+str(y))
        self.app = gskk.GSKK(self.gskk_win,self.mskk_btn,self.mskkcdkk)
    
    def license(self):
        self.lis_win = tk.Toplevel(self)
        self.lis_win.geometry('+50+0')
        frame =     tk.Frame(self.lis_win,borderwidth=3)
        lis_text =  Text(frame, width = 80, height = 45)
        exit_btn =  tk.Button(frame,text='Close Liscence',
                    command=self.lis_win.destroy)
        scroll =    tk.Scrollbar(frame,orient=VERTICAL,
                        command=lis_text.yview)
        lis_text['yscrollcommand'] = scroll.set
        frame.grid  (column=0,row=0,sticky=(N,W,E,S))
        lis_text.grid   (column=1,row=1,sticky=(N,W,E,S))
        exit_btn.grid   (column=1,row=2,columnspan=2,sticky=(W,E))
        scroll.grid (column=2,row=1,sticky=(N,S))
        fn = open('LICENSE','r')
        lis_text.insert('1.0',fn.read())
        fn.close()
        
app = KK_Interface()
app.mainloop()
