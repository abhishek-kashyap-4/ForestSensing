# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 00:26:27 2023

@author: kashy
"""

from load import load_specific
import numpy as np
import matplotlib.pyplot as plt
from  scipy.fft import fft
import os
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
import helpers
import seaborn as sns
os.environ["OMP_NUM_THREADS"] = '1'

from  hmmlearn import  hmm

pixels,NDVIS,positions = load_specific("NDVI") 
#NDVIS is a list of the area at each timestep. use -3000 for non existant values.
#positions is a list of a pixel's i,j in ndvi.
    
def smooth(ss):
    plt.plot(ss)
    model = SimpleExpSmoothing(ss)
    mf = model.fit()
    res = [mf.forecast(s)[0] for s in ss]
    plt.plot(res)
    plt.legend(['orig','smooth'])
    
#smooth(pixels[3])    
    
def mergepixels(pixelssublist):
    '''
    NAIVE implementation
    input: list of pixel histories. 
    output mega pixel history
    '''
    mega = np.zeros(len(pixelssublist[0]))
    for pixels in pixelssublist:
        for i in range(len(pixels)):
            mega[i] += pixels[i]
    for i in range(len(mega)):
        mega[i] /= len(pixelssublist)
    return mega

                          
        
def getpixelchanges(ph): #ph stands for pixel history
    ph = ph[0] + ph + ph[-1]
    phc = []
    for i in range(len(ph)-1):
        phc.append(ph[i]-ph[i+1])
        
    return phc
plt.subplot(2,1,1)
plt.plot(pixels[3])
plt.subplot(2,1,2)
plt.plot(getpixelchanges(pixels[3]))
plt.show()

pixelchanges = [getpixelchanges(ph) for ph in pixels]

def fithmm(pixelhistory, mincomp=1,maxcomp = 10):
    scores = []
    models = []
    X = np.array(pixelhistory).reshape(-1,1)
    for i in range(mincomp , maxcomp+1):
        model = hmm.GaussianHMM(n_components = i, covariance_type = "full", n_iter = 50)  
        model.fit(X)
        models.append(model)
        scores.append(model.score(X))
        
    best = models[np.argmax(scores)]
    n_states = best.n_components
    print(f'The best model had a score of {max(scores)} and {n_states} ''states')
    # use the Viterbi algorithm to predict the most likely sequence of states
    # given the model
    states = model.predict(X)
    return best, states

sample = pixels[63]
best , states = fithmm(getpixelchanges(sample),1,3)
plt.figure(figsize = (15, 10))
plt.plot(sample)
b=1
n = len(np.unique(states))
for i in np.unique(states):
    #x = pixels[7][states==i].astype(int)
    x = [j for j in range(len(states)) if states[j]==i]
    y = [sample[j] for j in x]
    plt.subplot(n,1,b)
    b+=1
    plt.plot(sample)
    plt.plot(x,y,'x')
plt.legend(np.unique(states), fontsize=16)
plt.grid(True)
plt.xlabel("datetime", fontsize=16)
plt.ylabel("NDVI ", fontsize=16)  


" Visualize means and variance of the region"
means = []
covars = []

for i in  range(len(pixels)):
    pixelhistory = pixels[i]
    pixelchangehistory = pixelchanges[i]
    best, states = fithmm(pixelchangehistory,3,3)
    mean = best.means_.copy()
    covar = best.covars_.copy()#length is number of hidden states
    meannew , covarnew = zip(*sorted(zip(mean, covar)))
    means.append([f[0] for f in meannew])
    covars.append([f[0] for f in covarnew])
    

#assume states are 3 here
n = len(means)
NDVIS_means0 = NDVIS[0].copy() 
NDVIS_means1 = NDVIS[0].copy() 
NDVIS_means2 = NDVIS[0].copy() 
NDVIS_means3 = NDVIS[0].copy() 
assert len(means) == len(positions)
for i in range(n):
    pos = positions[i]
    NDVIS_means0[pos[0] ][ pos[1]] = means[i][0]
    NDVIS_means1[pos[0] ][ pos[1]] = means[i][1]
    NDVIS_means2[pos[0] ][ pos[1]] = means[i][2]
    NDVIS_means3[pos[0] ][ pos[1]] = (means[i][0]+means[i][1]+means[i][2])/3
m = len(NDVIS_means0)

fig, ((ax1, ax2), (ax3,ax4)) = plt.subplots(nrows = 2, ncols=2)
fig.subplots_adjust(wspace=0.08)


sns.heatmap(NDVIS_means0,ax=ax1)
ax1.set_title("Decreasing NDVI")
sns.heatmap(NDVIS_means1,ax=ax2) 
ax2.set_title("Constant NDVI")
sns.heatmap(NDVIS_means2,ax=ax3)  
ax3.set_title("Increasing NDVI")
sns.heatmap(NDVIS_means3,ax=ax4)  
ax4.set_title("mean NDVI")

    
    

    

    



### ALGORITHM
'''
Human permeation into forests by outlier detection. 
Track outliers and the time they changed to an outlier state. 
So, for every pixel, have a HMM which can give information about when it can tuyrn into an outlier. 
Maybe the states are normal, outlier and hidden are 'recent' ndvi values. 

another way of HMM is just have the transition states, and any deviation in behaviour can be called an outlier. 
this behaviour is found by transition matrix

So, first, gather HMM for every pixel, and note down the values. 
Plot the values for a better understanding. 
Recognize outliers. 
-----------------
Now, you will have an outer algorithm that is iterating for every pixel. 
There should also be a function that creates this data for bigger areas by averaging pixel values.
'''

'''
OUTLIER DETECTION
def accordance(areamodel, samplemodel):
    if samplemodel 'like' area model, it isn't an outlier
    
area = mergepixels(pixels)
areamodel , areastates = fithmm(area)
for pixelhistory in  pixels:
    best, states = fithmm(pixelhistory)
    accordance(areamodel,best)
    
    
OUTLIER ANALYSIS
Given an outlier history and the model, 
find out the point of deviation with veterbi




'''
def plot_outliers(outlier_mask,fig = 16):
    '''
    Use positions for the actual positions.
    Outlier mask will have the same positions as the pixels list. 
    
    '''
    maskedNDVI = NDVIS[-1].copy()
    for i in range(len(outlier_mask)):
        if(outlier_mask[i]):
            m,n = positions[i]
            print(maskedNDVI[m][n])
            maskedNDVI[m][n] = 500
    plt.figure(fig)
    plt.imshow(maskedNDVI)
    plt.title("Time Invariant outliers")
    
    
            
def accordance(areamodel, samplemodel):
    '''if samplemodel 'like' area model, it isn't an outlier'''
    return False
    
    
def outlier_detection(pixels):
    area = mergepixels(pixels)
    areamodel , areastates = fithmm(area)
    bests = []
    beststates = []
    outlier_mask = []
    for i in  range(len(pixels)):
        pixelhistory = pixels[i]
        pixelchangehistory = pixelchanges[i]
        best, states = fithmm(pixelchangehistory)
        bests.append(best)
        beststates.append(states)
        is_outlier = accordance(areamodel,best)
        if(is_outlier):
            print("Found an outlier: pixels{i}")
            outlier_mask.append(True)
        else:
            outlier_mask.append(True)
    return bests , beststates , outlier_mask

#bests , beststates , outlier_mask = outlier_detection(pixels)

#outlier_mask  = [True] *(len(pixels)//2) +[False]*(len(pixels)//2)
#plot_outliers(outlier_mask)
        



    