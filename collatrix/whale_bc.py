#import modules
import pandas as pd
import numpy as np
import os, sys
import math
from scipy.integrate import quad
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon

#import functions
from bodycondition_functions import body_vol
from bodycondition_functions import bai_parabola
from bodycondition_functions import bai_trapezoid

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'close box to end script'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

        #add message box with link to github documentation
        msgBox = QMessageBox()
        msgBox.setWindowTitle("For detailed input info click link below")
        msgBox.setTextFormat(QtCore.Qt.RichText)
        msgBox.setText('<a href = "https://github.com/cbirdferrer/collatrix#whale-body-condition-function">CLICK HERE</a> for detailed input instructions, \n then click on OK button to continue')
        x = msgBox.exec_()

        #ask for input csv
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        input_csv, _ = QFileDialog.getOpenFileName(self,"Input 1. CollatriX output file", "","All Files (*);;csv files (*.csv)", options=options)
        if input_csv:
            print("collatrix output file = {0}".format(input_csv))

        #import csv
        df_all = pd.read_csv(input_csv,sep = ",")
        df_all = df_all.dropna(how="all",axis='rows').reset_index()
        df_all.columns = df_all.columns.str.replace(".00%", ".0%")

        #set up empty message list
        message = []
        #ask if they want body Volume
        items = ('yes','no')
        volchoice, okPressed = QInputDialog.getItem(self, 'Input 2.', 'Do you want body volume to be calculated? (width measurements required)',items,0,False)
        if okPressed and volchoice:
            print("{0} body volume calculated".format(volchoice))

        if volchoice == 'yes':
            n, okPressed = QInputDialog.getText(self, "Input 2.1", "What did you name the total length measurement? \n Total Length Name:", QLineEdit.Normal, "")
            if okPressed and n != '':
                tl_name= str(n)
            l, okPressed = QInputDialog.getText(self, "Input 2.2", "Lower Bound:", QLineEdit.Normal, "")
            if okPressed and l != '':
                lower= int(l)
            u, okPressed = QInputDialog.getText(self, "Input 2.3", "Upper Bound:", QLineEdit.Normal, "")
            if okPressed and u != '':
               upper = int(u)
            i, okPressed = QInputDialog.getText(self, "Input 2.4","Interval:", QLineEdit.Normal, "")
            if okPressed and i != '':
                interval = int(i)
            print("for body volume: length name = {0}, lower bound = {1}, upper bound = {2}, interval = {3}".format(tl_name,lower,upper,interval))
            volmess = "for body volume: length name = {0}, lower bound = {1}, upper bound = {2}, interval = {3}".format(tl_name,lower,upper,interval)
        elif volchoice == 'no':
            volmess = "no body volume calculated"
            pass

        #ask if they want BAI
        items = ('yes','no')
        baichoice, okPressed = QInputDialog.getItem(self, 'Input 3', "Do you want BAI to be calculated? (you have to have measured Total_Length widths)",items,0,False)
        if okPressed and baichoice:
            print("{0} BAI calculated".format(baichoice))
        if baichoice == 'yes':
            #ask if they want trapezoid method, parabola method, or both methods
            items = ('parabola','trapezoid','both')
            bai_method, okPressed = QInputDialog.getItem(self, 'Input 3.1', "Do you want BAI to be to measured using parabolas, trapezoids, or both?",items,0,False)
            if okPressed and bai_method:
                print("BAI calculated using {0} method(s)".format(bai_method))
            #get intervals
            n, okPressed = QInputDialog.getText(self, "Input 3.2", "What did you name the total length measurement?", QLineEdit.Normal, "")
            if okPressed and n != '':
                tl_name= str(n)
            l, okPressed = QInputDialog.getText(self, "Input 3.3", "Lower Bound:", QLineEdit.Normal, "")
            if okPressed and l != '':
                b_lower= int(l)
            u, okPressed = QInputDialog.getText(self, "Input 3.4","Upper Bound:", QLineEdit.Normal, "")
            if okPressed and u != '':
               b_upper = int(u)
            i, okPressed = QInputDialog.getText(self, "Input 3.5","Interval:", QLineEdit.Normal, "")
            if okPressed and i != '':
                b_interval = int(i)
            print("for BAI: length name = {0}, lower bound = {1}, upper bound = {2}, interval = {3}".format(tl_name,b_lower,b_upper,b_interval))
            baimess = "for BAI: length name = {0}, lower bound = {1}, upper bound = {2}, interval = {3}".format(tl_name,b_lower,b_upper,b_interval)
        elif baichoice == 'no':
            baimess = 'no BAI calculated'
            pass

        #ask for name of output
        outname, okPressed = QInputDialog.getText(self, "Input 4",'Output Name:',QLineEdit.Normal,"")

        #where should output be saved?
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        saveFold = QFileDialog.getExistingDirectory(None, "Input 5: folder where output should be saved",options=options)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        #set up output with inputs
        message = "Whale Body Condition Processing Inputs: {0}, {1}".format(volmess,baimess)
        mess = pd.DataFrame(data={'Processing Notes':message},index=[1])
        mess_out = os.path.join(saveFold,"{0}_processing_notes.txt".format(outname))
        mess.to_csv(mess_out)

        #process the data
        if volchoice == 'yes':
            df_allx = body_vol(df_all,tl_name,interval,lower,upper)
        elif volchoice == 'no':
            df_allx = df_all

        if baichoice == 'yes':
            if bai_method == 'parabola':
                df_bai = bai_parabola(df_all,tl_name,b_interval,b_lower,b_upper)
            elif bai_method == 'trapezoid':
                df_bai = bai_trapezoid(df_all,tl_name,b_interval,b_lower,b_upper)
            elif bai_method == 'both':
                df_par = bai_parabola(df_all,tl_name,b_interval,b_lower,b_upper)
                df_trap = bai_trapezoid(df_all,tl_name,b_interval,b_lower,b_upper)
                df_bai = pd.merge(df_par,df_trap,on = ['Animal_ID','Image'])
            df_all1 = pd.merge(df_allx,df_bai,on = ['Animal_ID','Image'])
        elif baichoice == 'no':
            df_all1 = df_allx

        outcsv = os.path.join(saveFold,"{0}_bodycondition.csv".format(outname))
        df_all1.to_csv(outcsv,sep = ',',index_label = 'IX')

        print(df_all1)

        print("done, close GUI window to end script")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
