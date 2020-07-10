# Example Setup Code
Many of the inputs to  `CollatriX` are image lists. `CollatriX` can work with files saved in any file structure. However, if you still need to make a list and don't want to go through the tedious process of making it manually, here's some example code written for previous projects to make the **Image** column of the input lists. Even if it's not exactly what you're looking for, we hope it's a useful starting off point.

In this example, the outputs were stored in a file structure that looked like this:  
```
GUI FOLD     
     YYMMDD    
          Flight Number     
               Whale ID       
                    img.csv        
                    img.csv    
```

So I also used the folders to create the Date and Flight columns for the altitude calibration.
```
#import packages
import pandas as pd
import os,sys
import numpy as np

#set folder where ouputs are stored
wd = r'\GUI FOLD' #path to where outputs are saved
```

In this case I only wanted csvs within a folder that included the word "whale". But if you just want all the csvs in the file structure, you don't need the extra if-else statement.
```
#loop through folder and pull all csvs.
csvs = []
for r,d,f in os.walk(wd):
    if "whale" in r:
      csvs += [os.path.join(r,f) for f in f if f.endswith(".csv") and not f.startswith(".")]
```
If, however, you had calibration files and measured animal files nested in the same structure.  

```
Flight Number
     Whale ID
     Calibration  
```

Then you could add a statement:
```
#loop through folder and pull all csvs.
csvs_wh = []
csvs_cal = []
for r,d,f in os.walk(wd):
    if "whale" in r:
      csvs_wh += [os.path.join(r,f) for f in f if f.endswith(".csv") and not f.startswith(".")]
    elif "Calib" in r:
      csvs_cal += [os.path.join(r,f) for f in f if f.endswith(".csv") and not f.startswith(".")]
```

Next we use the folder names in the path to fill the columns we need.
```
#make the list of csvs a column in a dataframe
dfb = pd.DataFrame(data={'root':csvs})
#do first path split
dfb['split'] = [os.path.split(i) for i in dfb['root']]
#isolate the file name, switch .csv for the image type suffix
dfb['csv'] = [i[1].replace(".csv",".png") for i in dfb['split']]
#isolate the flight number
dfb['Flight'] = [os.path.split(os.path.split(i[0])[0])[1] for i in dfb['split']]
#isolate the date
dfb['Date'] = [os.path.split(os.path.split(os.path.split(i[0])[0])[0])[1] for i in dfb['split']]

#finally export dataframe to csv
outname = os.path.join(wd,"imagelist.csv")
dfb.to_csv(outname,sep=',')
```
