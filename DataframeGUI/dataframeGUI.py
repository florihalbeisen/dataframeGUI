# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 22:35:23 2018

@author: Florian
"""

import wx
import wx.lib.mixins.listctrl  as  listmix
import os
import pandas as pd
#import numpy as np

from scipy import stats

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import Toolbar
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure



data = pd.read_csv('breeding_sucess_short.csv', sep=",")
df = pd.DataFrame(data)




class DataFrameView(wx.Panel):
    ''' To do:
        - Load datasets from 
    
    '''
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
 
    
        # To do - Add a Button or something to choose 
       # b =  wx.StaticText(self, -1, "This is a PageTwo object", (20,40))
        
        self.list_ctrl = ListCtrlDataFrame(self, style=wx.LC_REPORT)
        for colomn in range(len(df.columns)):
            self.list_ctrl.InsertColumn(colomn, data.columns.values[colomn])
            
        index = 0
        for i, row in df.iterrows():
            self.list_ctrl.InsertStringItem(index, str(row[0])) 
            
            for col in range(1,len(df.columns)):
                self.list_ctrl.SetStringItem(index, col, str(row[col]))
            
            index += 1
 
        sizer = wx.BoxSizer(wx.VERTICAL)
#        sizer.Add(b, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.list_ctrl, 1, wx.ALL | wx.EXPAND | wx.GROW, 5)
        self.SetSizer(sizer)
        



class ListCtrlDataFrame(wx.ListCtrl, listmix.TextEditMixin):
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        """Constructor"""
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)


class Plots(wx.Panel):
    
    ''' To do   
        - Checks if data are numbers  
        - Max restiction for boxplot
        - Label for ComboBox - x or y axis?
        - 
    
    '''
    
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        
        # Radio buttons - selection of plot type 
        self.rb1 = wx.RadioButton(self, 1, label = 'Scatter plot',  style = wx.RB_GROUP) 
        self.rb2 = wx.RadioButton(self, 2, label = 'Box plot')
        self.rb3 = wx.RadioButton(self, 3, label = 'QQ-plot') 
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup) 

        # Dropdown menu for choosing variables
        self.combo1 = wx.ComboBox(self, choices = df.columns, style=wx.CB_READONLY)
        self.combo2 = wx.ComboBox(self, choices = df.columns, style=wx.CB_READONLY) 

        # Button to draw plot
        self.btn = wx.Button(self, -1, "OK")
        self.btn.Bind(wx.EVT_BUTTON, self.redraw) 
        
        # matplot figure 
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)  # matplotlib toolbar
        self.toolbar.Realize()
        
        # Initalize sizers 
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.comboSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.plotSizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add radio button to sizer
        self.buttonSizer.Add(self.rb1, 0, wx.LEFT  | wx.TOP | wx.GROW, 10)
        self.buttonSizer.Add(self.rb2, 0, wx.LEFT | wx.TOP | wx.GROW, 10)
        self.buttonSizer.Add(self.rb3, 0, wx.LEFT | wx.TOP | wx.GROW, 10)
        self.buttonSizer.Add(self.btn, 0, wx.LEFT | wx.TOP | wx.GROW, 10)
        
        # Add drop down to sizer
        self.comboSizer.Add(self.combo1, 0, wx.LEFT | wx.TOP | wx.GROW, 10)
        self.comboSizer.Add(self.combo2, 0, wx.LEFT | wx.TOP | wx.GROW, 10)
        
        # Add plot to sizer
        self.plotSizer.Add(self.canvas, 0, wx.LEFT | wx.EXPAND, border=5)
        self.plotSizer.Add(self.toolbar, 0 , wx.LEFT | wx.EXPAND, border=5)
         
        # Combine sub sizer to panal sizer
        self.panelSizer.Add(self.buttonSizer, 0, wx.LEFT | wx.GROW, border=5)
        self.panelSizer.Add(self.comboSizer, 0, wx.LEFT | wx.GROW, border=5)
        self.panelSizer.Add(self.plotSizer, 0, wx.LEFT | wx.GROW | wx.EXPAND, border=5)

        # Connect panal to panelSizer
        self.SetSizer(self.panelSizer)
        # Calculate size based on the window (i.e. frame)
        self.Fit()
    
        self.Show(True)

    def redraw(self, event):
        column_1 = self.combo1.GetSelection()
        column_2 = self.combo2.GetSelection()
        
        # Scatter plot
        if self.rb1.GetValue() == True:
            self.axes.clear()
            self.axes.plot(df.iloc[:, column_1].values, df.iloc[:, column_2].values, 'o', clip_on=False)
        
        # Box plot     
        elif self.rb2.GetValue() == True:
            self.axes.clear()
           
            df_sorted = df.sort_values(by=[df.columns[column_2]])
            data = []
            groups = []
            for groups in pd.unique(df_sorted.iloc[:, column_2].values):
                data.append(df_sorted.loc[df_sorted.iloc[:,column_2] == groups, df_sorted.columns[column_1]])

            self.axes.boxplot(data)
            self.axes.set_xticklabels(pd.unique(df_sorted.iloc[:, column_2].values), rotation=45, fontsize=8)

        # QQ-Plot
        elif self.rb3.GetValue() == True:
            self.axes.clear()
            stats.probplot(df.iloc[:, column_1].values, plot=self.axes)

        self.canvas.draw()

                
    def OnRadiogroup(self, event):
        if event.GetEventObject().GetId() != 3:
            self.combo2.Show()
        else:
            self.combo2.Hide()
        
   
    

class DataFrameEdit(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
#        t = wx.StaticText(self, -1, "This is a PageThree object", (60,60))


class MainFrame(wx.Frame):
    def __init__(self):
        self.dirname=''
        wx.Frame.__init__(self, None, size=(-1,-1), title="Simple Notebook Example")

       # self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        # Setting up the menu.
        filemenu= wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a file to edit")
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Events.
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        
        
        # Here we create a panel and a notebook on the panel
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)

        # create the page windows as children of the notebook
        page1 = DataFrameView(notebook)
        page2 = Plots(notebook)
        page3 = DataFrameEdit(notebook)
        page1.SetFocus()

        # add the pages to the notebook with the label to show on the tab
        notebook.AddPage(page1, "DataFrame")
        notebook.AddPage(page2, "Plots")
        notebook.AddPage(page3, "Edit")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)


    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, " A sample editor \n in wxPython", "About Sample Editor", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.


    def OnOpen(self,e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()





if __name__ == "__main__":
    app = wx.App()
    

    
    MainFrame().Show()
    app.MainLoop()