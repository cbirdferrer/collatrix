import pytest
import pandas as pd
import os,sys
import numpy as np
import collatrix.collatrix_functions
from collatrix.collatrix_functions import anydup
from collatrix.collatrix_functions import collate

def test_dup():
    l = ['a','b']
    a = anydup(l)
    assert a == False

w1fold = 'https://raw.githubusercontent.com/cbirdferrer/collatrix/master/demo/measured_whales_outputs/Whale1'
w1csvs = ['170816_A_F2_DSC04215.csv','170816_A_F2_DSC04232.csv','170816_A_F2_DSC04263.csv']
w2fold = 'https://raw.githubusercontent.com/cbirdferrer/collatrix/master/demo/measured_whales_outputs/Whale2'
w2csvs = ['170809_A_F3_DSC01152.csv','170809_A_F3_DSC01185.csv','170809_A_F3_DSC01243.csv']

csvs = []
for i in w1csvs:
    csvs += [os.path.join(w1fold,i)]
for ii in w2csvs:
    csvs += [os.path.join(w2fold,ii)]

measurements = []
nonPercMeas = []
df_L = pd.read_csv("https://raw.githubusercontent.com/cbirdferrer/collatrix/master/demo/demo_safety.csv")
safety = "yes"
anFold = 'no'
constants = ['Image ID', 'Image Path', 'Focal Length', 'Altitude', 'Pixel Dimension']

def test_col():
    dfx = collate(csvs,constants,measurements,nonPercMeas,df_L,safety,anFold)
    return(print(dfx))
    assert dfx.empty == False
