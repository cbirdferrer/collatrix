---
title: 'CollatriX: A GUI to collate MophoMetriX outputs'
tags:
  - Python
  - Drones
  - Photogrammetry
  - GUI
  - Morphometry

authors:
  - name: Clara N Bird
    orcid: 0000-0001-7763-7761
    affiliation: "1, 2"
  - name: KC Bierlich
    affiliation: 2
affiliations:
 - name: Marine Mammal Institute, Department of Fisheries and Wildlife, Oregon State University
   index: 1
 - name: Nicholas School of the Environment, Duke University Marine Laboratory
   index: 2
date: 22 May 2020
bibliography: paper.bib

---

# Summary

CollatriX is a graphical user interface (GUI) developed using PyQt5 to collate outputs from MorphoMetriX [@Torres:2020], a photogrammetric measurement GUI designed for morphometric analysis of wild animals from aerial imagery. For each image used in MorphoMetriX, a comma-separated-values sheet (.csv) is produced containing the custom measurements (length, area, angle) and their associated labels created by the user. Hence, projects with a large number of images in their morphometric analysis have a large number of output files, creating time-intensive and tedious workflows to manually combine output files into a single data file to be used in analysis. CollatriX was designed as a user-friendly GUI overcoming this limitation by collating these measurement outputs into a single data sheet (.csv) based on the animal’s individual ID (Fig. 1). Furthermore, CollatriX has two add-on functions, one to correct for altitude error from Unoccupied Aerial Systems (UAS or drone) flights and another for calculating different animal body condition metrics, following body volume from @Christiansen:2018 and body area index (BAI) from @Burnett:2018 (Fig. 1). The framework of CollatriX was also designed to have the flexibility to accommodate and encourage other future add-on functions.

# Main Features

CollatriX will work with MorphoMetriX output files saved in any file structure formats (i.e., a single folder vs. across multiple folders), it will search through the provided file structure and collect all csvs that were outputted by MorphoMetriX. We also included an option for a subset of the collated data to be outputted as a separate csv, the subset is selected using a list of Animal IDs provided by the user. A safety option was built in to CollatriX to increase user efficiency in working through large image datasets while avoiding user input errors. For example, MorphoMetriX automatically scales length measurements in pixels to real world values (i.e. meters) from manually entered altitude, focal length, and pixel dimension values [@Torres:2020]. While this setup allows for each separate image to be scaled accordingly, there is potential for input errors when entering these values, especially when working through large datasets. CollatriX provides a safety option for users where the number of pixels in a length measurement is back calculated, and the measurement is recalculated using the correct values per image from a user provided csv.

# Add-on Functions

CollatriX also has two add-on functions for calculating 1) an altitude calibration and 2) whale body condition (Fig. 1). The altitude calibration function is an Unoccupied Aerial Systems (UAS) altitude calibration function that follows the recommended Method 5 from @Burnett:2018, where measurements of a calibration object of known length are used to calculate the true altitude of the UAS to create a linear model used for correcting the altitude of images taken throughout the flight (for more detail see @Burnett:2018). The output of this add-on function can then be used as the safety for the main CollatriX function (Fig. 1).

The whale body condition add-on function calculates two metrics of cetacean body condition. If the user used MorphoMetriX to measure perpendicular widths based on a length measurement, a common method for assessing body condition in cetaceans [@Christiansen:2016; @Dawson:2017; @Burnett:2018], the function can calculate body volume of the whale following @Christiansen:2018 and Body Area Index (BAI) following @Burnett:2018. BAI is a measure of dorsal surface area normalized by length, and CollatriX can calculate the surface area using parabolas [@Burnett:2018] or trapezoids [@Christiansen:2016]. Since MorphoMetriX allows the user to specify the number of perpendicular width segments of a length measurement, CollatriX provides the flexibility for the user to specify the number of width segments to include in the body condition calculation, i.e. 20 widths (5% increments of the total length), as well as the minimum and maximum bound in which to calculate body volume or BAI (i.e. widths between 20-85% vs. 25-80% of total length).

Together, MorphoMetriX and CollatriX provide a toolkit that is flexible, easy to use, and adaptable to future projects on a variety of species and applications, as CollatriX is designed to easily incorporate other add-on functions. CollatriX has been used on MorphoMetriX outputs from several projects on a variety of cetacean species including bottlenose dolphins and Antarctic minke, dwarf minke, fin, blue, gray, and humpback whales.

# Figures

![Figure 1. Basic overview of CollatriX workflow using measurement outputs from MorphoMetriX (Torres and Bierlich 2020) Measurement outputs are collated into a single output file based on the ‘Image ID’. Solid arrows represent main pathway, dotted arrows represent pathway including add-on functions.](../images/Figure1.png)

# Acknowledgements

We acknowledge Dr. David Johnston and Dr. Leigh Torres for project support, Walter Torres for development support, and Julian Dale for beta testing. This work was supported by the Duke University Marine Laboratory and the Duke Marine Robotics and Remote Sensing Lab.


# References
