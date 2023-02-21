

import matplotlib.pyplot as plt
import numpy as np
from load import load_specific
import seaborn as sns

pixels,NDVIS,positions = load_specific("NDVI")
pixels_NDVI,NDVIS,positions = load_specific("NDVI")
pixels_EVI,EVIS,E_positions = load_specific("EVI")
pixels_VI,NDVIS,V_positions = load_specific("_VI_")

"ONE Time step Visualizations across region - use NDVIS"

"1. Show the region for 1 timestep."
sample = NDVIS[12]
wool = sample[0][0]
for i in range(len(sample)):
    for j in range(len(sample[0])):
        if(sample[i][j]==wool):
            sample[i][j] = 0
plt.figure(1)
plt.imshow(sample)
plt.title("Adilabad region for 1 timestep")


"2. ONE Pixel Visualizations across time- Use pixlels"
sample = pixels[60]
plt.figure(2)
plt.plot(sample)
plt.grid()
plt.xlabel("Time")
plt.ylabel("NDVI")
plt.title("NDVI Timeseries for a sample region")

"3. NDVI overtime for different regions"
s1,s2,s3 = pixels[10],pixels[34],pixels[112]
plt.figure(3)
plt.plot(s1)
plt.plot(s2)
plt.plot(s3)
plt.grid()
plt.xlabel("Time")
plt.ylabel("NDVI")
plt.title("NDVI Timeseries for a 3 regions")



"4. NDVI, VI, EVI for 1 region"
s1 = pixels_NDVI[44]
s2 = pixels_EVI[44]
s3 = pixels_VI[44]
plt.figure(4)
plt.plot(s1)
plt.plot(s2)
plt.plot(s3)
plt.grid()
plt.legend(['NDVI','EVI','VI'])
plt.xlabel("Time")
plt.ylabel("Index")
plt.title("NDVI, VI, EVI for 1 region")







       
       

       