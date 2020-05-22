# Demo

## File Table of Contents

### **Folders**

**altitude_calibration_outputs**: This folder contains example outputs from MorphoMetrix of measured calibration objects.

**measured_whale_outputs**: This folder contains example outputs from MorphoMetriX of measured whales. These measurements include perpendicular widths measured at 10% increments. Note that the manually entered altitude values are not necessarily correct and uncalibrated, so the values of the collated output will be different.

### **Altitude calibration files**
**calibration_obj_imglist.csv**: This is the list of the measured calibration object images. It includes the date, flight, altitude, focal length, and pixel dimension per image.

**image_list**: This is the list of measured whale image that includes the date, flight, focal length, pixel dimension, and altitude per image. The altitude in this datasheet is the altitude that was recorded by the drone that needs to be calibrated.

### **Main function files**
**demo_safety.csv**: This is the sheet that includes the calibrated altitudes, focal lenghts, and pixel dimensions. The output of the altitude calibration should look like this file.

**demo_animal_list.csv**: This is an example of the animal list that can be used to subset the collated datasheet by animal ID.

## Demo altitude calibration input instructions
- Use the calibration_obj_imglist.csv as the calibration object img list input
- Use the image_list.csv as the img list w/ altitudes input
- Board Length measurement name = BL
- True length of calibration object = 1
- Folder containing MorphoMetriX outputs = altitude_calibration_outputs

## Demo collatrix input instructions
- Animal ID from folder name?: either is fine
- Safety: yes, use altitude calibration file from altitude calibration function. Or provided demo_safety.csv
- List of Specific Individuals: either is fine, if yes use demo_animal_list.csv
- Output name: whatever you want
- Location of MorphoMetrix files: measured_whales_outputs folder

## Demo whale body condition input instructions
- Name of length measurement = TL
- Lower bound = 20
- Upper bound = 80
- Interval = 10
*use these settings for both body volume and BAI
