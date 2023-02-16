# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 00:26:27 2023

@author: kashy
"""

from preprocess import preprocess
import numpy as np
import matplotlib.pyplot as plt
from  scipy.fft import fft


from  hmmlearn import  hmm

pixels = preprocess()

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

def plotmergepixels():
    plt.figure(3)
    plt.plot(pixels[3])
    plt.plot(pixels[4])
    plt.plot(mergepixels(pixels[3:5]))
    plt.legend(['pixel1','pixel2','merged'])
    plt.show()
                
            
        
    

def fourier_transform(pixelhistory,i=0,plot = False):
    new = fft(pixelhistory)
    
    if(plot):
        plt.figure(i)
        plt.plot(pixelhistory)
        
        plt.plot(new)
        plt.show()
    return new

def runhmm(pixelhistory):
    X = pixelhistory.reshape(-1,1)
    model = hmm.GaussianHMM(n_components = 3, covariance_type = "diag", n_iter = 50)    
    model.fit(X)
    return model
    

def fithmm(pixelhistory,X, mincomp=1,maxcomp = 10):
    scores = []
    models = []
    for i in range(mincomp , maxcomp+1):
        model = hmm.GaussianHMM(n_components = i, covariance_type = "full", n_iter = 50)  
        model.fit(X)
        models.append(model)
        scores.append(model.score(X))
        
    best = model[np.argmax(scores)]
    n_states = best.n_components
    print(f'The best model had a score of {max(scores)} and {n_states} ''states')
    # use the Viterbi algorithm to predict the most likely sequence of states
    # given the model
    states = model.predict(X)
    return best, states
        
    
model = runhmm(pixels[5])

transformed = fourier_transform(pixels[3],plot=False)

double_transformed = fourier_transform(transformed[1:],plot=True)



### ALGORITHM
'''
Human permeation into forests by outlier detection. 
Track outliers and the time they changed to an outlier state. 
So, for every pixel, have a HMM which can give information about when it can tuyrn into an outlier. 
Maybe the states are normal, outlier and hidden are 'recent' ndvi values. 

another way of HMM is just have the transition states, and any deviation in behaviour can be called an outlier. 

So, first, gather HMM for every pixel, and note down the values. 
Plot the values for a better understanding. 
Recognize outliers. 
-----------------
Now, you will have an outer algorithm that is iterating for every pixel. 
There should also be a function that creates this data for bigger areas by averaging pixel values.
'''

    