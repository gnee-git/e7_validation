# e7_validation
A repository to store all codes used to validate e7_tools image reconstruction against the Siemens online reconstruction software. The data is collected from a Ge-68 doped plastic NEMA IQ phantom.

*The following intro is copied from the first e7_validation iPython Notebook...*

## Extracting the data...

The data, taken from the scanner, was reconstructed on both the scanner's version of software and the "e7" software, run offline on a PC in the University of Manchester's Nuclear Physics Lab. 

From here, data was extracted using LIFEx. LIFEx is a free-to-download radiomics package, developed by a French collaboration including CEA and INSERM. Its useful GUI makes it a useful tool for ROI definition, and the capability of scripting to run for multiple patient files make it very suitable for this study. LIFEx v5.10 is available on their website, however v5.38 was used here.

Separate studies should be performed with LIFEx vs other radiomics feature extractors. 

17 datasets were created here. A 3 minute acquisition and a 4 hour acquisition were taken, and the data reconstructed on the scanner and e7 tools. Various configurations of OSEM with/without ToF and resolution recovery (PSF) were performed on each.

7 ROIs were created in LIFEx - one for the NEMA phantom background, and 6 for the 6 largest spheres. LIFEx extracts simulateously every feature (conventional, histogram, shape, GLCM, GLRLM, NGLDM & GLZLM - see https://www.lifexsoft.org/ resources for more details, or alternatively https://pyradiomics.readthedocs.io/en/latest/ ) for each ROI in each image. 

The comparison was initially attempted by working out a "maximum percentage difference" between metrics in the e7-reconstructed and the scanner-reconstructed images; *the maximum value of e.g. 100 x (val(scanner) - val(e7))/val(scanner) across all ROIs as taken from images equivalently reconstructed using each system*.

The file `writeLifexPatients.py` writes the LIFEx script for all images to be included in the study.

The file `e7_validation_functions.py` stores some of the functions created in `e7_validation.ipynb` for easier use in subssequent iPython Notebooks (starting with Pt III).

`e7_validation_pt1.ipynb` was my first attempt at the validation process, started on 11th October 2019. Using the initial dataset, I decided that my first attempts at creating realistic ROIs for the background and spheres of the NEMA phantom were inaccurate (I put this down to creating an ROI with 'free' voxels).

`e7_validation_pt2.ipynb` is the second notebook, started on 15th October 2019. Here I work with carefully redefined ROIs, and also redefine the gray level bins in the LIFEx script. I explore the impact of these changes to the previous data. New plots show the expected changes well, with the largest maximum percentage differences over all ROIs of around 2% in some texture matrix metrics.

`e7_validation_pt3.ipynb` is the third notebook, started on 18th October 2019. Here I switch from using SUV as the base image unit, to using kBq/ml - a feature enabled in scripting for LIFEx v5.38 that isn't possible in earlier versions. Further analysis, such as including **pyradiomics** alongside LIFEx, is considered.


George R Needham (GN)
University of Manchester & The Christie NHS Foundation Trust
