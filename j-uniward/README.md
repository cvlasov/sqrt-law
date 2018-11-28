# j-uniward

This directory contains code originally from the [DDE Lab at Binghamton University](http://dde.binghamton.edu/). It was downloaded from [here](http://dde.binghamton.edu/download/stego_algorithms/) on 05/11/18. The code has been modified and the history of all changes can be seen in this project's commit history.

The files in the two sub-directories do not constitute self-contained applications. You can use them by downloading J-UNIWARD from http://dde.binghamton.edu/download/stego_algorithms and replacing the relevant files in the ```J-UNIWARD_src``` sub-directory with the files from either sub-directory.

There are two subdirectories:
* ```costs```: These files do not do embedding. They only use J-UNIWARD to compute the costs of changing each coefficient in an image and save these costs to a file.
* ```embedding```: These files do embedding. They behave in the same way as the J-UNIWARD code that can be downloaded straight from the DDE Lab website.
* ```embed-with-costs```: These files do embedding. They are just like those in ```embedding``` except that they use pre-computed costs rather than computing the costs, as the original J-UNIWARD code does.
* ```utilities```: This consists of a file called ```jpeg_utils.cpp``` that provides a number of JPEG utilities. It can display the number of coefficients that differ between cover and stego images and by how much they differ (+1, -1, or something else) as well as the number of non-zero coefficients in cover images. This will be expanded as new utilities are needed.
