import numpy as np
import matplotlib.pyplot as plt
import discomb_utilities as disu

plot_layers = False
plot_lake = False
plot_diffs = False
burn_in_lakes = True
infile_dis = 'MODDANE5_rch_rjh1.dis'
infile_lak = 'MODDANE5_rch_rjh1bBEST.lak'

#
# Read in and handle the discritization file
#
indat = open(infile_dis,'r').readlines()

print 'Reading in the meta data'
DX,DY,NLAY,NROW,NCOL,i = disu.read_meta_data(indat)
[X,Y]=np.meshgrid(DX,DY)

print 'reading the model top and layer bottoms'
# Now read the Layer TOP and BOTTOMS
vertical_dis = np.zeros((NLAY+1,NROW,NCOL))
# now read the Model TOP
print 'reading model top'
TMP,i = disu.read_nrow_ncol_vals(indat,NROW,NCOL,np.float,i)
vertical_dis[0] = np.flipud(TMP)


# now read each of the other layers
for k in np.arange(NLAY):
    clay = k+1
    print 'reading bottom of layer --> %d ' %(clay)
    TMP,i = disu.read_nrow_ncol_vals(indat,NROW,NCOL,np.float,i)
    vertical_dis[k] = np.flipud(TMP)    

#
# Burn in the lake stages, if requested
#
if burn_in_lakes:
    indat = open(infile_lak,'r').readlines()
    # read in the stages
    tmp = indat.pop(0)
    nlakes = int(tmp.strip().split()[0])
    STAGES = []
    junkus = indat.pop(0)
    for i in np.arange(nlakes):
        tmp = indat.pop(0)
        STAGES.append(float(tmp.strip().split()[0]))
    # make a stages dictionary
    STAGES = dict(zip(np.arange(1,nlakes + 1),STAGES))
    
    # read in the LKARR array
    for i in np.arange(2):
        junkus = indat.pop(0)
    
    LKARR,i = disu.read_nrow_ncol_vals(indat,NROW,NCOL,np.int,0)
    LKARR = np.flipud(LKARR)
    if plot_lake:
        print 'Plotting the lake array'
        plt.figure()
        plt.pcolor(X,Y,LKARR)
        plt.title('Lake Array')
        plt.colorbar()
        plt.savefig('Lake Array.pdf')
        plt.close('all')
    else:
        print 'Lake array already plotted'
    
    # now for the burning in
    for i in np.arange(1,nlakes+1):
        inds = np.where(LKARR == i)
        vertical_dis[0][inds] = STAGES[i]
    
    
    
#
# Plot results
#

# first plot the model top
if plot_layers:
    print 'Plotting the model top'
    plt.figure()
    plt.pcolor(X,Y,vertical_dis[0])
    plt.title('Model top')
    plt.colorbar()
    plt.savefig('Model_top.pdf')
    plt.close('all')
else:
    print 'Model top already plotted'

# plot each layer
if plot_layers:
    for clay in np.arange(NLAY):
        print 'Plotting layer %d' %(clay + 1)
        plt.figure()
        plt.pcolor(X,Y,vertical_dis[clay+1])
        plt.colorbar()
        plt.title('Model layer %d' %(clay+1))
        plt.savefig('Model_layer_%d.pdf' %(clay+1))   
        plt.close('all')
else:
    print 'Layer bottoms already plotted'

# look at the subtractions of each and plot overlap
print 'Looking at the subtractions for overlap'
for clay1 in np.arange(NLAY):
    for clay2 in np.arange(clay1):
        print 'evaluating layer %d - %d' %(clay1,clay2)
        currdiff = vertical_dis[clay1] - vertical_dis[clay2]
        print 'max diff ==> %f' %(np.max(currdiff))
        if np.max(currdiff) >= 0:
            # first print out the overlapping cells
            ofp = open('overlap_between_L%d_and_L%d.dat' %(clay1,clay2),'w')
            ofp.write('row  col\n')
            inds = np.where(np.flipud(currdiff)>=0)
            for cind in np.arange(len(inds[0])):
                ofp.write('%d   %d\n' %(inds[0][cind],inds[1][cind]))
            ofp.close()
            currdiff[currdiff<=0] = 0
            plt.figure()
            if plot_diffs:
                print 'plotting first difference'
                plt.pcolor(X,Y,currdiff)
                plt.colorbar()
                plt.title('Diff between Layers %d and %d' %(clay1, clay2))
                plt.savefig('Diff_%d_%d.pdf' %(clay1, clay2))
                plt.close('all')
   