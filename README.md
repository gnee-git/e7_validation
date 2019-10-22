# e7_validation
A repository to store all codes used to validate e7_tools image reconstruction against the Siemens online reconstruction software. The data is collected from a Ge-68 doped plastic NEMA IQ phantom.

*The following intro is copied from the first e7_validation iPython Notebook...*

## Extracting the data...

The data, taken from the scanner, was reconstructed on both the scanner's version of software and the "e7" software, run offline on a PC in the University of Manchester's Nuclear Physics Lab. 

From here, data was extracted using LIFEx. LIFEx is a free-to-download radiomics package, developed by a French collaboration including CEA and INSERM. Its useful GUI makes it a useful tool for ROI definition, and the capability of scripting to run for multiple patient files make it very suitable for this study.

Separate studies should be performed with LIFEx vs other radiomics feature extractors. 

17 datasets were created here. A 3 minute acquisition and a 4 hour acquisition were taken, and the data reconstructed on the scanner and e7 tools. Various configurations of OSEM with/without ToF and resolution recovery (PSF) were performed on each.

The file `writeLifexPatients.py` writes the LIFEx script for all images to be included in the study.

The file `e7_validation_functions.py` stores some of the functions created in `e7_validation.ipynb` for easier use in subssequent iPython Notebooks. 

`e7_validation.ipynb` was my first attempt at the validation process. Using the initial dataset, I decided that my first attempts at creating realistic ROIs for the background and spheres of the NEMA phantom were inaccurate (I put this down to creating an ROI with 'free' voxels). This is then explored and examined in the further Notebooks.

George R Needham (GN)
University of Manchester & The Christie NHS Foundation Trust
