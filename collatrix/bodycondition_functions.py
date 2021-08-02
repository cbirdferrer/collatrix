#############################################################
#bodycondition_functions.py
#this script contains the functions used in body condition code
#created by Clara Bird (clara.birdferrer@gmail.com), October 2020
##############################################################

import pandas as pd
import numpy as np
import os, sys
import math
from scipy.integrate import quad

#body volume function
def body_vol(df_all,tl_name,interval,lower,upper):
    vname = "{0}%".format(interval)
    body_name = "BV_{0}".format(vname) #name of body volume column will use interval amount
    volm = [] #make empty list of widths
    #now fill list with the names of the width columns we want
    volm += ["{0}-{1}.0% Width".format(tl_name,str(x)) for x in range(lower,(upper + interval), interval)]
    #check that those columns are in the dataframe
    colarr = np.array(df_all.columns)
    mask = np.isin(colarr,volm)
    cc = list(colarr[mask])
    vlist = ['index',tl_name]
    vlist.extend(cc)
    ##calculate body col
    df_all_ix = df_all
    df_all_ix['index'] = df_all_ix['Animal_ID']+"*"+df_all_ix['Image'] #make column thats Image and AID combined
    df1 = df_all_ix[vlist] #subset dataframe to just columns we want to use
    df1['spacer'] = np.NaN #add row of nans, we need this for the roll
    dfnp = np.array(df1) #convert dataframe to a numpy array
    ids = dfnp[:,0] #isolate array of just IDs
    tl = dfnp[:,1] #isolate array of just TLs
    r = (dfnp[:,2:])/2 #isolate array of just widths and divide each val by 2 (calculate radius)
    R = (np.roll(r,1,axis=1)) #make second array that's shifted over 1
    p2 = ((r**2)+(r*R)+(R**2)) #calculate the part of the equation that invovles the widths
    p1 = (tl*(interval/100))*(1/3)*math.pi #calculate the part of the equation that invovles TL
    v = p1[:,None]*p2 #calculate the volume of each frustrum
    vsum = np.nansum(v,axis=1) #sum all frustrums per ID
    vol_arr = np.column_stack((ids,vsum)) #make 2D array (df) of IDs and volumes
    dfvx = pd.DataFrame(data=vol_arr,columns=["index",body_name]) #convert array to dataframe
    #make Animal_ID and Image columns again and drop index
    dfvx['Animal_ID'] = [x.split("*")[0] for x in dfvx['index']]
    dfvx['Image'] = [x.split("*")[1] for x in dfvx['index']]
    dfvx = dfvx.drop(["index"],axis=1)
    #check for duplicates and group
    cls = dfvx.columns.tolist() #get list of column headers
    grBy = ['Animal_ID','Image'] #list of columns to group by
    groups = [x for x in cls if x not in grBy] #get list of columns to be grouped
    df1 = dfvx.groupby(['Animal_ID','Image'])[groups].apply(lambda x: x.astype(float).sum()).reset_index() #group to make sure no duplicates
    df_vol = pd.merge(df_all,df1,on = ['Animal_ID','Image']) #merge volume df with big df
    return df_vol

#BAI from parabola functions
def bai_parabola(df_all,tl_name,b_interval,b_lower,b_upper):
    df_all = df_all.dropna(how="all",axis='rows').reset_index()
    vname = '{0}%'.format(b_interval)
    bai_name = "BAIpar_{0}".format(vname) #create BAI column header using interval
    sa_name = 'SA_{0}'.format(vname)
    bai = [] #list of columns containing the width data we want to use to calculate BAI
    perc_l = []
    for x in range(b_lower,(b_upper + b_interval), b_interval): # loop through columns w/in range we want
        xx = "{0}-{1}.0% Width".format(tl_name,str(x)).format(str(x)) #set up column name
        bai += [xx]
        perc_l += [x/100]
    #here we check that the widths are actually in the column headers
    colarr = np.array(df_all.columns)
    mask = np.isin(colarr,bai)
    cc = list(colarr[mask])
    blist = []
    blist.extend(cc)
    #calculate BAI
    df_all_ix = df_all
    df_all_ix['index'] = df_all_ix['Animal_ID']+"*"+df_all_ix['Image'] #make column thats Image and AID combined
    npy = np.array(df_all_ix[bai]) #make array out of width values to be used
    ids = np.array(df_all_ix['index'])
    plist = np.array(perc_l) #make array of the percents
    npTL = np.array(df_all_ix[tl_name]) #make array of the total lengths
    x = np.tile(npTL.reshape(npTL.shape[0],-1), (1,plist.size)) #make a 2D array of TL's repeating to be multiplied with the percs
    npx = x * plist #make 2D array of the x values for the regression
    min_tl = npTL*(b_lower/100)
    max_tl = npTL*(b_upper/100)
    newx = np.linspace(min_tl,max_tl,500)
    sas = []
    for i in range(npx.shape[0]):
        xx = npx[i,:]; yy = npy[i,:]; newxx = newx[:,i]
        lm = np.polyfit(xx,yy,2)
        fit = np.poly1d(lm)
        pred = fit(newxx)
        I = quad(fit, min_tl[i], max_tl[i])
        sas.append(I[0])
    bais = (sas/((npTL*((b_upper-b_lower)/float(100)))**2))*100
    bai_arr = np.column_stack((ids,bais,sas))
    dfb = pd.DataFrame(data = bai_arr,columns= ['index',bai_name,sa_name])
    dfb['Animal_ID'] = [x.split("*")[0] for x in dfb['index']]
    dfb['Image'] = [x.split("*")[1] for x in dfb['index']]
    dfb = dfb.drop(["index"],axis=1)
    cls = dfb.columns.tolist()
    grBy = ['Animal_ID','Image'] #list of columns to group by
    groups = [x for x in cls if x not in grBy]
    dfp = dfb.groupby(["Animal_ID",'Image'])[groups].apply(lambda x: x.astype(float).sum()).reset_index()
    return dfp

#BAI trapezoid function
def bai_trapezoid(df_all,tl_name,b_interval,b_lower,b_upper):
    bai_name = "BAItrap_{0}%".format(b_interval) #create BAI column header using interval
    bai = [] #list of columns containing the width data we want to use to calculate BAI
    for x in range(b_lower,(b_upper + b_interval), b_interval): # loop through columns w/in range we want
        xx = "{0}-{1}.0% Width".format(tl_name,str(x)) #set up column name
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
