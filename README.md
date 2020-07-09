# CollatriX
[![DOI](https://zenodo.org/badge/243385218.svg)](https://zenodo.org/badge/latestdoi/243385218)  

## Background
This function collates the csv outputs from the MorphoMetriX photogrammetry GUI (https://github.com/wingtorres/morphometrix) into one large single data frame containing the image, animal ID, measurements, and notes.  
CollatriX was designed with several add-ons. A figure showing the different routes available is included below:  
![alt text](https://github.com/cbirdferrer/collatrix/blob/master/images/Figure1.png)

The altitude calibration function (`collatrix.altitude_calib`) can be used to calculate corrected altitudes using images of an object of known length. If used, this function should be used before the main function. The output can be used to create the safety input file for the main `collatrix` function. Note that the altitude calibration function is not required, the user can start the workflow using the main `collatrix` function. The output of this main function can then be used to calculate metrics of whale body condition (`collatrix.whale_bc`) if desired.

To jump to the altitude calibration function instructions click [here](https://github.com/cbirdferrer/collatrix#altitude-calibration-function)

To jump to the whale body condition function instructions click [here](https://github.com/cbirdferrer/collatrix#whale-body-condition-function)


## Installation
[![Anaconda-Server Badge](https://anaconda.org/cbird/collatrix/badges/version.svg)](https://anaconda.org/cbird/collatrix)

  The easiest way to install is through the Anaconda python distribution. In anaconda create/use your preferred environment, open command line and enter. Note that you'll need python version 3.6 or higher.
  ```
  conda install -c cbird collatrix
  ```

  Note that `collatrix` can be installed and run in the same [environment](https://github.com/wingtorres/morphometrix#installation) as `morphometrix`.

## Running
After the package has been installed in your preferred environment enter this command

  ```
  python -m collatrix
  ```
## Important Tips
1. If there is a repeated Object Name in a GUI output csv (i.e. two rows of Total Length) the script will end and give you a message telling you to get rid of the duplicate. If you want both instances of the measurement included, then just alter the name slightly (for example, "Total Length_1").

2. Each measurement receives its own column. Rows are simply left blank for images that do not contain a measurement.

3. Naming recommendations: Create simple labels for measurements in MorphoMetriX to reduce chances of mistyping a label while measuring (i.e. consider using "TL" for total length). If you want body volume to be calculated the name of the length measurement **cannot** contain a dash (-) (i.e.use "total length" or "TL" instead of "total-length").

4. The output file from CollatriX is linked by the "Image ID" input in MorphoMetriX, so it is ok to use the same image to generate multiple csv outputs as long as the image ID is unique or the output csv file is unique.

5. If you measure the same whale in the same image twice (separate csvs), make sure that you do not repeat a measurement name as this will overwrite the previous measurement. For instance, if you are measuring the total length of a whale twice and want to create two separate csvs for each one, use "TL1" and "TL2" for each measurement.

## Inputs
This script has several options and inputs to be aware of that will be explained here. Note, these are listed in the order that the function will ask you to enter them.

### 1. Do you want the Animal ID to be assigned based on the name of the folder?
  MorphoMetriX output csvs can be saved in any file structure. The function will search through all folders within the folder provided and pull all csvs. If you have saved the outputs within folders named using Animal IDs, you can choose to have the Animal ID be pulled from the folder name. If no is selected, the Animal ID will be the 'Image ID' manually entered through MorphoMetriX.

  An example of a file structure where the folders are named using the Animal ID is:         
  * Whale1      
        > image_name1.jpg    
        > image_name1.csv
  * Whale2      
        > image_name2.jpg    
        > image_name2.csv

### 2. Safety
  Because it's easy to accidentally enter the wrong altitude, focal length, or pixel dimension in MorphoMetriX, this function can recalculate the measurements using the correct values. Selecting "yes" for this input will have the function recalculate, using values that you will need to provide through an additional csv. If you select 'yes',a box will pop up asking you to select this file from where it is saved.
#### How to format this csv (note: header spelling and capitalization matters most)
* Required columns (spelled and capitalized just as written here): Image, Altitude, Focal_Length, Pixel_Dimension
* Make sure that the image names are identical to the name of the images measured (be mindful of capitilzation, *especially of the file exentions*, .JPG and .jpg would not be considered matching).

Example

Image | Altitude | Focal_Length | Pixel_Dimension
----- | -------- | ------------ | ---------------
whale1.JPG | 55.0 | 35 | 0.0039
whale2.JPG | 40.0 | 35 | 0.0039

### 3. List of Specific Individuals
  If you want an extra output csv containing only a subset of animals, select 'yes' for this input. You will still get an output file containing the collated information from all the csvs. To pull a subset of individuals you will need to provide a csv containing the IDs you want.
  If you select 'yes', a window will open asking you to select this csv file containing the list of Animal_IDs that you want included in the subset list.  
#### How to format this csv (note: header spelling and capitalization matters most)
* If you want a second output csv containing only a specific subset of individuals you'll need to specify a csv containing that list.
* Required column: Animal_ID
* Make sure that the ID's listed are spelled exactly as those in the MorphoMetriX outputs

Example

Animal_ID |
--------- |
Whale1

### 4. Output name
The function will ask you what name you want for the output csv. The collated final csv outputted by this function will be named inputname_allIDs.csv. If you selected yes for list of specific individuals, a second list containing the subset will be produced and named inputname_IDS.csv.

### 5. Location of MorphoMetriX files
A window will open asking you to select the folder where the MorphoMetriX csvs are saved.

### 6. Location where output should be saved
Select the folder where you want the output of this function to be saved

# Add-on Functions

## Altitude Calibration Function
Barometers are known to provide inaccurate measures of altitude. Burnett et al. (2018) developed a method to calibrate the altitude of the drone using images of an object of known length. We have written a function to replicate this calibration. The output will be named **altitude_calibration.csv**.

  ```
  python -m collatrix.altitude_calib
  ```
### Inputs
#### 1. Calibration object image list
This sheet should contain information on the altitude, focal length, pixel dimension, date, and flight of the calibration object images. Like the safety sheet for the main function, this information is used to ensure proper calculation of the pixel count.

**How to format this csv (note: header spelling and capitalization matters most)** 
* Required columns (spelled and capitalized just as written here): Image, Altitude, Focal_Length, Pixel_Dimension, Date, Flight
* Make sure that the image names are identical to the name of the images measured (be mindful of capitalization, *especially of the file exentions*, .JPG and .jpg would not be considered matching).
* The contents of the Date and Flight columns can be formatted however, it just needs to match the formatting of the Date and Flight columns in the image information file (input 2).

Image | Altitude | Focal_Length | Pixel_Dimension | Date | Flight |
----- | -------- | ------------ | ---- | ---- | ------ |
obj1.JPG | 25.0 | 35 | 0.0039 | 2017_05_12 | F4 |
obj2.JPG | 20.0 | 35 | 0.0039 | 2017_05_12 | F4 |

#### 2. Image information file
This sheet should contain information on the altitude, date, and flight per image. The altitude should be the entered altitude that needs to corrected.

**How to format this csv (note: header spelling and capitalization matters most)**
* Required columns (spelled and capitalized just as written here): Image, UAS_Alt, Date, Flight
* Make sure that the image names are identical to the name of the images measured (be mindful of capitilzation, *especially of the file exentions*, .JPG and .jpg would not be considered matching).
* UAS_Alt should be the altitude that was recorded by the UAS. This is the altitude that will be corrected.
* The contents of the Date and Flight columns can be formatted however the user prefers, however it needs to match the formatting of the Date and Flight columns in the calibration object image list (input 1).
* Note: the output of this function will merge the calibrated altitudes with this sheet, so the user can choose to add the Focal_Length and Pixel_Dimension columns before or after running this function to make the safety sheet for the main function.

Image | UAS_Alt | Date | Flight |
----- | -------- | ---- | ------ |
whale1.JPG | 55.0 | 2017_05_12 | F4 |
whale2.JPG | 40.0 | 2017_05_12 | F4 |

#### 3. Calibration object length measurement name
The name of your length measurement (i.e. if you named total length "OL" enter "OL")

#### 4. Calibration object length in meters
The length of the calibration object (i.e. if the object was 1.0 meters long enter 1.0)

#### 5. Folder containing MorphoMetriX outputs
Select the folder where the outputs are saved. The files can be nested within a file structure.

#### 6. Folder where output should be saved
Select the folder where you want the output to be saved.

## Whale Body Condition Function

```
python -m collatrix.whale_bc
```
### Inputs
#### 1. CollatriX output csv
Select the csv containing the collated measurements outputted by CollatriX

#### 2. Body Volume
CollatriX also provides the option to calculate body volume from perpendicular width intervals along a total length measurement following Christiansen et al. 2018. If you say "yes" to have body volume calculated, the following information will need to be provided:

1. The name of your length measurement (i.e. if you named total length "TL" enter "TL")
2. The lower bound percentage (i.e. if you want to use widths between 20-80% of total length to calculate body volume, then 20 would be the lower bound)
3. The upper bound (using the above example, 80 would be the upper bound)
4. The interval that the widths were measured in (i.e 5 if you measured in 5% increments. **Note** this value cannot be less than the increments of width that you measured).

*Christiansen, F., Vivier, F., Charlton, C., Ward, R., Amerson, A., Burnell, S., & Bejder, L. Maternal body size and condition determine calf growth rates in southern right whales (2018). Maternal body size and condition determine calf growth rates in southern right whales. Marine Ecology Progress Series, 592, 267–281. http://doi.org/10.3354/meps12522*

If you calculate body volume, please cite Christiansen et al. 2018 in addition to this software.

#### 3. Body Area Index (BAI)
CollatriX also provides the option to calculate BAI from perpendicular width intervals along a total length measurement following Burnett et al. 2018. If you say "yes" to have BAI calculated, the following information will need to be provided:

1. The method used to calculate BAI. Options: parabola, trapezoid, or both.
* The parabola method will calculate a parabola for the sides of the whale using the width measurements and surface is calculated as the area under this curve (Burnett et al. 2018). The trapezoid method calculates the surface area by summing the surface areas of the trapezoids created between each segment (Christiansen et al. 2016). You can also select both to have both methods used.
2. The name of your length measurement (i.e. if you named total length "TL" enter "TL")
3. The lower bound percentage (i.e. if you want to use widths between 20-80% of total length to calculate body volume, then 20 would be the lower bound)
4. The upper bound (using the above example, 80 would be the upper bound)
5. The interval that the widths were measured in (i.e 5 if you measured in 5% increments. **Note** this value cannot be less than the increments of width that you measured).

*Burnett, Jonathan D., Leila Lemos, Dawn Barlow, Michael G. Wing, Todd Chandler, and Leigh G. Torres. 2018. “Estimating Morphometric Attributes of Baleen Whales with Photogrammetry from Small UASs: A Case Study with Blue and Gray Whales.” Marine Mammal Science 35 (1): 108–39. https://doi.org/10.1111/mms.12527.*

If you calculate BAI please cite Burnett et al. 2018 in addition to this software.

#### 4. Output name
The function will ask you what name you want for the output csv. The csv outputted by this function will be named inputname_bodycondition.csv.

#### 5. Location where output should be saved
Select the folder where you want the output of this function to be saved

#### Output format
The output of this function will be the `collatrix` output with added columns. If all three metrics were calculated at 10% intervals the headers would be Body_Vol_10%, BAIpar_10%, and BAItrap_10%. BAIpar is BAI calculated using parabolas and BAItrap is BAI calculated using trapezoids.

## Demo
A demonstration is available in the [demo](https://github.com/cbirdferrer/collatrix/tree/master/demo) directory. The demo includes a separate README file with instructions for what inputs to use.

### Automated Testing
A GitHub Action has been set up to test the main `collatrix` function when an update is pushed to the master branch using `pytest`. If you are working on editing `collatrix` and would like to run the automated tests locally, open a terminal or command prompt window, then change the directory (`cd`) to the folder where you have cloned `collatrix` to, then type `pytest`, the test should then run.

For example:

```
(base) :~ user$ cd github/collatrix
(base) :collatrix user$ pytest
```

# Attribution
If you use this software please cite our paper.

Additionally, if you used `collatrix.whale_bc` to measure cetacean body condition:
* Cite Christiansen et al. (2018) for Body Volume  
*Christiansen, F., Vivier, F., Charlton, C., Ward, R., Amerson, A., Burnell, S., & Bejder, L. Maternal body size and condition determine calf growth rates in southern right whales (2018). Maternal body size and condition determine calf growth rates in southern right whales. Marine Ecology Progress Series, 592, 267–281. http://doi.org/10.3354/meps12522*

* Cite Burnett et al. (2018) for Body Area Index  
*Burnett, Jonathan D., Leila Lemos, Dawn Barlow, Michael G. Wing, Todd Chandler, and Leigh G. Torres. 2018. “Estimating Morphometric Attributes of Baleen Whales with Photogrammetry from Small UASs: A Case Study with Blue and Gray Whales.” Marine Mammal Science 35 (1): 108–39. https://doi.org/10.1111/mms.12527.*

# Contributing
We designed CollatriX with future collaborations in mind and we'd love for you to contribute! If you'd like to contribute please see our [contributing guidelines](https://github.com/cbirdferrer/collatrix/blob/master/CONTRIBUTING.md)

# Code of Conduct
See our [code of conduct](https://github.com/cbirdferrer/collatrix/blob/master/CODE_OF_CONDUCT.md)

# License
[![Anaconda-Server Badge](https://anaconda.org/cbird/collatrix/badges/license.svg)](https://anaconda.org/cbird/collatrix)

Copyright (c) 2020 Clara Bird, KC Bierlich

`Collatrix` is free software made available under the MIT License. For details see the the [LICENSE](https://github.com/cbirdferrer/collatrix/blob/master/LICENSE) file.

# Contributors
Clara N. Bird and KC Bierlich are the developers of this software.
