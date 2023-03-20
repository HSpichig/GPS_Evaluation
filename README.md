# GPS_Evaluation
Script for conducting a Bayesian evaluation of a single point location data recovered from a mobile device.

This python script provides the tools to conduct a Bayesian evaluation of a single point localisation as described in the article *A Likelihood Ratio Approach for the Evaluation of Single Point Device Locations* presented at DFRWS EU 2023 and published here: https://www.sciencedirect.com/science/article/pii/S2666281723000136

The first version of this repository is the code provided as an Annex in the aforementionned article. It is update as new results become available and when I have time to make the code more accessible. This is not my dayjob. If you are missing a feature and feel that updating intervals are too long, feel fre to develop it yourself.

The xlsx-files are provided as an example data-set. They are the data sets used in the article.

## Disclaimer
If you use this code for expertise in a court case, be aware that it is your responsability that the code works as intended and is adapted to the problem you aim to solve. I accept no liability for damages caused by using this code.
I'm no programmer. I refuse all liability for mental unease, heart problems or psychic damage caused by inefficient and bad coding.

## Functionality
The code requires coordinates of the locations specified in propositions P1 and P2, as well as the locations of the made observation E.
Reference measurements can be provided as a cellebrite locations output.
The code provides a scatter plot of all available data and histograms of the data within the observed wedge.
Probability values are outputted to SDTOUT.

## Use
Start by reading the article discussing the approach and make sure you understand the concept.
Then gather reference data at both your locations.

In the current version, you have to modify the code to provide it with the requisite values. This will be updated shortly.
I recommend using an IDE to do this.

## References
Spichiger, H., 2023. A likelihood ratio approach for the evaluation of single point device locations. Forensic Science International: Digital Investigation, Proceedings of the Tenth Annual DFRWS EU Conference 44, 301512. https://doi.org/10.1016/j.fsidi.2023.301512
