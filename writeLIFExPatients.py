#
#                             writeLIFExPatients.py
#
# - This program writes out the LIFEx script to extract features from a range of patients
#   alongside a log file which describes which images are which index.
#
#   LIFEx is a medical image viewer and feature-extraction software created by a French 
#   collaboration including CEA and INSERM. For more details and downloading, visit 
#       www.lifexsoft.org
#
#   EDIT - This program uses LIFEx v5.38 for the image unit conversion. For previous versions, 
#          please remove the "Session0" part from the 'patient'-writing loop, as well as the 
#          image units line (67 at time of writing) - GN  17-10-19
#   
#   INPUT FILES MUST BE IN DICOM FORMAT
#   (see LIFEx "TextureUserGuide.pdf" for details about LIFEx scripting procedure)
#
#                   George Needham, University of Manchester & The Christie NHS FT,  8/10/19


from glob import glob
import os

# This study name affects only the filenames of the output
studyName=input("\n\nPlease enter the name for this current study:\t")
print("\nCreating study \"{}.xls\"...\n".format(studyName))


# IMPORTANT
# 
# Here defines where you are pulling your DICOM folders from.
# Change this to get "allImgs" to contain all of the desired patients
prefix="/home/gn/SCANNER_DATA/GeNEMA_2Oct19/{}"
e7Imgs=glob(prefix.format("e7/*/"))
scannerImgs=glob(prefix.format("scanner/*/"))
allImgs = e7Imgs + scannerImgs

# Just a check to see if this is what you're looking for
print("\n\nYou are looking for directories in:\t{}".format(prefix))
print("\nFound the following files:")
for i in allImgs:
	print(i)


# LIFEx script will be a .txt file, drag and drop into the "Patient" window in LIFEx to run
of = open("patientList_{}.txt".format(studyName),"w")
print("\nWriting LIFEx patient script to \"patientList_{}.txt\"...".format(studyName))


# IMPORTANT
#
# This preamble contains the info required to read DICOM images into LIFEx as the same format
# Some of this might have to be changed at a later date
# Taken from p16 of "TextureUserGuide.pdf"
of.write("# start of file\n\n")

# BIN SIZE DESCRIPTION - this should be changed depending on the voxel values in your images.
# Note that this will depend also on base voxel units.
of.write("# Common\n")
of.write("\tLIFEx.texture.BinSize=0.25\n")         # describes width of bins in terms of base unit
of.write("\tLIFEx.texture.NbGrey=100.0\n")          # the number of gray levels 
of.write("\tLIFEx.texture.SessionCsv=/home/gn/data/{}.csv\n\n".format(studyName))

of,write("# Absolute\n"
of.write("\tLIFEx.texture.ButtonAbsolute=true\n")
of.write("\tLIFEx.texture.MinBound=0.0\n")          # define the absolute bounds of gray level definition
of.write("\tLIFEx.texture.MaxBound=25.0\n\n")

# More necessary stuff here - leave this as it is for now.
of.write("# RelativeMeanSd\n")
of.write("\tLIFEx.texture.ButtonRelativeMeanSd=false\n\n")
of.write("# RelativeMinMax\n")
of.write("\tLIFEx.texture.ButtonRelativeMinMax=false\n\n")
of.write("# DistanceWithNeighbours\n")
of.write("\tLIFEx.texture.GLCM.DistanceWithNeighbours=1\n\n")


# IMPORTANT
# 
# Not only here are we loading the images, we are also loading the ROIs defined in LIFEx which
# correspond to the regions of the Ge-68 NEMA phantom; BG (background) and C1-6 for the six 
# largest spheres in descending order.
patientNum = 0
for i in allImgs:
	of.write("# Patient {0}\n".format(patientNum))
	of.write("\tLIFEx.texture.Session0.Img{0}={1}\n".format(patientNum,i))
	of.write("\tLIFEx.texture.Session0.Img{0}.ZSpatialResampling=0\n".format(patientNum))
	of.write("\tLIFEx.texture.Session0.Img{0}.YSpatialResampling=0\n".format(patientNum))
	of.write("\tLIFEx.texture.Session0.Img{0}.XSpatialResampling=0\n".format(patientNum))
	of.write("\tLIFEx.texture.Session0.Img{0}.unitY=kBq/mL\n\n".format(patientNum)) # Converts to activity concentration (vs default SUV)
	patientNum += 1
of.write("\tLIFEx.texture.Session0.Roi0=/home/gn/ROIs/GeNEMA/LIFEx/BG.nii.gz\n")
of.write("\tLIFEx.texture.Session0.Roi1=/home/gn/ROIs/GeNEMA/LIFEx/C1.nii.gz\n")
of.write("\tLIFEx.texture.Session0.Roi2=/home/gn/ROIs/GeNEMA/LIFEx/C2.nii.gz\n")
of.write("\tLIFEx.texture.Session0.Roi3=/home/gn/ROIs/GeNEMA/LIFEx/C3.nii.gz\n")
of.write("\tLIFEx.texture.Session0.Roi4=/home/gn/ROIs/GeNEMA/LIFEx/C4.nii.gz\n")
of.write("\tLIFEx.texture.Session0.Roi5=/home/gn/ROIs/GeNEMA/LIFEx/C5.nii.gz\n")
of.write("\tLIFEx.texture.Session0.Roi6=/home/gn/ROIs/GeNEMA/LIFEx/C6.nii.gz\n\n")
of.write("\n# end of file")
of.close()
print("Finished writing LIFEx script!")

# For courtesy, output a .csv log file which gives the patient index alongside the root folder of 
# the DICOM images. This information could be taken from the .txt file, but this just makes it a 
# bit more explicit
print("\nNow just writing you a quick log file to say which patients are which. File written to \"patientListLog_{}.csv\"...".format(studyName))
logf = open("patientListLog_{}.csv".format(studyName),"w") 
logf.write("PatientNumber,Filepath\n")
patientNum=0
for i in allImgs:
	logf.write("{0},{1}\n".format(patientNum,i))
	patientNum+=1
logf.close()
print("Finished writing log file!")
print("\nClosing...")

# End of program
