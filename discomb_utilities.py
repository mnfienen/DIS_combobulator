import numpy as np

def read_nrow_ncol_vals(indat,NROW,NCOL,DTYPE,i):
    # read in NROW * NCOL values from a file read into indat
    # Returns TMP - a np array of type DTYPE
    # i is a counter that was already set as the file is parsed
    # i is returned as well to keep the party rockin'
    ncells = NROW*NCOL
    contflag = True
    TMP = []    
    for i in np.arange(i,len(indat)):
        if contflag == False:
            break
        if len(TMP) < ncells:
            TMP.extend(indat[i].strip().split())
        else:
            contflag = False
    TMP = np.array(TMP,dtype=DTYPE).reshape(NROW,NCOL)    
    return TMP, i

def read_meta_data(indat):
    DX = []
    DY = []    
    # remove the comment lines from the top of the file
    contflag = True
    while contflag:
        if '#' in indat[0]:
            junkus = indat.pop(0)
        else:
            contflag = False
            
    # get the control (uber) parameters
    tmp = indat.pop(0).strip().split()
    NLAY = int(tmp.pop(0))
    NROW = int(tmp.pop(0))
    NCOL = int(tmp.pop(0))
    
    # skip the next two control lines
    for i in np.arange(2):
        junkus = indat.pop(0)
    
    # now read the DX values
    contflag = True
    for i in np.arange(len(indat)):
        if contflag == False:
            break
        if len(DX) < NCOL:
            DX.extend(indat[i].strip().split())
        else:
            contflag = False
    DX = np.array(DX,dtype=float)
    
    # now read the DY values
    contflag = True
    for i in np.arange(i,len(indat)):
        if contflag == False:
            break
        if len(DY) < NROW:
            DY.extend(indat[i].strip().split())
        else:
            contflag = False
    DY = np.array(DY,dtype=float)
    
    # adjust DX and DY for pcolor plotting
    DX = np.hstack([0.5*DX[0],DX])
    DY = np.hstack([0.5*DY[0],DY])
    DX = np.cumsum(DX)
    DY = np.cumsum(DY)    
    return DX,DY,NLAY,NROW,NCOL,i