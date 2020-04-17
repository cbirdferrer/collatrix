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

        #get file containing board img list w/
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        img_csv, _ = QFileDialog.getOpenFileName(self,"img list w/ altitudes", "","All Files (*);;csv files (*.csv)", options=options)
        print("image csv = {0}".format(img_csv))

        #what did they name the length of the board
        n, okPressed = QInputDialog.getText(self, "What did you name the board length measurement?","Board Length Name:", QLineEdit.Normal, "")
        if okPressed and n != '':
            bl_name= str(n)

        n, okPressed = QInputDialog.getText(self, "What is the true length of the calibration object?","Calibration Object Length", QLineEdit.Normal, "")
        if okPressed and n != '':
            ob_l= float(n)

        #get folder
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        GUIfold = QFileDialog.getExistingDirectory(None, str("folder containing MorphoMetriX outputs"),options=options)
        saveFold = QFileDialog.getExistingDirectory(None,str("folder where output should be saved"),options=options)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        #make empty lists
        measurements= ['Image','Animal_ID','Altitude','Focal Length','PixD','Notes',bl_name, 'OLp','DateFlight']
        names = ['Image','Animal_ID','Altitude','Focal Length','PixD','Notes']
        csvs = []

        #set up list of csvs to loop through
        files = os.listdir(GUIfold) #list all folders
        print(files)
        for i in files:
            fx = os.path.join(GUIfold,i) #set up full path of folder
            print(fx)
            f = os.path.isdir(fx) #check if it's a folder
            print(f)
            if f == True: #if it is a folder
                filesx = os.listdir(fx)
                print(filesx)
                for j in filesx:
                    fy = os.path.join(fx,j)
                    print(fy)
                    f1 = os.path.isdir(fy)
                    if f1 == True:
                        clist = os.listdir(fy) #list the contents of the folder (this is the individual folder)
                        for ii in clist:
                            if ii.endswith('.csv'): #if its a csv
                                iii = os.path.join(fy,ii) #set up full file path
                                csvs += [iii] #add to list of csvs

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

            split = os.path.split(os.path.split(f)[0])
            flight = split[1]
            date = os.path.split(split[0])[1]
            dateflight = date + "_" + flight
            mDict['DateFlight'] = dateflight

            aID = df[df[0] == 'Image ID'].loc[:,[1]].values[0] #pull animal id
            aID = aID[0]
            mDict['Animal_ID'] = aID

            image = os.path.split(df[df[0] == 'Image Path'].loc[:,1].values[0])[1] #extract image
            print(image)
            mDict['Image'] = image

            alt = float((df[df[0] == 'Altitude'].loc[:,[1]].values[0])[0]) #extract entered altitude
            mDict['Altitude'] = alt

            focl = float((df[df[0] == 'Focal Length'].loc[:,[1]].values[0])[0]) #extract entered focal length
            mDict['Focal Length'] = focl

            pixd = float((df[df[0] == 'Pixel Dimension'].loc[:,[1]].values[0])[0]) #extract entered pixel dimension
            mDict['PixD'] = pixd

            notes = df[df[0] == 'Notes'].loc[:,[1]].values[0] #extract entered notes
            mDict['Notes'] = notes[0]

            #go into the cvs to look for the measurement values
            dfGUI = df0.truncate(before=idx[0]) #now subset the df so we're just looking at the measurements
            head = dfGUI.iloc[0] #isolate the current header row
            dfGUI.columns = head #make the header the original header
            dfGUI = dfGUI.set_index('Object') #make index column the one named Object

            if bl_name in dfGUI.index:
                x = float(dfGUI.loc[bl_name,'Length (m)'])
                mDict[bl_name] = x
                pixc = (x/pixd)*(focl/alt) #back calculate the pixel count
                mDict['OLp'] = pixc

            df_op = pd.DataFrame(data = mDict,index=[1]) #make dictionary (now filled with the measurements from this one csv) into dataframe
            df_all = pd.concat([df_all,df_op],sort = True)
        print(df_all)
        #ok now we have a dataframe and want to make the linear model
        dfImg = pd.read_csv(img_csv,sep =',')
        dfImg['DateFlight'] = [x + "_" + y for x,y in zip(dfImg['Date'],dfImg['Flight'])]

        #loop through DateFlights, run linear model, predict acurate value for image altitude
        dateflights = set(df_all['DateFlight'])
        dlist = ['Image','Altitude']
        iDict = dict.fromkeys(dlist)
        k = list(iDict.keys())
        df_calib = pd.DataFrame (columns = k)
        for datefl in dateflights:
            df_board = df_all.loc[df_all['DateFlight']==datefl]
            df_image = dfImg.loc[dfImg['DateFlight']==datefl]

            Board = (df_board['Focal Length']*(ob_l/df_board['OLp']))/df_board['PixD'].tolist()

            Alts = df_board['Altitude'].tolist()

            lm = np.polyfit(Alts,Board,1)
            fit = np.poly1d(lm)

            for img, b_alt in zip(df_image['Image'],df_image['Baro_Alt']):
                iDict['Image'] = img
                iDict['Altitude'] = fit(b_alt)

            df_temp = pd.DataFrame(data=iDict,index=[1])
            df_calib = pd.concat([df_calib,df_temp])
        print(df_calib)
        outcsv = os.path.join(saveFold,"board_calibration.csv")
        df_calib.to_csv(outcsv,sep = ',')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
