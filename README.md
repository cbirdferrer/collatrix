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
# Things to know
1. if there’s a repeated Object Name in a GUI output csv (like two rows of Total Length) the script will end and give you a message telling you to get rid of the duplicate. If you want both instances of the measurement included, then just alter the name slightly (for example: Total Length_1).

2. If you used different names for measurements these will just appear as extra columns with empty cell values for places where you didn’t use that measurement name.
