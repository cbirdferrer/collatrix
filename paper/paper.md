---
title: 'CollatriX: A tool to collate MophoMetriX outputs'
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
date: 1 April 2020
bibliography: paper.bib

---

# Summary

CollatriX is a graphical user interface (GUI) developed using PyQt5 to collate outputs from MorphoMetriX [@Torres:2020], a photogrammetric measurement GUI designed for morphometric analysis of wild animals from aerial imagery. For each image used in MorphoMetriX, a comma-separated-values sheet (.csv) is produced containing the custom measurements (length, area, angle) and their associated labels created by the user. Hence, projects with a large number of images in their morphometric analysis have a large number of output files, creating time-intensive and tedious workflows to manually combine output files into a single data file to be used in analysis. CollatriX was designed as a user-friendly GUI overcoming this limitation by collating these measurement outputs into a single data sheet (.csv) based on the animal’s individual ID.

# Features

CollatriX works with MorphoMetriX outputs saved in two different file structures: 1) all outputs saved in a single folder, or 2) outputs are saved in a folder corresponding to an individual animal. If the user used MorphoMetriX to measure perpendicular widths based on a length measurement, a common metric for assessing body condition in cetaceans [@Christiansen:2016; @Dawson:2017], CollatriX provides an option to automatically calculate body volume of the whale following [@Christiansen:2018]. Because MorphoMetriX allows the user to specify the number of width segments, CollatriX provides the option for the user to specify the number of width segments, i.e. 20 widths (5% increments of the total length), as well as the minimum and maximum bound in which to calculate body volume (i.e. widths between 20-85% of total length).

A safety option was also built in CollatriX to increase user efficiency in working through large image datasets while avoiding user input errors. MorphoMetrix automatically scales length measurements in pixels to real world values (i.e. meters) from manually entered altitude, focal length, and pixel dimension values. While this setup allows for each separate image to be scaled accordingly, there is potential for input errors when entering these values, especially when working through large datasets. CollatriX provides a safety option for users where the number of pixels in a length is back calculated, and the measurement is recalculated using the correct values per image from a user provided csv.

Finally, CollatriX has an option to select a subset of output csvs associated with a specified list of individuals. CollatriX has been used on MorphoMetriX outputs from several projects on a variety of cetacean species including bottlenose dolphins, Antarctic minke, dwarf minke, fin, blue, humpback, and pilot whales.

# Acknowledgements

We acknowledge Dr. David Johnston for project support, Walter Torres for development support, and Julian Dale for beta testing. This work was supported by the Duke University Marine Laboratory.


# References
