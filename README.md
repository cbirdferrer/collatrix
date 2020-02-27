# morphometrix-collating
 this tool collates the outputs of the MorphoMetriX photogrammetry tool
 This script combines all the output csvs and makes one large data frame that contains the image, animal ID, and all measurements. If you used different names for measurements these will just appear as extra columns with empty cell values for places where you didn’t use that measurement name.

## Installation
  as of now you need to download the python file for the script

## Running
  to run the script
  1. open a command prompt or terminal window
  2. type python
  3. drag and drop the python script from its folder on your computer to the terminal window

  so it should look like this

  ```
  python \filepath\gui_collating_alloptions_v6.0.py
  ```
## Things to know
1. if there’s a repeated Object Name in a GUI output csv (like two rows of Total Length) the script will end and give you a message telling you to get rid of the duplicate. If you want both instances of the measurement included, then just alter the name slightly (for example: Total Length_1).

2. If you used different names for measurements these will just appear as extra columns with empty cell values for places where you didn’t use that measurement name.

## Inputs
This script has several options and inputs to be aware of that will be explained here. Note, these are listed in the order that the tool will ask you to enter them.

### 1. Save Location
  For this script you can either have the MorphoMetriX output csvs saved in **One Folder** or in **Individual Folders**
  If you choose OneFolder, the Animal ID will be the Animal ID provided through MorphoMetrix, if you choose Individual Folders the Animal ID will be the name of the folder it was saved in.

  An example of **One Folder** is       
  * Folder      
        > whale1.csv    
        > whale2.csv
  
  An example of **Individual Folders** is         
  * Whale1      
        > whale1.jpg    
        > whale1.csv
  * Whale2      
        > whale2.jpg    
        > whale2.csv

### 2. Safety
  Because it's easy to accidentally enter the wrong altitude, focal length, or pixel dimension in MorphoMetriX, this tool can recalculate the measurements using the correct values. Selecting "yes" for this input will have the tool recalculate, using values that you will need to provide through an extra sheet. Instructions for formatting this sheet will be provided later on.

### 3. Body Volume (for whales)
 Using the methods from *Maternal body size and condition determine calf growth rates in southern right whales
Christiansen, F., Vivier, F., Charlton, C., Ward, R., Amerson, A., Burnell, S., & Bejder, L. (2018). Maternal body size and condition determine calf growth rates in southern right whales. Marine Ecology Progress Series, 592, 267–281. http://doi.org/10.3354/meps12522*
the tool will calculate body volume if widths are measured. If you say 'yes' to having body volume calculated, you will enter some more information.
1. the name of your total length measurement (so if you named it TL enter TL) 
2. The lower bound percentage (so if you want to use widths from 20% of total length to 80%, 20 would be the lower bound) 
3. The upper bound (using the above example, 80 would be the upperbound) 
4. The interval (if you want it calculated using 10% increments, enter 10. **Note** this value cannot be less than the increments of width that you measured) 

### 3. List of Specific Individuals 
  If you want an extra output csv containing only a subset of animals, select 'yes' for this input. You will still get an output file containing the collated information from all the csvs.If you want this you will need to provide a csv containing the ids you want.

### 4. Output name 
The tool will ask you what name you want for the output csv. The collated final csv outputted by this tool will be named inputname_allIDs.csv. If you selected yes for list of specific individuals, a second list containing the subset will be outputed named inputname_IDS.csv. 

### 5. Location of MorphoMetriX files
A window will open asking you to select the folder where the MorphoMetriX csvs are saved. 
* If you have them in one folder, select that folder
* If you have them in individual folders, select the folder containing all the individual folders

### 6. Location where output should be saved
Select the folder where you want the output of this tool to be saved

### 7. Select the safety csv (only if you said 'yes' to safety)
Select the csv file containing the correct Altitude, Focal Length, and Pixel Dimension data per image

### 8. Select the individual list csv (only if you said 'yes' to a individual list)
Select the csv file containing the list of Animal_IDs that you want included in the subset list

## Input File Format
* If you use the safety or the list of specific individuals, the input sheets have to be specifically formated
* Note, the name of these sheets won't matter, the format of the **headers** matters most

### Safety List
* Required columns (spelled and capitalized just as written here): Image, Altitude, Focal_Length, Pixel_Dimension
* Make sure that the image anmes are identical to the name of the images measured

Example table

Image | Altitude | Focal_Length | Pixel_Dimension
----- | -------- | ------------ | ---------------
whale1.JPG | 55.0 | 35 | 0.0039
whale2.JPG | 40.0 | 35 | 0.0039

### Individual List
* If you want a second output csv containing only a specific subset of individuals you'll need to specify a csv containing that list.
* Required column: Animal_ID
* Make sure that the ID's listed are spelled exactly as those in the MorphoMetriX outputs

Example table

Animal_ID |
--------- |
Whale1
