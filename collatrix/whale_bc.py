#import modules
import pandas as pd
import numpy as np
import os, sys
import math
from scipy.integrate import quad
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

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

        #ask for input csv
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        input_csv, _ = QFileDialog.getOpenFileName(self,"CollatriX output file", "","All Files (*);;csv files (*.csv)", options=options)
        if input_csv:
            print("collatrix output file = {0}".format(input_csv))

        #import csv
        df_all = pd.read_csv(input_csv,sep = ",")
        df_all.columns = df_all.columns.str.replace(".00%", ".0%")


        #ask if they want body Volume
        items = ('yes','no')
        volchoice, okPressed = QInputDialog.getItem(self, 'Do you want body volume to be calculated? (width measurements required)','',items,0,False)
        if okPressed and volchoice:
            print("{0} body volume calculated".format(volchoice))

        if volchoice == 'yes':
            n, okPressed = QInputDialog.getText(self, "What did you name the total length measurement?","Total Length Name:", QLineEdit.Normal, "")
            if okPressed and n != '':
                tl_name= str(n)
            l, okPressed = QInputDialog.getText(self, "Lower Bound","Lower Bound:", QLineEdit.Normal, "")
            if okPressed and l != '':
                lower= int(l)
            u, okPressed = QInputDialog.getText(self, "Upper Bound","Upper Bound:", QLineEdit.Normal, "")
            if okPressed and u != '':
               upper = int(u)
            i, okPressed = QInputDialog.getText(self, "Interval","Interval:", QLineEdit.Normal, "")
            if okPressed and i != '':
                interval = int(i)
            print("for body volume: length name = {0}, lower bound = {1}, upper bound = {2}, interval = {3}".format(tl_name,lower,upper,interval))
        elif volchoice == 'no':
            pass

        #ask if they want BAI
        items = ('yes','no')
        baichoice, okPressed = QInputDialog.getItem(self, 'Do you want BAI to be calculated? (you have to have measured Total_Length widths)','',items,0,False)
        if okPressed and baichoice:
            print("{0} BAI calculated".format(baichoice))

        if baichoice == 'yes':
            #ask if they want trapezoid method, parabola method, or both methods
            items = ('parabola','trapezoid','both')
            bai_method, okPressed = QInputDialog.getItem(self, 'Do you want BAI to be to measured using parabolas, trapezoids, or both?','',items,0,False)
            if okPressed and bai_method:
                print("BAI calculated using {0} method(s)".format(bai_method))
            #get intervals
            n, okPressed = QInputDialog.getText(self, "What did you name the total length measurement?","Total Length Name:", QLineEdit.Normal, "")
            if okPressed and n != '':
                tl_name= str(n)
            l, okPressed = QInputDialog.getText(self, "Lower Bound","Lower Bound:", QLineEdit.Normal, "")
            if okPressed and l != '':
                b_lower= int(l)
            u, okPressed = QInputDialog.getText(self, "Upper Bound","Upper Bound:", QLineEdit.Normal, "")
            if okPressed and u != '':
               b_upper = int(u)
            i, okPressed = QInputDialog.getText(self, "Interval","Interval:", QLineEdit.Normal, "")
            if okPressed and i != '':
                b_interval = int(i)
            print("for BAI: length name = {0}, lower bound = {1}, upper bound = {2}, interval = {3}".format(tl_name,b_lower,b_upper,b_interval))
        elif baichoice == 'no':
            pass

        #ask for name of output
        outname, okPressed = QInputDialog.getText(self, "output name",'name',QLineEdit.Normal,"")

        #where should output be saved?
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        saveFold = QFileDialog.getExistingDirectory(None, "folder where output should be saved",options=options)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        #functions
        def body_vol(df_all,tl_name,interval,lower,upper):
            body_name = "Body_Vol_{0}%".format(interval) #name of body volume column will use interval amount
            volm = [] #make empty list of widths
            for x in range(lower,(upper + interval), interval): #loop through range of widths
                xx = "{0}-{1}.0%".format(tl_name,str(x)) #create the name of the headers to pull measurements from
                volm += [xx] #add to list
            vlist = []
            for i in volm: #loop through column headers
                for ii in df_all.columns:
                    if i in ii:
                        vlist += [ii]
            ids = []; vs = []; imgs = []
            for i,j in enumerate(vlist[:-1]):
                jj = vlist[i+1]
                #calculate volume by looping through two columns at a time
                for rr, RR, hh,anid,img in zip(df_all[j],df_all[jj], df_all[tl_name],df_all['Animal_ID'],df_all['Image']):
                    ph = float(interval)/float(100); h = float(hh)*ph
                    r = float(rr)/float(2); R = float(RR)/float(2)
                    v1 = (float(1)/float(3))*(math.pi)*h*((r**2)+(r*R)+(R**2))
                    ids += [anid]; vs += [v1]; imgs += [img]
            d = {'Animal_ID':ids, body_name:vs, 'Image':imgs} #make dataframe of id and body volume
            df = pd.DataFrame(data = d) #make dataframe
            cls = df.columns.tolist() #get list of column headers
            grBy = ['Animal_ID','Image'] #list of columns to group by
            groups = [x for x in cls if x not in grBy] #get list of columns to be grouped
            df1 = df.groupby(['Animal_ID','Image'])[groups].apply(lambda x: x.astype(float).sum()).reset_index() #group to make sure no duplicates
            df_vol = pd.merge(df_all,df1,on = ['Animal_ID','Image']) #merge volume df with big df
            return df_vol

        def bai_parabola(df_all,tl_name,b_interval,b_lower,b_upper):
            bai_name = "BAIpar_{0}%".format(b_interval) #create BAI column header using interval
            bai = [] #list of columns containing the width data we want to use to calculate BAI
            perc_l = []
            for x in range(b_lower,(b_upper + b_interval), b_interval): # loop through columns w/in range we want
                xx = "{0}-{1}.0%".format(tl_name,str(x)) #set up column name
                bai += [xx]
                perc_l += [x/100]
            #here we check that the widths are actually in the column headers
            blist = []
            for i in bai:
                for ii in df_all.columns:
                    if i in ii:
                        blist += [ii]
            #make empty lists to be filled
            ids = []
            bais = []
            imgs = []
            #loop through the dataframe by image/ID
            for img,anid in zip(df_all['Image'],df_all['Animal_ID']):
                idx = df_all.loc[df_all['Image'] == img].index[0]
                ids += [anid]
                imgs += [img]
                #fill list of y values (y = width)
                ylist = []
                for b in blist:
                    ylist += [(df_all[b].tolist()[idx])] #populate y values withwidth at each incr.
                ylist = np.array(ylist)

                tl = df_all[tl_name].tolist()[idx]
                min_tl = tl*(b_lower/100)
                max_tl = tl*(b_upper/100)

                xlist = [x*tl for x in perc_l] #populate x vlaues with x of TL at each incr.
                xlist = np.array(xlist)

                #make list of 500 x values along TL between bounds
                newx = np.linspace(min_tl,max_tl,500)

                #fit quadratric linear model using original x and y lists. then fit to big list of x values
                lm = np.polyfit(xlist,ylist,2)
                fit = np.poly1d(lm)
                pred = fit(newx)

                #integrate using linear model to get surface area
                I = quad(fit,min_tl,max_tl)
                sa = I[0]

                #calculate BAI
                bai = (sa/((tl*((b_upper-b_lower)/float(100)))**2))*100

                bais += [bai]

            d = {'Animal_ID':ids, bai_name:bais, 'Image':imgs}
            df = pd.DataFrame(data = d)

            cls = df.columns.tolist()
            grBy = ['Animal_ID','Image']
            groups = [x for x in cls if x not in grBy]
            dfp = df.groupby(['Animal_ID','Image'])[groups].apply(lambda x: x.astype(float).sum()).reset_index()
            return dfp

        def bai_trapezoid(df_all,tl_name,b_interval,b_lower,b_upper):
            bai_name = "BAItrap_{0}%".format(b_interval) #create BAI column header using interval
            bai = [] #list of columns containing the width data we want to use to calculate BAI
            for x in range(b_lower,(b_upper + b_interval), b_interval): # loop through columns w/in range we want
                xx = "{0}-{1}.0%".format(tl_name,str(x)) #set up column name
                bai += [xx]
            blist = []
            for i in bai:
                for ii in df_all.columns:
                    if i in ii:
                        blist += [ii]
            ids = []
            bais = []
            imgs = []
            for i,j in enumerate(blist[:-1]):
                jj = blist[i+1]
                for w, W, hh,anid,img in zip(df_all[j],df_all[jj], df_all[tl_name],df_all['Animal_ID'],df_all['Image']):
                    ph = float(b_interval)/float(100)
                    h = float(hh)*ph
                    sa1 = (float(1)/float(2))*(w+W)*h
                    ids += [anid]
                    bais += [sa1]
                    imgs += [img]
            d = {'Animal_ID':ids, bai_name:bais, 'Image':imgs}
            df = pd.DataFrame(data = d)

            cls = df.columns.tolist()
            grBy = ['Animal_ID','Image']
            groups = [x for x in cls if x not in grBy]
            df1 = df.groupby(['Animal_ID','Image'])[groups].apply(lambda x: x.astype(float).sum()).reset_index()
            dft = pd.merge(df_all[['Animal_ID','Image',tl_name]],df1,on = ['Animal_ID','Image'])
            dft[bai_name] = (dft[bai_name]/((dft[tl_name]*((b_upper-b_lower)/float(100)))**2))*100
            dft = dft.drop([tl_name],axis=1)
            return dft

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
        df_all1.to_csv(outcsv,sep = ',')

        print(df_all1)

        print("done, close GUI window to end script")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
