

import rasterio
import matplotlib.pyplot as plt
import numpy as np
import os, glob

def load_specific(col):
    NDVIS = []
    for filename in glob.glob('adilabad tiff\\*.tif'):
       if(col not in filename):
           continue
       with rasterio.open(os.path.join(os.getcwd(), filename), 'r') as image:
           image_array = image.read(1)
           NDVIS.append(image_array)
           
    sample = NDVIS[0]
    stackedNDVI = np.zeros((len(NDVIS),NDVIS[0].shape[0],NDVIS[0].shape[1]))
    for n in range(len(NDVIS)):
        stackedNDVI[n,:,:] = NDVIS[n]
       
    pixels = []
    positions = []
    for i in range(len(sample)):
        for j in range(len(sample[i])):
            if(sample[i][j]==-3000):
                continue
            pixelhistory = stackedNDVI[:,i,j]
            pixels.append(pixelhistory)
            positions.append((i,j))
    return pixels,NDVIS,positions



       
       
       

       