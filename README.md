# CollatriX
[![DOI](https://joss.theoj.org/papers/10.21105/joss.02328/status.svg)](https://doi.org/10.21105/joss.02328) [![DOI](https://zenodo.org/badge/243385218.svg)](https://zenodo.org/badge/latestdoi/243385218)  [![Anaconda-Server Badge](https://anaconda.org/cbird/collatrix/badges/version.svg)](https://anaconda.org/cbird/collatrix)

## Background
This function collates the csv outputs from the MorphoMetriX photogrammetry GUI (https://github.com/wingtorres/morphometrix) into one large single data frame containing the image, animal ID, measurements, and notes.  
CollatriX was designed with several add-ons. A figure showing the different routes available is included below:  
![alt text](https://github.com/cbirdferrer/collatrix/blob/master/images/Figure1.png)

The altitude calibration function (`collatrix.altitude_calib`) can be used to calculate corrected altitudes using images of an object of known length. If used, this function should be used before the main function. The output can be used to create the safety input file for the main `collatrix` function. Note that the altitude calibration function is not required, the user can start the workflow using the main `collatrix` function. The output of this main function can then be used to calculate metrics of whale body condition (`collatrix.whale_bc`) if desired.

## Documentation
Information on how to install and use `collatrix` and example code can be found in our [wiki](https://github.com/cbirdferrer/collatrix/wiki)

## Demo
A demonstration is available in the [demo](https://github.com/cbirdferrer/collatrix/tree/master/demo) directory. The demo includes a separate README file with instructions for what inputs to use.

### Automated Testing
A GitHub Action has been set up to test the main `collatrix` function when an update is pushed to the master branch using `pytest`. If you are working on editing `collatrix` and would like to run the automated tests locally, open a terminal or command prompt window, then change the directory (`cd`) to the folder where you have cloned `collatrix` to, then type `pytest`, the test should then run.

For example:

```bash
(base) :~ user$ cd github/collatrix
(base) :collatrix user$ pytest
```

# Attribution
If you use this software please cite our paper:  
*Bird C. & Bierlich K., (2020). CollatriX: A GUI to collate MorphoMetriX outputs. Journal of Open Source Software, 5(51), 2328, https://doi.org/10.21105/joss.02328*

Additionally:
* if you used `collatrix.whale_bc` to calculate Body Volume cite:
*Christiansen, F., Vivier, F., Charlton, C., Ward, R., Amerson, A., Burnell, S., & Bejder, L. Maternal body size and condition determine calf growth rates in southern right whales (2018). Maternal body size and condition determine calf growth rates in southern right whales. Marine Ecology Progress Series, 592, 267–281. http://doi.org/10.3354/meps12522*

* if us used `collatrix.whale_bc ` to calculate BAI or `collatrix.altitude_calib` for the altitude calibration cite: 
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
