#############################################################
#collatrix_functions.py
#this script contains the functions used in all collatrix code
#created by Clara Bird (clara.birdferrer@gmail.com), October 2020
##############################################################

#import modules
import pandas as pd
import numpy as np
import os, sys

#duplicate check function
def anydup(l): #we'll use this function later to check for duplicates
    seen = set()
    for x in l:
        if x in seen: return True
        seen.add(x)
    return False

# function that reads in csv as one column, then splits
def readfile(f):
    temp=pd.read_csv(f,sep='^',header=None,prefix='X',engine = 'python',quoting=3, na_values = ['""','"']) #read in csv as one column
    df00=temp.X0.str.split(',',expand=True) #split rows into columns by delimeter
    df00 = df00.replace("",np.nan)
    df0 = df00.dropna(how='all',axis = 'rows').reset_index(drop=True)
    df0 = df0.fillna('') #replace nans by blank space
    return df0

# function that resets header
def fheader(df):
    head = df.iloc[0] #make list out of names in first row
    df = df[1:] #take the data less the header row
    df.columns = head #set the header row as the df header
    return(df)

#this is the function that does the collating
def collate(csvs,constants,measurements,nonPercMeas,df_L,safety,anFold):
    for f in csvs:
        print(f)
        df0 = readfile(f)
        idx = df0.loc[df0[0] == 'Object'].index #find index (row) values of 'Object'
        df = df0.truncate(before=idx[0]) #take subset of df starting at first row containing Object
        df = fheader(df)

        #make list of Length measurements
        l = df['Object'].tolist() #make list of Object columns aka. names of measurements made
        l = [x for x in l if pd.isna(x) == False] #eliminate all empty cells
        l = [x for x in l if x not in constants and x != 'Object'] #elimate all other instances of Object
        l = [x for x in l if x] #make sure no blank elements in list

        measurements = measurements + l #add the measurement names to the master list
        nonPercMeas = nonPercMeas + l #copy of the master list that does not include widths

        #make list of Width measurements
        iwx = df.loc[df['Widths (%)'].str.contains("Width")].index.tolist()

        for ix,iw in enumerate(iwx):
            if ix +1 < len(iwx):
                iw1 = iwx[ix+1]-1
            else:
                iw1 = len(df0)
            dfw = df.truncate(before=iw,after=iw1)
            head = dfw.iloc[0] #make list out of names in first row
            dfw = dfw[1:] #take the data less the header row
            dfw.columns = head #set the header row as the df header

            dfw = dfw.set_index(dfw.iloc[:,0]) #set Object column as the index
            dfw = dfw.replace(r'^\s*$', np.nan, regex=True) #replace blank space with nan

            widths = dfw.columns.tolist()
            widths = [x for x in widths if x != ""]

            if anydup(l) == True: #check for any duplicate measurement names, if exists, exit code, print error msg
                print("please check file {0} for duplicate Objects and remove duplicates".format(f))
                sys.exit("remove duplicate and run script again")
            elif anydup(l) == False:
                for i in l: #loop through list of measurement types
                    if i in dfw.index:
                        for w in (w for w in widths if w[0].isdigit()): #loop through the widths
                            x = dfw.loc[i,w] #extract cell value of width of measurement type
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

    #now make list and dictionary for pixel count dataframe
    measurements_pixc = ["{0}.PixCount".format(x) if x not in names else x for x in measurements]
    mDict_pixc = dict.fromkeys(measurements_pixc)
    keys_pixc = list(mDict_pixc.keys())
    #make an empty dataframe with the headers being the measurement types/info to pull
    df_all = pd.DataFrame(columns = keys)
    df_all_pixc = pd.DataFrame(columns = keys_pixc)

    rawMM = set(rawM) #get unique list of measurements

    for f in csvs:
        df0 = readfile(f)
        idx = df0.loc[df0[0]=='Object'].index #set object column to index
        df = df0.truncate(after=idx[0]) #subset df to be only top info section

        if anFold == 'yes':
            aID = os.path.split(os.path.split(f)[0])[1] #extract animal ID
        elif anFold == 'no':
            aID = df[df[0] == 'Image ID'].loc[:,[1]].values[0] #pull animal id
            aID = aID[0]
        mDict['Animal_ID'] = aID; mDict_pixc['Animal_ID'] = aID

        image = os.path.split(df[df[0] == 'Image Path'].loc[:,1].values[0])[1] #extract image
        print(image)
        mDict['Image'] = image; mDict_pixc['Image'] = image

        alt = float((df[df[0] == 'Altitude'].loc[:,[1]].values[0])[0]) #extract entered altitude
        mDict['Altitude'] = alt; mDict_pixc['Altitude'] = alt

        focl = float((df[df[0] == 'Focal Length'].loc[:,[1]].values[0])[0]) #extract entered focal length
        mDict['Focal Length'] = focl; mDict_pixc['Focal Length'] = focl

        pixd = float((df[df[0] == 'Pixel Dimension'].loc[:,[1]].values[0])[0]) #extract entered pixel dimension
        mDict['PixD'] = pixd; mDict_pixc['PixD'] = pixd

        notes = df[df[0] == 'Notes'].loc[:,[1]].values[0] #extract entered notes
        mDict['Notes'] = notes[0]; mDict_pixc['Notes'] = notes

        if safety == 'yes': #pull the altitude, focal length, and pix d from the safety csv by image name
            alt_act = float(df_L[df_L.Image == image].loc[:,'Altitude'].values[0]) #this says: find row where image = image and pull altitude
            foc_act = float(df_L[df_L.Image == image].loc[:,'Focal_Length'].values[0])
            pixd_act = float(df_L[df_L.Image == image].loc[:,'Pixel_Dimension'].values[0])
        else:
            pass

        dfg = df0.truncate(before=idx[0]) #look at part of dataframe that contains measurment data
        dfg = fheader(dfg) #reset the header
        iwx = dfg.loc[dfg['Widths (%)'].str.contains("Width")].index.tolist() #find all rows containing the names of the widths measured
        if len(iwx) == 0: iwx = [0] #if no widths were measured, make index list just 0
        else: iwx = iwx
        dfgg = dfg.set_index(dfg.iloc[:,0]) #make the index the Object column

        for ix,iw in enumerate(iwx): #loop through and make a dataframe for each section of measured widths
            if ix +1 < len(iwx): #if there's an index following the current one
                iw1 = iwx[ix+1]-1 #make the bottom cutoff the next row
            else: #if there is no next width rows
                iw1 = len(df0) #make the bottom cutoff the bottom of the dataframe
            dfw = dfg.truncate(before=iw,after=iw1) #truncate the dataframe to contain just a set of wdiths
            dfGUI = dfw.set_index(dfw.iloc[:,0]) #set Object column as the index
            dfGUI = dfGUI.replace(r'^\s*$', np.nan, regex=True) #replace blank space with nan

            for key in keys: #loop through the keys aka future column headers
                #for the non-width measurements, use full dataframe
                if key in nonPercMeas: #if that key is in the list of measurement types (not widths)
                    if key in dfgg.index: #if the key is in the index of the full dataframe
                        x = float(dfgg.loc[key,'Length (m)']) #extract the measurement value using location
                        pixc = (x/pixd)*(focl/alt) #back calculate the pixel count
                        if safety == 'yes': # now is the time to do the back calculations
                            xx = ((alt_act/foc_act)*pixd_act)*pixc #recalculate using the accurate focal length and altitude
                        elif safety == 'no':
                            xx = x
                    elif key not in dfgg.index: #if this key is not in the csv
                        xx = np.nan
                        pixc = np.nan
                    mDict[key] = xx #add the value to the respective key
                    mDict_pixc["{0}.PixCount".format(key)] = pixc #add pixel count to respecitive key in pixel count dataframe
                #for the width measurements, use the truncated dataframes
                elif "%" in key:
                    if key.split("-")[0] in dfGUI.index: #if the key is a width
                        head = dfGUI.iloc[0] #make list out of names in first row
                        dfG = dfGUI[1:] #take the data less the header row
                        dfG.columns = head #set the header row as the df header
                        row = key.split("-")[0] #split the name of the measurement
                        col = key.split("-")[1] #to get the row and column indices
                        y = float(dfG.loc[row,col]) #to extract the measurement value
                        pixc = (y/pixd)*(focl/alt) #back calculate the pixel count
                        if safety == 'yes': #back calculate and recalculate
                            yy = ((alt_act/foc_act)*pixd_act)*pixc #recalculate using the accurate focal length and altitude
                        elif safety == 'no':
                            yy = y
                    elif key.split("-")[0] not in dfGUI.index:
                        yy = np.nan
                    mDict[key] = yy
                    mDict_pixc["{0}.PixCount".format(key)] = pixc #add pixel count to respecitive key in pixel count dataframe

        df_dict = pd.DataFrame(data = mDict,index=[1]) #make dictionary (now filled with the measurements from this one csv) into dataframe
        df_dict_pixc = pd.DataFrame(data = mDict_pixc,index=[1]) #make dictionary filled with pixel counts of measurements into dataframe

        df_all = pd.concat([df_all,df_dict],sort = True) # add this dataframe to the empty one with all the measurements as headers
        df_all_pixc = pd.concat([df_all_pixc,df_dict_pixc],sort = True) #add this dataframe to the empty one with all the measurements as headers

    df_allx = df_all.drop(columns = ['Altitude','Focal Length','PixD']).replace(np.nan,0) #drop non-measurement cols
    df_allx_pixc = df_all_pixc.drop(columns = ['Altitude','Focal Length','PixD']).replace(np.nan,0) #replace nans with 0 for grouping in final formatting)
    return df_allx, df_allx_pixc

#format the dataframe after collating
def df_formatting(df_allx):
    df_all_cols = df_allx.columns.tolist() #make list of column names
    gby = ['Animal_ID','Image','Notes'] #list of non-numeric columns
    togroup = [x for x in df_all_cols if x not in gby] #setting up list of columns to be grouped

    df_all = df_allx.groupby(['Animal_ID','Image'])[togroup].apply(lambda x: x.astype(float).sum()).reset_index()
    df_notes = df_allx.groupby(['Animal_ID','Image'])['Notes'].first().reset_index()
    df_all =df_all.merge(df_notes,on=['Animal_ID','Image'])

    #sort cols
    cols = list(df_all)
    a = "AaIiTtEeJjRrBbFfWwCcDdGgHhKkLlMmNnOoPpQqSsUuVvXxYyZz" #make your own ordered alphabet
    col = sorted(cols, key=lambda word:[a.index(c) for c in word[0]]) #sort headers based on this alphabet
    df_all1 = df_all.loc[:,col] #sort columns based on sorted list of column header
    df_all1 = df_all1.replace(0,np.nan) #replace the 0s with nans
    return df_all1
