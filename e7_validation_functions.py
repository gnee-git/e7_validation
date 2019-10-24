#
#                             e7_validation_functions.py
#
#   This program contains functions written for the purpose of validating e7_tools reconstruction
#   aginst the scanner's (Siemens Biograph mCT with TrueV) own reconstruction software.
#
#   Data is extracted from images in batches using "LIFEx" ( www.lifexsoft.org )
#   The data is stored in the LIFEx output folder under a "STUDY" subfolder; e.g. 
#
#   /LIFEx/output/root/
#                   |
#                   |
#                    ---> Ge-NEMA-phantom_study
#                                    |
#                                    |
#                                     ---> RoiValue
#                                             |
#                                             |
#                                              ----> outfile1.xls
#                                                    outfile2.xls
#                                                          :
#                                                          :
#                                                    patientListLog-studyname.csv
#
#   The "patientListLog...csv" comes from my own file "writeLIFExPatients.py", which I use to keep 
#   track of which scan is stored where and its associated parameters. I put this manually in the
#   RoiValue folder.
#
#   NB: For LIFEx v5.38, these .xls output files are instead saved as .csv - therefore making the
#       loading in of data a little more complex. To be dealt with next week  
#
#   The task of "import_e7val_data" is to:
#          -  import all .xls files as a list of pandas dataframes
#          -  output this list alongside a pandas dataframe version of the patientListLog
#      ** UPDATE 20/10/19 ** 
#          -  included ability to switch between .xls and .csv depending on datafile format   
#
#   "get_xydata" then creates:
#          - ylist; a list of non-string, non-zero features extracted by LIFEx
#          - xlist; a list of the maximum percentage difference between the e7- and 
#                   scanner-reconstructed images exhibited by each feature.
#                   (In the first dataset, the given value is the maximum between a
#                    3 minute and 4 hour acquisition)  
#
#   Read comments below for more info.
#
#                   George Needham, University of Manchester & The Christie NHS FT,  18/10/19



#
#   IMPORT PACKAGES HERE
#
from glob import glob
import os
import numpy as np
import pandas as pd



def import_e7val_data(dataPrefix,datafile_type="xls"):

    # Check for valid datafile format, default is .xls
    if datafile_type not in ["csv","xls"]:   # i.e. if format isn't accounted for, we raise error and exit
        raise NameError
    else:
        pass
        
    # Give the prefix for the folder, including "RoiValue" equivalent path
    if datafile_type == "xls":
        filepaths = sorted(glob(dataPrefix.format("*.xls")))
    elif datafile_type == "csv":
        filepaths = sorted(glob(dataPrefix.format("[!patientListLog]*.csv")))
    
    # Load up the log file into pandas dataframe
    logFile = glob(dataPrefix.format("patientListLog_*.csv"))[0]
    logFileDF = pd.read_csv(logFile)
    sLength = len(logFileDF["PatientNumber"])

    # Create new columns to make explicit some of the protocol features
    logFileDF["System"] = pd.Series(np.random.randn(sLength), index=logFileDF.index)      # -- either "e7" or "scanner" 
    logFileDF["TOF"] = pd.Series(np.random.randint(sLength), index=logFileDF.index)       # -- Binary 0/1 depending if TOF 
    logFileDF["PSF"] = pd.Series(np.random.randint(sLength), index=logFileDF.index)       #    or PSF enabled 
    logFileDF["ScanTime"] = pd.Series(np.random.randn(sLength), index=logFileDF.index)    # -- either 3mins/240mins (4 hrs)
    logFileDF["datapath"] = pd.Series(np.random.randint(sLength), index=logFileDF.index)  # -- path to .xls file

    # ....Now this is ugly, but this is the easiest way to operate multiple iterations through the dataframe without
    # compilcations around the changing string in "Filepath"
    for index,row in logFileDF.iterrows():
        logFileDF.loc[index,"Filepath"] = row["Filepath"].replace("/home/gn/SCANNER_DATA/GeNEMA_2Oct19/","")
    for index,row in logFileDF.iterrows():
        logFileDF.loc[index,"System"] = row["Filepath"].split("/")[0]
    for index,row in logFileDF.iterrows():
        logFileDF.loc[index,"Filepath"] = row["Filepath"].replace(row["Filepath"].split("/")[0],"")
    for index,row in logFileDF.iterrows():
        if "TOF" in logFileDF.loc[index,"Filepath"] or "ToF" in logFileDF.loc[index,"Filepath"]:
            logFileDF.loc[index,"TOF"] = 1
        else:
            logFileDF.loc[index,"TOF"] = 0
        if "PSF" in logFileDF.loc[index,"Filepath"]:
            logFileDF.loc[index,"PSF"] = 1
        else:
            logFileDF.loc[index,"PSF"] = 0
    for index,row in logFileDF.iterrows():
        if "-01-" in logFileDF.loc[index,"Filepath"] or "4hrs" in logFileDF.loc[index,"Filepath"] or " WB/" in logFileDF.loc[index,"Filepath"]:
            logFileDF.loc[index,"ScanTime"] = 240
        else:
            logFileDF.loc[index,"ScanTime"] = 3
    i=0
    for index,row in logFileDF.iterrows():
        logFileDF.loc[index,"datapath"] = filepaths[i]
        i+=1

    # Create a list of pandas dataframes, each consisting of a single patient's full extraction over all 7 ROIs
    dataDFList = []
    if datafile_type == "xls":
        for fp in filepaths:
            dataDFList.append(pd.read_excel(fp))
    elif datafile_type == "csv":
        for fp in filepaths:
            dataDFList.append(pd.read_csv(fp,skiprows=1))
    return dataDFList,logFileDF




    

def get_xydata(logFileDF,dataDFList,tof_flag=True,psf_flag=True,include_all_valid=True,scan_length=3.,calc_method="A"):

    # For pyradiomics, I'm not sure whether the small values in the "minimum" are artificialy 
    # inflating the "maxdiff" values. Therefore instead of doing the calculation with respect
    # to just the scanner value (method A), I have included the capability of doing so with 
    # respect to the mean of the scanner and e7 values (method B)
    def calcMethodA(e,s):
        return 100*(s-e)/s 
    def calcMethodB(e,s):
        return 200*(s-e)/(s+e)
    
    # so... "include_all_valid" is used as a Boolean switch to determine whether to use both 3 min and 4 hour
    # acquisitions in the data. If this is False, then it is required to set "scan_length" equal to the 
    # desired acquisition length. This is done in minutes as a float.

    titles = [c for c in dataDFList[0].columns]
    if tof_flag: 
        tof=1 
    else: 
        tof=0
    if psf_flag: 
        psf=1 
    else: 
        psf=0


    if include_all_valid: # use both 3min and 4hour acquisitions...
        maxdiff=[]
        names=[]
        for title in titles: # Loop over all possible features. This will include some non-desirables that we filter out at a later date
            e7subj = logFileDF.index[(logFileDF["ScanTime"] == 3.) & (logFileDF["TOF"] == tof) & (logFileDF["PSF"] == psf) & (logFileDF["System"] == "e7")].tolist()[0]
            scannersubj = logFileDF.index[(logFileDF["ScanTime"] == 3.) & (logFileDF["TOF"] == tof) & (logFileDF["PSF"] == psf) & (logFileDF["System"] == "scanner")].tolist()[0]
            e7data = dataDFList[e7subj][title].tolist()
            scannerdata = dataDFList[scannersubj][title].tolist()
            e7subj4h = logFileDF.index[(logFileDF["ScanTime"] == 240.) & (logFileDF["TOF"] == tof) & (logFileDF["PSF"] == psf) & (logFileDF["System"] == "e7")].tolist()[0]
            scannersubj4h = logFileDF.index[(logFileDF["ScanTime"] == 240.) & (logFileDF["TOF"] == tof) & (logFileDF["PSF"] == psf) & (logFileDF["System"] == "scanner")].tolist()[0]
            e7d4h = dataDFList[e7subj4h][title].tolist()
            scannerd4h = dataDFList[scannersubj4h][title].tolist()

            # Apply conditions; we only want the numerical features, which have to be non-zero in order to satisfy a
            # "percentage difference" calculation
            #
            # Note as well, the "params" features will be equal for every dataset, so their inclusion is superfluous here.
            if not all(isinstance(e,str) for e in  e7data+scannerdata+e7d4h+scannerd4h) and 0 not in scannerdata+scannerd4h and "PARAMS" not in title:
                y3m = []
                for i in range(0,len(e7data)):
                    if calc_method == "A":
                        y3m.append(calcMethodA(e7data[i],scannerdata[i]))
                    elif calc_method == "B":
                        y3m.append(calcMethodB(e7data[i],scannerdata[i]))
                y4h = []
                for i in range(0,len(e7d4h)):
                    y4h.append(100*(scannerd4h[i]-e7d4h[i])/scannerd4h[i])
                maxdiff.append(max([abs(y) for y in y3m+y4h]))
                names.append(title)
        return maxdiff,names

    else:  # IMPORTANT - REMEMBER TO SET "scan_length" FOR THIS BIT
        maxdiff = []
        names = []
        for title in titles:
            e7subj = logFileDF.index[(logFileDF["ScanTime"] == scan_length) & (logFileDF["TOF"] == tof) & (logFileDF["PSF"] == psf) & (logFileDF["System"] == "e7")].tolist()[0]
            scannersubj = logFileDF.index[(logFileDF["ScanTime"] == scan_length) & (logFileDF["TOF"] == tof) & (logFileDF["PSF"] == psf) & (logFileDF["System"] == "scanner")].tolist()[0]
            e7data = dataDFList[e7subj][title].tolist()
            scannerdata = dataDFList[scannersubj][title].tolist()

            if not all(isinstance(e,str) for e in  e7data+scannerdata) and 0 not in scannerdata and "PARAMS" not in title:
                y = []
                for i in range(0,len(e7data)):
                    if calc_method == "A":
                        y.append(calcMethodA(e7data[i],scannerdata[i]))
                    elif calc_method == "B":
                        y.append(calcMethodB(e7data[i],scannerdata[i]))
                maxdiff.append(max([abs(yi) for yi in y]))
                names.append(title)
        return maxdiff,names
