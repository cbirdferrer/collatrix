# CollatriX
 This tool collates the csv outputs from the MorphoMetriX photogrammetry tool (https://github.com/wingtorres/morphometrix) into one large single data frame containing the image, animal ID, measurements, and notes.

## Installation
[![Anaconda-Server Badge](https://anaconda.org/cbird/collatrix/badges/version.svg)](https://anaconda.org/cbird/collatrix)

  The easiest way to install is through the Anaconda python distribution. In anaconda create/use your preferred environment, open command line and enter
  ```
  conda install -c cbird collatrix
  ```

## Running
After the package has been installed in your preferred environment enter this command

  ```
  python -m collatrix
  ```
## Important Tips
1. If there is a repeated Object Name in a GUI output csv (i.e. two rows of Total Length) the script will end and give you a message telling you to get rid of the duplicate. If you want both instances of the measurement included, then just alter the name slightly (for example, "Total Length_1").

2. Each measurement recieves its own column. Rows are simply left blank for images that do not contain a measurement.

3. Naming recommendations: Create simple labels for measurements to reduce chances of mistyping a label while measuring (i.e. consider using "TL" for total length). If you want body volume to be calculated the name of the length measurement **cannot** contain a dash (-) (i.e.use "total length" or "TL" instead of "total-length").

4. The output file from CollatriX is linked by the "Image ID" input in MorphoMetriX, so it is ok to use the same image to generate multiple csv outputs as long as the image ID is unique or the output csv file is unique.

5. If you measure the same whale in the same image twice (separate csvs), make sure that you do not repeat a measurement name as this will overwrite the previous measurement. For instance, if you are measuring the total length of a whale twice and want to create two separate csvs for each one, use "TL1" and "TL2" for each measurement.

## Inputs
This script has several options and inputs to be aware of that will be explained here. Note, these are listed in the order that the tool will ask you to enter them.

### 1. Save Location
  MorphoMetriX output csvs can be saved in either **One Folder** or in **Individual Folders**
  If you choose OneFolder, the Animal ID will be the Animal ID provided in MorphoMetriX. If you choose Individual Folders, each output csv needs to be saved in a folder with its respective Animal ID.

  An example of **One Folder** is       
  * Folder      
        > image_name1.csv    
        > image_name2.csv

  An example of **Individual Folders** is         
  * Whale1      
        > image_name1.jpg    
        > image_name1.csv
  * Whale2      
        > image_name2.jpg    
        > image_name2.csv

### 2. Safety
  Because it's easy to accidentally enter the wrong altitude, focal length, or pixel dimension in MorphoMetriX, this tool can recalculate the measurements using the correct values. Selecting "yes" for this input will have the tool recalculate, using values that you will need to provide through an additional csv. If you select 'yes',a box will pop up asking you to select this file from where it is saved.
#### How to format this csv (note: header spelling and capitalization matters most)
* Required columns (spelled and capitalized just as written here): Image, Altitude, Focal_Length, Pixel_Dimension
* Make sure that the image names are identical to the name of the images measured (be mindful of capitilzation, *especially of the file exentions*, .JPG and .jpg would not be considered matching).

Example 

Image | Altitude | Focal_Length | Pixel_Dimension
----- | -------- | ------------ | ---------------
whale1.JPG | 55.0 | 35 | 0.0039
whale2.JPG | 40.0 | 35 | 0.0039

### 3. Body Volume (for whales)
CollatriX also provides the option to calculate body volume from perpendicular width intervals along a total length measurement following Christiansen et al. 2018. If you say "yes" to have body volume calculated, the following information will need to be provided:

1. The name of your length measurement (i.e. if you named total length "TL" enter "TL")
2. The lower bound percentage (i.e. if you want to use widths between 20-80% of total length to calculate body volume, then 20 would be the lower bound)
3. The upper bound (using the above example, 80 would be the upper bound)
4. The interval that the widths were measured in (i.e 5 if you measured in 5% increments. **Note** this value cannot be less than the increments of width that you measured).

*Christiansen, F., Vivier, F., Charlton, C., Ward, R., Amerson, A., Burnell, S., & Bejder, L. Maternal body size and condition determine calf growth rates in southern right whales (2018). Maternal body size and condition determine calf growth rates in southern right whales. Marine Ecology Progress Series, 592, 267–281. http://doi.org/10.3354/meps12522*

### 4. Body Area Index (BAI) (for whales)
CollatriX also provides the option to calculate BAI from perpendicular width intervals along a total length measurement following Burnett et al. 2019. If you say "yes" to have BAI calculated, the following information will need to be provided:

1. The method used to calculate BAI. Options: parabola, trapezoid, or both. 
* The parabola method will calculate a parabola for the sides of the whale using the width measurements and surface is calculated as the area under this curve. The trapezoid method calculates the surface area by summing the surface areas of the trapezoids created between each segment. You can also select both to have both methods used.

2. The name of your length measurement (i.e. if you named total length "TL" enter "TL")
3. The lower bound percentage (i.e. if you want to use widths between 20-80% of total length to calculate body volume, then 20 would be the lower bound)
4. The upper bound (using the above example, 80 would be the upper bound)
5. The interval that the widths were measured in (i.e 5 if you measured in 5% increments. **Note** this value cannot be less than the increments of width that you measured).

*Burnett, Jonathan D., Leila Lemos, Dawn Barlow, Michael G. Wing, Todd Chandler, and Leigh G. Torres. 2019. “Estimating Morphometric Attributes of Baleen Whales with Photogrammetry from Small UASs: A Case Study with Blue and Gray Whales.” Marine Mammal Science 35 (1): 108–39. https://doi.org/10.1111/mms.12527.*

### 5. List of Specific Individuals
  If you want an extra output csv containing only a subset of animals, select 'yes' for this input. You will still get an output file containing the collated information from all the csvs.If you want this you will need to provide a csv containing the ids you want.
  If you select 'yes', a window will open asking you to select this csv file containing the list of Animal_IDs that you want included in the subset list.  
#### How to format this csv (note: header spelling and capitalization matters most)
* If you want a second output csv containing only a specific subset of individuals you'll need to specify a csv containing that list.
* Required column: Animal_ID
* Make sure that the ID's listed are spelled exactly as those in the MorphoMetriX outputs

Example 

Animal_ID |
--------- |
Whale1

### 6. Output name
The tool will ask you what name you want for the output csv. The collated final csv outputted by this tool will be named inputname_allIDs.csv. If you selected yes for list of specific individuals, a second list containing the subset will be outputed named inputname_IDS.csv.

### 7. Location of MorphoMetriX files
A window will open asking you to select the folder where the MorphoMetriX csvs are saved.
* If you have them in one folder, select that folder
* If you have them in individual folders, select the folder containing all the individual folders

### 8. Location where output should be saved
Select the folder where you want the output of this tool to be saved

## Demo 
A demonstration is available in the [demo](https://github.com/cbirdferrer/collatrix/tree/master/demo) directory. The directory includes a text file with the body volume settings that should be used for those files.

# License
[![Anaconda-Server Badge](https://anaconda.org/cbird/collatrix/badges/license.svg)](https://anaconda.org/cbird/collatrix)
  
Copyright (c) 2020 Clara Bird, KC Bierlich

`Collatrix` is free software made available under the MIT License. For details see the the [LICENSE](https://github.com/cbirdferrer/collatrix/blob/master/LICENSE) file.

# Contributors
Clara N. Bird and KC Bierlich are the developers of this software.
