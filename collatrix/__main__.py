#---------------------------------------------------------------
#gui_collating_alloptions_v5.0.py
#this script collates measurements from individual csv outputs of
#the morphometriX GUI
#the csvs can be saved either all in one folder or within each individual
#animals folder.
#this version includes a safety net that recalculates the measurement using
#accurate altitude and focal lengths that the user must provie in csvs.
# this version uses PyQt5 instead of easygui (used in v2.0)
#created by: Clara Bird (clara.birdferrer#gmail.com), August 2019
#----------------------------------------------------------------

#import modules
import pandas as pd
import numpy as np
import os, sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
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

        #ask how csvs are saved
        items = ('Individual Folders', 'One Folder')
        option, okPressed = QInputDialog.getItem(self, "Option","Saved Where", items, 0, False)
        if okPressed and option:
            print(option)

        #ask if they want safey net
        items = ('yes', 'no')
        safety, okPressed = QInputDialog.getItem(self,"Safety?", "On or Off?",items,0,False)
        if okPressed and safety:
            print(safety)


        #ask if they want body Volume
        items = ('yes','no')
        volchoice, okPressed = QInputDialog.getItem(self, 'Do you want body volume to be calculated? (you have to have measured Total_Length widths)','',items,0,False)
        if okPressed and volchoice:
            print(volchoice)

        if volchoice == 'yes':
            n, okPressed = QInputDialog.getText(self, "What did you name the total length measurement?","Total Length Name:", QLineEdit.Normal, "")
            if okPressed and n != '':
                tl_name= str(n)
                print(tl_name)
            l, okPressed = QInputDialog.getText(self, "Lower Bound","Lower Bound:", QLineEdit.Normal, "")
            if okPressed and l != '':
                lower= int(l)
                print(lower)
            u, okPressed = QInputDialog.getText(self, "Upper Bound","Upper Bound:", QLineEdit.Normal, "")
            if okPressed and u != '':
               upper = int(u)
               print(upper)
            i, okPressed = QInputDialog.getText(self, "Interval","Interval:", QLineEdit.Normal, "")
            if okPressed and i != '':
                interval = int(i)
                print(interval)
        elif volchoice == 'no':
            pass

        #animal id list?
        items = ('yes','no')
        idchoice, okPressed = QInputDialog.getItem(self, "do you want output to only contain certain individuals?",'use animal id list?',items,0,False)
        if idchoice and okPressed:
            print(idchoice)
        if idchoice == 'yes':
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            idsCSV, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;csv files (*.csv)", options=options)
            if idsCSV:
                print(idsCSV)
        elif idchoice == 'no':
            pass

        #ask for name of output
        outname, okPressed = QInputDialog.getText(self, "output name",'name',QLineEdit.Normal,"")

        constants = ['Image ID', 'Image Path', 'Focal Length', 'Altitude', 'Pixel Dimension']

        if safety == 'yes':
            if option == 'Individual Folders':
                INDfold = QFileDialog.getExistingDirectory(None, "folder containing individual folders")
                saveFold = QFileDialog.getExistingDirectory(None,"folder where output should be saved")
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                safe_csv, _ = QFileDialog.getOpenFileName(self,"img list w/ altitudes and focal lengths", "","All Files (*);;csv files (*.csv)", options=options)

                dfList = pd.read_csv(safe_csv,sep = ",")
                #print(dfList)

                #make lists
                measurements = []
                nonPercMeas = []
                csvs = []

                #loop through individual folders and make list of GUI output csvs
                files = os.listdir(INDfold)
                for i in files:
                    fii = os.path.join(INDfold,i)
                    f = os.path.isdir(fii)
                    if f == True:
                        clist = os.listdir(fii)
                        for ii in clist:
                            if ii.endswith('.csv'):
                                iii = os.path.join(fii,ii)
                                csvs += [iii]

                def anydup(l): #we'll use this function later to check for duplicates
                    seen = set()
                    for x in l:
                        if x in seen: return True
                        seen.add(x)
                    return False

                #here we loop through all csvs to extract all the possible measurement names
                for f in csvs:
                    temp=pd.read_csv(f,sep='^',header=None,prefix='X',engine = 'python') #read in csv as one column
                    df0=temp.X0.str.split(',',expand=True) #split rows into columns by delimeter
                    df0 = df0.fillna('') #replace nans by blank space
                    idx = df0.loc[df0[0] == 'Object'].index #find index (row) values of 'Object'
                    df = df0.iloc[idx[0]:].reset_index(drop=True)  #take subset of df starting at first row containing Object
                    head = df.iloc[0] #make list out of names in first row
                    df = df[1:] #take the data less the header row
                    df.columns = head #set the header row as the df header
                    #display(df)

                    wlist = df.iloc[0] #make list of all the width types
                    widths = []
                    for ww in wlist: #loop through widths row to make sure only widths are in list
                        if "Width" in str(ww):
                            widths += [str(ww)]

                    l = df['Object'].tolist() #make list of Object columns aka. names of measurements made
                    l = [x for x in l if pd.isna(x) == False] #eliminate all empty cells
                    l = [x for x in l if x not in constants and x != 'Object'] #elimate all other instances of Object
                    l = [x for x in l if x] #make sure no blank elements in list

                    measurements = measurements + l #add the measurement names to the master list
                    nonPercMeas = nonPercMeas + l #copy of the master list that does not include widths


                    new_header = df.columns[0:2].values.tolist() + df.iloc[0,2:].values.tolist() #merge header with width names
                    df = df[1:] #cut header row off
                    df.columns = new_header #make the updated list the new header

                    df = df.set_index('Object') #set Object column as the index
                    df = df.replace(r'^\s*$', np.nan, regex=True)

                    if anydup(l) == True: #check for any duplicate measurement names, if exists, exit code, print error msg
                        print("please check file {0} for duplicate Objects and remove duplicates".format(f))
                        sys.exit("remove duplicate and run script again")
                    elif anydup(l) == False:
                        print(f)
                        for i in l: #loop through list of measurement types
                            for w in (w for w in widths if w[0].isdigit()): #loop through the widths
                                x = df.loc[i,w] #extract cell value of width of measurement type
                                if pd.isna(x) == False: #if the cell isn't empty
                                    ww = i + "-" + w #combine the names
                                    measurements += [ww] #add this combined name to the master list

                #now we're going to set up a dictionary to fill in with all the measurements
                #that we will eventually turn into a dataframe where the keys are the columns
                rawM = measurements
                measurements += ['Image','Animal_ID','Altitude','Focal Length','PixD','Notes']
                names = ['Image','Animal_ID','Altitude','Focal Length','PixD','Notes']
                mDict = dict.fromkeys(measurements)
                keys = list(mDict.keys())

                df_all = pd.DataFrame(columns = keys)

                rawMM = set(rawM)

                for f in csvs:
                    print(f)
                    #pull the initial values i.e image, ID, alt, focal length
                    temp=pd.read_csv(f,sep='^',header=None,prefix='X',engine = 'python') #import as one column
                    df1=temp.X0.str.split(',',expand=True) #split on comma delimeter
                    df0 = df1.fillna('') #replace nans by blank space
                    idx = df0.loc[df0[0]=='Object'].index #set object column to index
                    df = df0.iloc[:idx[0]].reset_index(drop=True) #subset df to be only top info section

                    aID = os.path.split(os.path.split(f)[0])[1] #extract animal ID
                    mDict['Animal_ID'] = aID
                    #df = df.set_index([0])
                    image = os.path.split(df[df[0] == 'Image Path'].loc[:,1].values[0])[1] #extract image
                    print(image)
                    #print(image)
                    mDict['Image'] = image
                    #print(df)
                    alt = float((df[df[0] == 'Altitude'].loc[:,[1]].values[0])[0]) #extract entered altitude
                    mDict['Altitude'] = alt

                    focl = float((df[df[0] == 'Focal Length'].loc[:,[1]].values[0])[0]) #extract entered focal length
                    mDict['Focal Length'] = focl

                    pixd = float((df[df[0] == 'Pixel Dimension'].loc[:,[1]].values[0])[0]) #extract entered pixel dimension
                    mDict['PixD'] = pixd

                    notes = df[df[0] == 'Notes'].loc[:,[1]].values[0]
                    mDict['Notes'] = notes[0]


                    #get the true values of focal length and altitude to use when recalculating
                    df_L = dfList.groupby('Image').first().reset_index()
                    alt_act = float(df_L[df_L.Image == image].loc[:,'Altitude'].values[0])
                    foc_act = float(df_L[df_L.Image == image].loc[:,'Focal_Length'].values[0])
                    pixd_act = float(df_L[df_L.Image == image].loc[:,'Pixel_Dimension'].values[0])

                    #go into the cvs to look for the measurement values
                    dfGUI = df0.iloc[idx[0]:].reset_index(drop=True) #now subset the df so we're just looking at the measurements
                    head = dfGUI.iloc[0]
                    dfGUI = dfGUI[1:]
                    dfGUI.columns = head
                    new_headerG = dfGUI.columns[0:2].values.tolist() + dfGUI.iloc[0,2:].values.tolist() #merge header with width names
                    dfGUI = dfGUI[1:] #take the data less the header row
                    dfGUI.columns = new_headerG
                    dfGUI = dfGUI.set_index('Object')

                    for key in keys: #loop through the keys aka future column headers
                        if key in nonPercMeas: #if that key is in the list of measurement types (not widths)
                            if key in dfGUI.index: #if that key (measurement) is in this csv
                                x = float(dfGUI.loc[key,'Length (m)']) #extract the measurement value using location
                                #print(key,x)
                                # now is the time to do the back calculations
                                pixc = (x/pixd)*(focl/alt) #back calculate the pixel count
                                #print(pixc)
                                xx = ((alt_act/foc_act)*pixd_act)*pixc #recalculate using the accurate focal length and altitude
                                #print(xx)
                            else: #if this key is not in the csv
                                xx = np.nan
                            mDict[key] = xx #add the value to the respective key
                        elif "%" in key and key.split("-")[0] in dfGUI.index: #if the key is a width
                            row = key.split("-")[0] #split the name of the measurement
                            col = key.split("-")[1] #to get the row and column indices
                            y = float(dfGUI.loc[row,col]) #to extract the measurement value
                            #recalculate using accurate focal length and altitude
                            pixc = (y/pixd)*(focl/alt) #back calculate the pixel count
                            yy = ((alt_act/foc_act)*pixd_act)*pixc #recalculate using the accurate focal length and altitude
                            mDict[key] = yy
                        elif key not in dfGUI.index and key not in names:
                            mDict[key] = np.nan


                    df_op = pd.DataFrame(data = mDict,index=[1]) #make dictionary into dataframe
                    #df_all = pd.merge(df_all,df_op,on=['Image'])
                    df_all = pd.concat([df_all,df_op],sort = True)

                df_allx = df_all.drop(columns = ['Altitude','Focal Length','PixD']).replace(np.nan,0)
                df_all_cols = df_allx.columns.tolist() #make list of column names
                gby = ['Animal_ID','Image','Notes']
                togroup = [x for x in df_all_cols if x not in gby] #setting up list of columns to be grouped
                #no we group by ID and image just incase multiple images were measured for the same animal
                #this would combine those measurements
                df_all = df_allx.groupby(['Animal_ID','Image'])[togroup].apply(lambda x: x.astype(float).sum()).reset_index()
                df_notes = df_allx.groupby(['Animal_ID','Image'])['Notes'].first().reset_index()
                df_all =df_all.merge(df_notes,on=['Animal_ID','Image'])

                #calculate body volume
                df_all.columns = df_all.columns.str.replace(".00%", ".0%")
                if volchoice == 'yes':
                    body_name = "Body_Vol_{0}%".format(interval)
                    volm = []
                    for x in range(lower,(upper + interval), interval):
                        wname = ww.split("-")[0]
                        xx = "{0}-{1}.0%".format(tl_name,str(x))
                        volm += [xx]
                    print(volm)
                    vlist = []
                    for i in volm:
                        for ii in df_all.columns:
                            if i in ii:
                                vlist += [ii]

                    ids = []
                    vs = []
                    imgs = []
                    for i,j in enumerate(vlist[:-1]):
                        jj = vlist[i+1]
                        #print(df_all[j])
                        for rr, RR, hh,anid,img in zip(df_all[j],df_all[jj], df_all[tl_name],df_all['Animal_ID'],df_all['Image']):
                            ph = float(interval)/float(100)
                            h = float(hh)*ph
                            #print(r)
                            r = float(rr)/float(2)
                            R = float(RR)/float(2)
                            v1 = (float(1)/float(3))*(math.pi)*h*((r**2)+(r*R)+(R**2))
                            #print(v1)
                            ids += [anid]
                            vs += [v1]
                            imgs += [img]

                    d = {'Animal_ID':ids, body_name:vs, 'Image':imgs}
                    df = pd.DataFrame(data = d)

                    cls = df.columns.tolist()
                    grBy = ['Animal_ID','Image']
                    groups = [x for x in cls if x not in grBy]
                    df1 = df.groupby(['Animal_ID','Image'])[groups].apply(lambda x: x.astype(float).sum()).reset_index()

                    df_all1 = pd.merge(df_all,df1,on = ['Animal_ID','Image'])
                elif volchoice == 'no':
                    df_all1 = df_all
                print(df_all1)
                #sort cols
                cols = list(df_all1)
                a = "AaIiTtEeJjRrBbFfWwCcDdGgHhKkLlMmNnOoPpQqSsUuVvXxYyZz" #make your own ordered alphabet
                col = sorted(cols, key=lambda word:[a.index(c) for c in word[0]]) #sort headers based on this alphabet
                df_all1 = df_all1.ix[:,col] #sort columns based on sorted list of column header

                outcsv = os.path.join(saveFold,"{0}_allIDs.csv".format(outname))
                df_all1.to_csv(outcsv,sep = ',')

                if idchoice == 'yes':
                    df_ids = pd.read_csv(idsCSV,sep = ',')
                    idList = df_ids['Animal_ID'].tolist()
                    df_allx = df_all1[df_all1['Animal_ID'].isin(idList)]

                    outidcsv = os.path.join(saveFold,"{0}_IDS.csv".format(outname))
                    df_allx.to_csv(outidcsv,sep = ',')
                elif idchoice == 'no':
                    pass

                print("done, close GUI window to end script")
            elif option == 'One Folder':
                GUIfold = QFileDialog.getExistingDirectory(None, "folder containing GUI outputs")
                saveFold = QFileDialog.getExistingDirectory(None,"folder where output should be saved")
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                safe_csv, _ = QFileDialog.getOpenFileName(self,"img list w/ altitudes and focal lengths", "","All Files (*);;csv files (*.csv)", options=options)

                dfList = pd.read_csv(safe_csv, sep = ",")
                #print(dfList)

                files = os.listdir(GUIfold)
                measurements= []
                nonPercMeas = []

                def anydup(l): #we'll use this function later to check for duplicates
                    seen = set()
                    for x in l:
                        if x in seen: return True
                        seen.add(x)
                    return False

                for f in (f for f in files if f.endswith('.csv')):
                    ff = os.path.join(GUIfold,f) #join csv name to folder file path
                    temp=pd.read_csv(ff,sep='^',header=None,prefix='X',engine = 'python') #read in csv as one column
                    df0=temp.X0.str.split(',',expand=True) #split rows into columns by delimeter
                    df0 = df0.fillna('') #replace nans by blank space
                    idx = df0.loc[df0[0] == 'Object'].index #find index (row) values of 'Object'
                    df = df0.iloc[idx[0]:].reset_index(drop=True)  #take subset of df starting at first row containing Object
                    head = df.iloc[0] #make list out of names in first row
                    df = df[1:] #take the data less the header row
                    df.columns = head #set the header row as the df header
                    #display(df)

                    wlist = df.iloc[0] #make list of all the width types
                    widths = []
                    for ww in wlist: #loop through widths row to make sure only widths are in list
                        if "Width" in str(ww):
                            widths += [str(ww)]

                    l = df['Object'].tolist() #make list of Object columns aka. names of measurements made
                    l = [x for x in l if pd.isna(x) == False] #eliminate all empty cells
                    l = [x for x in l if x not in constants and x != 'Object'] #elimate all other instances of Object
                    l = [x for x in l if x] #make sure no blank elements in list

                    measurements = measurements + l #add the measurement names to the master list
                    nonPercMeas = nonPercMeas + l #copy of the master list that does not include widths


                    new_header = df.columns[0:2].values.tolist() + df.iloc[0,2:].values.tolist() #merge header with width names
                    df = df[1:] #cut header row off
                    df.columns = new_header #make the updated list the new header

                    df = df.set_index('Object') #set Object column as the index

                    if anydup(l) == True: #check for any duplicate measurement names, if exists, exit code, print error msg
                        print("please check file {0} for duplicate Objects and remove duplicates".format(f))
                        sys.exit("remove duplicate and run script again")
                    elif anydup(l) == False:
                        print(f)
                        for i in l: #loop through list of measurement types
                            for w in (w for w in widths if w[0].isdigit()): #loop through the widths
                                x = df.loc[i,w] #extract cell value of width of measurement type
                                if pd.isna(x) == False: #if the cell isn't empty
                                    ww = i + "-" + w #combine the names
                                    measurements += [ww] #add this combined name to the master list


                #now we're going to set up a dictionary to fill in with all the measurements
                #that we will eventually turn into a dataframe where the keys are the columns
                rawM = measurements
                measurements += ['Image','Animal_ID','Altitude','Focal Length','PixD','Notes']
                names = ['Image','Animal_ID','Altitude','Focal Length','PixD','Notes']
                mDict = dict.fromkeys(measurements)
                keys = list(mDict.keys())

                df_all = pd.DataFrame(columns = keys)

                rawMM = set(rawM)


                for f in (f for f in files if f.endswith('.csv')):
                    print(f)
                    fil = os.path.join(GUIfold,f)
                    #pull the initial values i.e image, ID, alt, focal length
                    temp=pd.read_csv(fil,sep='^',header=None,prefix='X',engine='python') #import as one column
                    df1=temp.X0.str.split(',',expand=True) #split on comma delimeter
                    df0 = df1.fillna('') #replace nans with blank space
                    idx = df0.loc[df0[0]=='Object'].index #set object column to index
                    df = df0.iloc[:idx[0]].reset_index(drop=True) #subset df to be only top info section

                    image = os.path.split((df[df[0] == 'Image Path'].loc[:,[1]].values[0])[0])[1] #extract image
                    print(image)
                    mDict['Image'] = image
                    #print(df)
                    aID = (df[df[0] == 'Image ID'].loc[:,[1]].values[0])[0] #extract animal ID
                    mDict['Animal_ID'] = aID

                    alt =  float((df[df[0] == 'Altitude'].loc[:,[1]].values[0])[0]) #extract entered altitude
                    mDict['Altitude'] = alt

                    focl = float((df[df[0] == 'Focal Length'].loc[:,[1]].values[0])[0]) #extract entered focal length
                    mDict['Focal Length'] = focl

                    pixd =  float((df[df[0] == 'Pixel Dimension'].loc[:,[1]].values[0])[0]) #extract entered pixel dimension
                    mDict['PixD'] = pixd

                    notes = df[df[0] == 'Notes'].loc[:,[1]].values[0]
                    mDict['Notes'] = notes[0]

                    #get the true values of focal length and altitude to use when recalculating
                    df_L = dfList.groupby('Image').first().reset_index()
                    alt_act = float(df_L[df_L.Image == image].loc[:,'Altitude'].values[0])
                    foc_act = float(df_L[df_L.Image == image].loc[:,'Focal_Length'].values[0])
                    pixd_act = float(df_L[df_L.Image == image].loc[:,'Pixel_Dimension'].values[0])

                    #go into the cvs to look for the values
                    dfGUI = df0.iloc[idx[0]:].reset_index(drop=True) #now subset the df so we're just looking at the measurements
                    head = dfGUI.iloc[0]
                    dfGUI = dfGUI[1:]
                    dfGUI.columns = head
                    new_headerG = dfGUI.columns[0:2].values.tolist() + dfGUI.iloc[0,2:].values.tolist() #merge header with width names
                    dfGUI = dfGUI[1:] #take the data less the header row
                    dfGUI.columns = new_headerG
                    dfGUI = dfGUI.set_index('Object')
                    df = df.replace(r'^\s*$', np.nan, regex=True)

                    for key in keys: #loop through the keys aka future column headers
                        if key in nonPercMeas: #if that key is in the list of measurement types (not widths)
                            if key in dfGUI.index: #if that key (measurement) is in this csv
                                x = float(dfGUI.loc[key,'Length (m)']) #extract the measurement value using location
                                # now is the time to do the back calculations
                                pixc = (x/pixd)*(focl/alt) #back calculate the pixel count
                                xx = ((alt_act/foc_act)*pixd_act)*pixc #recalculate using the accurate focal length and altitude
                                #just the thing for the time we had to divide by 2 for a few images
                            else: #if this key is not in the csv
                                xx = np.nan
                            mDict[key] = xx #add the value to the respective key
                        elif "%" in key and key.split("-")[0] in dfGUI.index: #if the key is a width
                            row = key.split("-")[0] #split the name of the measurement
                            col = key.split("-")[1] #to get the row and column indices
                            y = float(dfGUI.loc[row,col]) #to extract the measurement value
                            #recalculate using accurate focal length and altitude
                            pixc = (y/pixd)*(focl/alt) #back calculate the pixel count
                            yy = ((alt_act/foc_act)*pixd_act)*pixc #recalculate using the accurate focal length and altitude
                            mDict[key] = yy
                        elif key not in dfGUI.index and key not in names:
                            mDict[key] = np.nan

                    df_op = pd.DataFrame(data = mDict,index=[1]) #make dictionary into dataframe
                    df_all = pd.concat([df_all,df_op],sort = True)

                df_allx = df_all.drop(columns = ['Altitude','Focal Length','PixD']).replace(np.nan,0)
                df_all_cols = df_allx.columns.tolist() #make list of column names
                gby = ['Animal_ID','Image','Notes']
                togroup = [x for x in df_all_cols if x not in gby] #setting up list of columns to be grouped
                #no we group by ID and image just incase multiple images were measured for the same animal
                #this would combine those measurements
                df_all = df_allx.groupby(['Animal_ID','Image'])[togroup].apply(lambda x: x.astype(float).sum()).reset_index()
                df_notes = df_allx.groupby(['Animal_ID','Image'])['Notes'].first().reset_index()
                df_all =df_all.merge(df_notes,on=['Animal_ID','Image'])


                #calculate body volume
                df_all.columns = df_all.columns.str.replace(".00%", ".0%")

                if volchoice == 'yes':
                    body_name = "Body_Vol_{0}%".format(interval)
                    volm = []
                    for x in range(lower,(upper + interval), interval):
                        wname = ww.split("-")[0]
                        xx = "{0}-{1}.0%".format(tl_name,str(x))
                        volm += [xx]

                    vlist = []
                    for i in volm:
                        #print(i)
                        for ii in df_all.columns:
                            #print(ii)
                            if i in ii:
                                vlist += [ii]

                    ids = []
                    vs = []
                    imgs = []
                    for i,j in enumerate(vlist[:-1]):
                        jj = vlist[i+1]
                        #print(df_all[j])
                        for rr, RR, hh,anid,img in zip(df_all[j],df_all[jj], df_all[tl_name],df_all['Animal_ID'],df_all['Image']):
                            ph = float(interval)/float(100)
                            h = float(hh)*ph
                            #print(r)
                            r = float(rr)/float(2)
                            R = float(RR)/float(2)
                            v1 = (float(1)/float(3))*(math.pi)*h*((r**2)+(r*R)+(R**2))
                            #print(v1)
                            ids += [anid]
                            vs += [v1]
                            imgs += [img]

                    d = {'Animal_ID':ids, body_name:vs, 'Image':imgs}
                    df = pd.DataFrame(data = d)

                    cls = df.columns.tolist()
                    grBy = ['Animal_ID','Image']
                    groups = [x for x in cls if x not in grBy]
                    df1 = df.groupby(['Animal_ID','Image'])[groups].apply(lambda x: x.astype(float).sum()).reset_index()
                    df_all1 = pd.merge(df_all,df1,on = ['Animal_ID','Image'])

                elif volchoice == 'no':
                    df_all1 = df_all
                print(df_all1)
                #sort cols
                cols = list(df_all1)
                a = "AaIiTtEeJjRrBbFfWwCcDdGgHhKkLlMmNnOoPpQqSsUuVvXxYyZz" #make your own ordered alphabet
                col = sorted(cols, key=lambda word:[a.index(c) for c in word[0]]) #sort headers based on this alphabet
                df_all1 = df_all1.ix[:,col] #sort columns based on sorted list of column header



                outcsv = os.path.join(saveFold,"{0}_allIDs.csv".format(outname))
                df_all1.to_csv(outcsv,sep = ',')

                if idchoice == 'yes':
                    df_ids = pd.read_csv(idsCSV,sep = ',')
                    idList = df_ids['Animal_ID'].tolist()
                    df_allx = df_all1[df_all1['Animal_ID'].isin(idList)]

                    outidcsv = os.path.join(saveFold,"{0}_IDS.csv".format(outname))
                    df_allx.to_csv(outidcsv,sep = ',')
                elif idchoice == 'no':
                    pass
                print("done, close GUI window to end script")

        elif safety == 'no':
            if option == 'Individual Folders':
                INDfold = QFileDialog.getExistingDirectory(None, "folder containing individual folders")
                saveFold = QFileDialog.getExistingDirectory(None,"folder where output should be saved")
                #make lists
                measurements = []
                nonPercMeas = []
                csvs = []

                #loop through individual folders and make list of GUI output csvs
                files = os.listdir(INDfold)
                for i in files:
                    fii = os.path.join(INDfold,i)
                    f = os.path.isdir(fii)
                    if f == True:
                        clist = os.listdir(fii)
                        for ii in clist:
                            if ii.endswith('.csv'):
                                iii = os.path.join(fii,ii)
                                csvs += [iii]

                def anydup(l): #we'll use this function later to check for duplicates
                    seen = set()
                    for x in l:
                        if x in seen: return True
                        seen.add(x)
                    return False

                #here we loop through all csvs to extract all the possible measurement names
                for f in csvs:
                    temp=pd.read_csv(f,sep='^',header=None,prefix='X',engine = 'python') #read in csv as one column
                    df0=temp.X0.str.split(',',expand=True) #split rows into columns by delimeter
                    df0 = df0.fillna('') #replace nans by blank space
                    idx = df0.loc[df0[0] == 'Object'].index #find index (row) values of 'Object'
                    df = df0.iloc[idx[0]:].reset_index(drop=True)  #take subset of df starting at first row containing Object
                    head = df.iloc[0] #make list out of names in first row
                    df = df[1:] #take the data less the header row
                    df.columns = head #set the header row as the df header
                    #display(df)

                    wlist = df.iloc[0] #make list of all the width types
                    widths = []
                    for ww in wlist: #loop through widths row to make sure only widths are in list
                        if "Width" in str(ww):
                            widths += [str(ww)]

                    l = df['Object'].tolist() #make list of Object columns aka. names of measurements made
                    l = [x for x in l if pd.isna(x) == False] #eliminate all empty cells
                    l = [x for x in l if x not in constants and x != 'Object'] #elimate all other instances of Object
                    l = [x for x in l if x] #make sure no blank elements in list

                    measurements = measurements + l #add the measurement names to the master list
                    nonPercMeas = nonPercMeas + l #copy of the master list that does not include widths


                    new_header = df.columns[0:2].values.tolist() + df.iloc[0,2:].values.tolist() #merge header with width names
                    df = df[1:] #cut header row off
                    df.columns = new_header #make the updated list the new header

                    df = df.set_index('Object') #set Object column as the index
                    df = df.replace(r'^\s*$', np.nan, regex=True)

                    if anydup(l) == True: #check for any duplicate measurement names, if exists, exit code, print error msg
                        print("please check file {0} for duplicate Objects and remove duplicates".format(f))
                        sys.exit("remove duplicate and run script again")
                    elif anydup(l) == False:
                        print(f)
                        for i in l: #loop through list of measurement types
                            for w in (w for w in widths if w[0].isdigit()): #loop through the widths
                                x = df.loc[i,w] #extract cell value of width of measurement type
                                if pd.isna(x) == False: #if the cell isn't empty
                                    ww = i + "-" + w #combine the names
                                    measurements += [ww] #add this combined name to the master list

                #now we're going to set up a dictionary to fill in with all the measurements
                #that we will eventually turn into a dataframe where the keys are the columns
                rawM = measurements #making a copy of the measurement list
                measurements += ['Image','Animal_ID','Notes'] #add key elements to measurement list (all for dict)
                names = ['Image','Animal_ID','Notes'] #make list of the non measurement elements that will go in final table
                mDict = dict.fromkeys(measurements) #make empty dictionary with measurement names as keys
                keys = list(mDict.keys()) #make list of keys from the dictionary we just made

                df_all = pd.DataFrame(columns = keys) #make empty dataframe with each key as a column hedaer

                rawMM = set(rawM) #make set out of rawM measurement list

                for f in csvs: #loop through the csvs again
                    print(f)
                    #pull the initial values i.e image, ID, alt, focal length
                    temp=pd.read_csv(f,sep='^',header=None,prefix='X',engine = 'python') #import as one column
                    df1=temp.X0.str.split(',',expand=True) #split on comma delimeter
                    df0 = df1.fillna('')
                    idx = df0.loc[df0[0]=='Object'].index #set object column to index
                    df = df0.iloc[:idx[0]].reset_index(drop=True) #subset df to be only top info section

                    image = os.path.split((df[df[0] == 'Image Path'].loc[:,[1]].values[0])[0])[1] #pull image name
                    print(image)
                    mDict['Image'] = image #add image name to dictionary
                    aID = os.path.split(os.path.split(f)[0])[1] #pull animal id
                    mDict['Animal_ID'] = aID[0] #fill dictionary
                    notes = df[df[0] == 'Notes'].loc[:,[1]].values[0]
                    mDict['Notes'] = notes[0]

                    #go into the cvs to look for the measurement values
                    dfGUI = df0.iloc[idx[0]:].reset_index(drop=True) #now subset the df so we're just looking at the measurements
                    head = dfGUI.iloc[0]
                    dfGUI = dfGUI[1:]
                    dfGUI.columns = head
                    new_headerG = dfGUI.columns[0:2].values.tolist() + dfGUI.iloc[0,2:].values.tolist() #merge header with width names
                    dfGUI = dfGUI[1:] #take the data less the header row
                    dfGUI.columns = new_headerG
                    dfGUI = dfGUI.set_index('Object')

                    for key in keys: #loop through the keys aka future column headers
                        if key in nonPercMeas: #if that key is in the list of measurement types (not widths)
                            if key in dfGUI.index.tolist(): #if that key (measurement) is in this csv
                                x = float(dfGUI.loc[key,'Length (m)']) #extract the measurement value using location
                            else: #if this key is not in the csv
                                x = np.nan
                            mDict[key] = x #add the value to the respective key
                        elif "%" in key and key.split("-")[0] in dfGUI.index: #if the key is a width
                            row = key.split("-")[0] #split the name of the measurement
                            col = key.split("-")[1] #to get the row and column indices
                            y = dfGUI.loc[row,col] #to extract the measurement value
                            mDict[key] = y
                        elif key not in dfGUI.index and key not in names:
                            mDict[key] = np.nan

                    df_op = pd.DataFrame(data = mDict,index=[1]) #make dictionary into dataframe
                    df_all = pd.concat([df_all,df_op],sort = True) #concatenate the df from the one csv to the master csv

                df_allx = df_all.replace(np.nan,0) #replace all nans with 0s
                df_all_cols = df_allx.columns.tolist() #make list of column names
                gby = ['Animal_ID','Image','Notes']
                togroup = [x for x in df_all_cols if x not in gby] #setting up list of columns to be grouped
                #no we group by ID and image just incase multiple images were measured for the same animal
                #this would combine those measurements
                df_all = df_allx.groupby(['Animal_ID','Image'])[togroup].apply(lambda x: x.astype(float).sum()).reset_index()
                df_notes = df_allx.groupby(['Animal_ID','Image'])['Notes'].first().reset_index()
                df_all =df_all.merge(df_notes,on=['Animal_ID','Image'])

                #calculate body volume
                df_all.columns = df_all.columns.str.replace(".00%", ".0%")
                if volchoice == 'yes':
                    body_name = "Body_Vol_{0}%".format(interval) #name of body volume column will use interval amount
                    volm = [] #make empty list of widths
                    for x in range(lower,(upper + interval), interval): #loop through range of widths
                        wname = ww.split("-")[0]
                        xx = "{0}-{1}.0%".format(tl_name,str(x))
                        volm += [xx]

                    vlist = []
                    for i in volm:
                        for ii in df_all.columns:
                            if i in ii:
                                vlist += [ii]

                    ids = []
                    vs = []
                    imgs = []
                    for i,j in enumerate(vlist[:-1]):
                        jj = vlist[i+1]
                        #calculate volume
                        for rr, RR, hh,anid,img in zip(df_all[j],df_all[jj], df_all[tl_name],df_all['Animal_ID'],df_all['Image']):
                            ph = float(interval)/float(100)
                            h = float(hh)*ph
                            r = float(rr)/float(2)
                            R = float(RR)/float(2)
                            v1 = (float(1)/float(3))*(math.pi)*h*((r**2)+(r*R)+(R**2))
                            ids += [anid]
                            vs += [v1]
                            imgs += [img]

                    d = {'Animal_ID':ids, body_name:vs, 'Image':imgs} #make dataframe of id and body volume
                    df = pd.DataFrame(data = d)

                    cls = df.columns.tolist()
                    grBy = ['Animal_ID','Image']
                    groups = [x for x in cls if x not in grBy]
                    df1 = df.groupby(['Animal_ID','Image'])[groups].apply(lambda x: x.astype(float).sum()).reset_index()

                    df_all1 = pd.merge(df_all,df1,on = ['Animal_ID','Image'])
                elif volchoice == 'no':
                    df_all1 = df_all
                #sort cols
                cols = list(df_all1)
                a = "AaIiTtEeJjRrBbFfWwCcDdGgHhKkLlMmNnOoPpQqSsUuVvXxYyZz" #make your own ordered alphabet
                col = sorted(cols, key=lambda word:[a.index(c) for c in word[0]]) #sort headers based on this alphabet
                df_all1 = df_all1.ix[:,col] #sort columns based on sorted list of column header
                print(df_all1)

                outcsv = os.path.join(saveFold,"{0}_allIDs.csv".format(outname))
                df_all1.to_csv(outcsv,sep = ',')

                if idchoice == 'yes':
                    df_ids = pd.read_csv(idsCSV,sep = ',')
                    idList = df_ids['Animal_ID'].tolist()
                    df_allx = df_all1[df_all1['Animal_ID'].isin(idList)]

                    outidcsv = os.path.join(saveFold,"{0}_IDS.csv".format(outname))
                    df_allx.to_csv(outidcsv,sep = ',')
                elif idchoice == 'no':
                    pass

                print("done, close GUI window to end script")
            elif option == 'One Folder':
                GUIfold = QFileDialog.getExistingDirectory(None, "folder containing GUI outputs")
                saveFold = QFileDialog.getExistingDirectory(None,"folder where output should be saved")
                files = os.listdir(GUIfold)
                measurements= []
                nonPercMeas = []

                def anydup(l): #we'll use this function later to check for duplicates
                    seen = set()
                    for x in l:
                        if x in seen: return True
                        seen.add(x)
                    return False

                for f in (f for f in files if f.endswith('.csv')):
                    ff = os.path.join(GUIfold,f) #join csv name to folder file path
                    temp=pd.read_csv(ff,sep='^',header=None,prefix='X',engine = 'python') #read in csv as one column
                    df0=temp.X0.str.split(',',expand=True) #split rows into columns by delimeter
                    df0 = df0.fillna('') #replace nans by blank space
                    idx = df0.loc[df0[0] == 'Object'].index #find index (row) values of 'Object'
                    df = df0.iloc[idx[0]:].reset_index(drop=True)  #take subset of df starting at first row containing Object
                    head = df.iloc[0] #make list out of names in first row
                    df = df[1:] #take the data less the header row
                    df.columns = head #set the header row as the df header
                    #display(df)

                    wlist = df.iloc[0] #make list of all the width types
                    widths = []
                    for ww in wlist: #loop through widths row to make sure only widths are in list
                        if "Width" in str(ww):
                            widths += [str(ww)]

                    l = df['Object'].tolist() #make list of Object columns aka. names of measurements made
                    l = [x for x in l if pd.isna(x) == False] #eliminate all empty cells
                    l = [x for x in l if x not in constants and x != 'Object'] #elimate all other instances of Object
                    l = [x for x in l if x] #make sure no blank elements in list

                    measurements = measurements + l #add the measurement names to the master list
                    nonPercMeas = nonPercMeas + l #copy of the master list that does not include widths


                    new_header = df.columns[0:2].values.tolist() + df.iloc[0,2:].values.tolist() #merge header with width names
                    df = df[1:] #cut header row off
                    df.columns = new_header #make the updated list the new header

                    df = df.set_index('Object') #set Object column as the index
                    df = df.replace(r'^\s*$', np.nan, regex=True)

                    if anydup(l) == True: #check for any duplicate measurement names, if exists, exit code, print error msg
                        print("please check file {0} for duplicate Objects and remove duplicates".format(f))
                        sys.exit("remove duplicate and run script again")
                    elif anydup(l) == False:
                        print(f)
                        for i in l: #loop through list of measurement types
                            for w in (w for w in widths if w[0].isdigit()): #loop through the widths
                                x = df.loc[i,w] #extract cell value of width of measurement type
                                if pd.isna(x) == False: #if the cell isn't empty
                                    ww = i + "-" + w #combine the names
                                    measurements += [ww] #add this combined name to the master list

                #now we're going to set up a dictionary to fill in with all the measurements
                #that we will eventually turn into a dataframe where the keys are the columns
                rawM = measurements #making a copy of the measurement list
                measurements += ['Image','Animal_ID','Notes'] #add key elements to measurement list (all for dict)
                names = ['Image','Animal_ID','Notes'] #make list of the non measurement elements that will go in final table
                mDict = dict.fromkeys(measurements) #make empty dictionary with measurement names as keys
                keys = list(mDict.keys()) #make list of keys from the dictionary we just made

                df_all = pd.DataFrame(columns = keys) #make empty dataframe with each key as a column hedaer

                rawMM = set(rawM) #make set out of rawM measurement list

                for f in (f for f in files if f.endswith('.csv')): #loop through the csvs again
                    print(f)
                    fil = os.path.join(GUIfold,f)
                    #pull the initial values i.e image, ID, alt, focal length
                    temp=pd.read_csv(fil,sep='^',header=None,prefix='X',engine='python') #import as one column
                    df0=temp.X0.str.split(',',expand=True) #split on comma delimeter
                    idx = df0.loc[df0[0]=='Object'].index #set object column to index
                    df = df0.iloc[:idx[0]].reset_index(drop=True) #subset df to be only top info section

                    image = os.path.split((df[df[0] == 'Image Path'].loc[:,[1]].values[0])[0])[1] #pull image name
                    print(image)
                    mDict['Image'] = image #add image name to dictionary
                    aID = df[df[0] == 'Image ID'].loc[:,[1]].values[0] #pull animal id
                    mDict['Animal_ID'] = aID[0] #fill dictionary
                    notes = df[df[0] == 'Notes'].loc[:,[1]].values[0]
                    mDict['Notes'] = notes[0]

                    #go into the cvs to look for the measurement values
                    dfGUI = df0.iloc[idx[0]:].reset_index(drop=True) #now subset the df so we're just looking at the measurements
                    head = dfGUI.iloc[0]
                    dfGUI = dfGUI[1:]
                    dfGUI.columns = head
                    new_headerG = dfGUI.columns[0:2].values.tolist() + dfGUI.iloc[0,2:].values.tolist() #merge header with width names
                    dfGUI = dfGUI[1:] #take the data less the header row
                    dfGUI.columns = new_headerG
                    dfGUI = dfGUI.set_index('Object')

                    for key in keys: #loop through the keys aka future column headers
                        if key in nonPercMeas: #if that key is in the list of measurement types (not widths)
                            if key in dfGUI.index.tolist(): #if that key (measurement) is in this csv
                                x = float(dfGUI.loc[key,'Length (m)']) #extract the measurement value using location
                            else: #if this key is not in the csv
                                x = np.nan
                            mDict[key] = x #add the value to the respective key
                        elif "%" in key and key.split("-")[0] in dfGUI.index: #if the key is a width
                            row = key.split("-")[0] #split the name of the measurement
                            col = key.split("-")[1] #to get the row and column indices
                            y = dfGUI.loc[row,col] #to extract the measurement value
                            mDict[key] = y
                        elif key not in dfGUI.index and key not in names:
                            mDict[key] = np.nan

                    df_op = pd.DataFrame(data = mDict,index=[1]) #make dictionary into dataframe
                    df_all = pd.concat([df_all,df_op],sort = True) #concatenate the df from the one csv to the master csv

                df_allx = df_all.replace(np.nan,0) #replace all nans with 0s
                df_all_cols = df_allx.columns.tolist() #make list of column names
                gby = ['Animal_ID','Image','Notes']
                togroup = [x for x in df_all_cols if x not in gby] #setting up list of columns to be grouped
                #now we group by ID and image just incase multiple images were measured for the same animal
                #this would combine those measurements
                df_all = df_allx.groupby(['Animal_ID','Image'])[togroup].apply(lambda x: x.astype(float).sum()).reset_index()
                df_notes = df_allx.groupby(['Animal_ID','Image'])['Notes'].first().reset_index()
                df_all =df_all.merge(df_notes,on=['Animal_ID','Image'])

                #calculate body volume
                df_all.columns = df_all.columns.str.replace(".00%", ".0%")
                if volchoice == 'yes':
                    body_name = "Body_Vol_{0}%".format(interval) #name of body volume column will use interval amount
                    volm = [] #make empty list of widths
                    for x in range(lower,(upper + interval), interval): #loop through range of widths
                        wname = ww.split("-")[0]
                        xx = "{0}-{1}.0%".format(tl_name,str(x))
                        volm += [xx]

                    vlist = []
                    for i in volm:
                        for ii in df_all.columns:
                            if i in ii:
                                vlist += [ii]

                    ids = []
                    vs = []
                    imgs = []
                    for i,j in enumerate(vlist[:-1]):
                        jj = vlist[i+1]
                        #calculate volume
                        for rr, RR, hh,anid,img in zip(df_all[j],df_all[jj], df_all[tl_name],df_all['Animal_ID'],df_all['Image']):
                            ph = float(interval)/float(100)
                            h = float(hh)*ph
                            r = float(rr)/float(2)
                            R = float(RR)/float(2)
                            v1 = (float(1)/float(3))*(math.pi)*h*((r**2)+(r*R)+(R**2))
                            ids += [anid]
                            vs += [v1]
                            imgs += [img]

                    d = {'Animal_ID':ids, body_name:vs, 'Image':imgs} #make dataframe of id and body volume
                    df = pd.DataFrame(data = d)

                    cls = df.columns.tolist()
                    grBy = ['Animal_ID','Image']
                    groups = [x for x in cls if x not in grBy]
                    df1 = df.groupby(['Animal_ID','Image'])[groups].apply(lambda x: x.astype(float).sum()).reset_index()

                    df_all1 = pd.merge(df_all,df1,on = ['Animal_ID','Image'])
                elif volchoice == 'no':
                    df_all1 = df_all
                #sort cols
                cols = list(df_all1)
                a = "AaIiTtEeJjRrBbFfWwCcDdGgHhKkLlMmNnOoPpQqSsUuVvXxYyZz" #make your own ordered alphabet
                col = sorted(cols, key=lambda word:[a.index(c) for c in word[0]]) #sort headers based on this alphabet
                df_all1 = df_all1.ix[:,col] #sort columns based on sorted list of column header
                print(df_all1)

                outcsv = os.path.join(saveFold,"{0}_allIDs.csv".format(outname))
                df_all1.to_csv(outcsv,sep = ',')

                if idchoice == 'yes':
                    df_ids = pd.read_csv(idsCSV,sep = ',')
                    idList = df_ids['Animal_ID'].tolist()
                    df_allx = df_all1[df_all1['Animal_ID'].isin(idList)]

                    outidcsv = os.path.join(saveFold,"{0}_IDS.csv".format(outname))
                    df_allx.to_csv(outidcsv,sep = ',')
                elif idchoice == 'no':
                    pass

                print("done, close GUI window to end script")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
