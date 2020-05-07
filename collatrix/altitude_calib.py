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

        #####INPUTS#####
        #get file containing board img list w/
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        calib_csv, _ = QFileDialog.getOpenFileName(self,"calibration object img list", "","All Files (*);;csv files (*.csv)", options=options)
        print("calibration object csv = {0}".format(calib_csv))

        #get file containing non-calibration img list (this will become the safety)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        img_csv, _ = QFileDialog.getOpenFileName(self,"img list w/ altitudes", "","All Files (*);;csv files (*.csv)", options=options)
        print("image csv = {0}".format(img_csv))

        #what did they name the length of the board
        n, okPressed = QInputDialog.getText(self, "What did you name the board length measurement?","Board Length Name:", QLineEdit.Normal, "")
        if okPressed and n != '':
            bl_name= str(n)

        n, okPressed = QInputDialog.getText(self, "What is the true length of the calibration object (in meters)?","Calibration Object Length", QLineEdit.Normal, "")
        if okPressed and n != '':
            ob_l= float(n)

        #get folder
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        GUIfold = QFileDialog.getExistingDirectory(None, str("folder containing MorphoMetriX outputs"),options=options)
        saveFold = QFileDialog.getExistingDirectory(None,str("folder where output should be saved"),options=options)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        ####SET UP####
        #make empty lists
        measurements= ['Image','Animal_ID','Notes',bl_name, 'OLp','DateFlight']
        names = ['Image','Animal_ID','Notes']
        csvs_all = []
        csvs = []
        not_mmx = []

        #walk through all folders in GUI folder and collect all csvs
        for root,dirs,files in os.walk(GUIfold):
            csvs_all += [os.path.join(root,f) for f in files if f.endswith('.csv')]
        #make sure the csvs are morphometrix outputs by checking first row
        csvs += [c for c in csvs_all if 'Image ID' in pd.read_csv(c,nrows=1,header=None)[0].tolist()]
        #make list of all csvs that were not morphometrix csvs to tell user
        not_mmx += [x for x in csvs if x not in csvs_all]
        print("these csvs were not morphometrix outputs: {0}".format(not_mmx))

        #import calibration object csv
        df_cal = pd.read_csv(calib_csv,sep = ',')

        #####COLLATE#####
        mDict = dict.fromkeys(measurements)
        keys = list(mDict.keys())
        df_all = pd.DataFrame (columns = keys)

        for f in csvs:
            print(f)
            temp=pd.read_csv(f,sep='^',header=None,prefix='X',engine = 'python') #import as one column
            df1=temp.X0.str.split(',',expand=True) #split on comma delimeter
            df00 = df1.replace("",np.nan)
            df0 = df00.dropna(how='all',axis = 'rows')
            df0 = df0.fillna('') #replace nans by blank space
            idx = df0.loc[df0[0]=='Object'].index #set object column to index
            df = df0.truncate(after=idx[0]) #subset df to be only top info section

            #go into the cvs to look for the measurement values
            dfGUI = df0.truncate(before=idx[0]) #now subset the df so we're just looking at the measurements
            head = dfGUI.iloc[0] #isolate the current header row
            dfGUI.columns = head #make the header the original header
            dfGUI = dfGUI.set_index('Object') #make index column the one named Object

            #if calibration object length was measured, process. this means that if some whale outputs are included,
            #thats ok, they won't go through because calibration object length wasn't measured.
            if bl_name in dfGUI.index:
                #get information from top of output sheet
                aID = df[df[0] == 'Image ID'].loc[:,[1]].values[0] #pull animal id
                aID = aID[0]
                mDict['Animal_ID'] = aID

                image = os.path.split(df[df[0] == 'Image Path'].loc[:,1].values[0])[1] #extract image
                print(image)
                mDict['Image'] = image
                notes = df[df[0] == 'Notes'].loc[:,[1]].values[0] #extract entered notes
                mDict['Notes'] = notes[0]

                alt = float((df[df[0] == 'Altitude'].loc[:,[1]].values[0])[0]) #extract entered altitude
                focl = float((df[df[0] == 'Focal Length'].loc[:,[1]].values[0])[0]) #extract entered focal length
                pixd = float((df[df[0] == 'Pixel Dimension'].loc[:,[1]].values[0])[0]) #extract entered pixel dimension

                #pull measurement from measurement part of sheet
                x = float(dfGUI.loc[bl_name,'Length (m)'])
                mDict[bl_name] = x
                pixc = (x/pixd)*(focl/alt) #back calculate the pixel count
                mDict['OLp'] = pixc

                df_op = pd.DataFrame(data = mDict,index=[1]) #make dictionary (now filled with the measurements from this one csv) into dataframe
                df_all = pd.concat([df_all,df_op],sort = True)
        print(df_all)

        df_total = df_all.merge(df_cal, on = ['Image'])
        df_total['DateFlight'] = [x + "_" + y for x,y in zip(df_total['Date'],df_total['Flight'])]

        #ok now we have a dataframe and want to make the linear model
        #read in list of images that we want altitude for
        dfImg = pd.read_csv(img_csv,sep =',')
        dfImg['DateFlight'] = [x + "_" + y for x,y in zip(dfImg['Date'],dfImg['Flight'])]

        #loop through DateFlights, run linear model, predict acurate value for image altitude
        dateflights = set(df_total['DateFlight'])
        dlist = ['Image','Altitude']
        iDict = dict.fromkeys(dlist)
        k = list(iDict.keys())
        df_calib = pd.DataFrame (columns = k)
        for datefl in dateflights:
            df_board = df_all.loc[df_total['DateFlight']==datefl]
            df_image = dfImg.loc[dfImg['DateFlight']==datefl]

            OLp = df_board['OLp'].tolist()
            logOLp = [math.log10(x) for x in OLp]

            Alts = df_board['Altitude'].tolist()
            logAlts = [math.log10(x) for x in Alts]

            lm1 = np.polyfit(logAlts,logOLp,1)
            fitsmooth = np.poly1d(lm1)
            pred = 10**(fitsmooth(logAlts))
            df_board['pred'] = pred
            Board = (df_board['Focal_Length']*(ob_l/df_board['pred']))/df_board['PixD'].tolist()
            lm2 = np.polyfit(Alts,Board,1)
            fit = np.poly1d(lm2)

            for img, b_alt in zip(df_image['Image'],df_image['Baro_Alt']):
                iDict['Image'] = img
                iDict['Altitude'] = fit(b_alt)

            df_temp = pd.DataFrame(data=iDict,index=[1])
            df_calib = pd.concat([df_calib,df_temp])
        print(df_calib)
        outcsv = os.path.join(saveFold,"altitude_calibration.csv")
        df_calib.to_csv(outcsv,sep = ',')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
