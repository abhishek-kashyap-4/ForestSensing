# Outlier Prediction for Land cover change

## Part 1 - Data Collection
Data was primarily extracted from MODIS Application for Extracting and Exploring Analysis Ready Samples (AρρEEARS). This Dataset with pre-computed NDVI, EVI values was used as a baseline for developing the models. 
Data with better spatial resolution was later extracted from GEE. Currently, I am preprocessing this data to fit the models.


A sample of 125 regions with 500m resolution was used with the following bands:

1. Normalized Difference Vegetation Index (NDVI)
2. Enhanced Vegetation Index (EVI)
3. Date of Year
4. MIR, NIR reflectance

## Part 2 - Data Visualization:

The NDVI values of the sample region for a specific timestep look like this:

![sample_NDVI__adilabad.png](plots/sample_NDVI__adilabad.png)

Each region in the Image is associated with a history of values.  The 3 historic values for a sample region look like this:

![ndvi_evi_vi.png](plots/ndvi_evi_vi.png)

I ignored the VI values because of the obvious spikes in the data. 

Each "Normal" region in the locality can be expected to have the same seasonality:

![ndvithrice.png](plots/ndvithrice.png)

The histogram for NDVI, EVI and VI: 

![NDVI_EVI_VI](plots/ndvi_evi_vi_hist.png)


## Part 3 - Models
### Part 3.1 - Hidden Markov Models

A hidden Markov model (HMM) is a statistical model that can be used to describe the time series of observable events that depend on hidden factors. They are powerful models which can describe the probability distributions of "Hidden States" based on the observations. 
3 Important Algorithms in HMM:
1. Forward Algorithm
2. HMM training with Expectation-Maximization: Baum–Welch algorithm
3. Maximum a posteriori estimate: viterbi (Dynamic Programming)

![HMM](hmm.png)

For our purposes, HMM can be used to differentiate between "Normal" regions and regions with outlier behaviour. a Gaussian HMM is the most applicable for our scenario, as the change of NDVI(or EVI) is expected to have a mean and a variance roughly following a Gaussian Distribution.

I created a HMM that can model the behaviour of NDVI (or EVI) changing overtime with a hope that outliers will have a different distribution compared to normal regions.  For this, we need to extract "change" over NDVI (or EVI) values. 

Visualizing NDVI change overtime for a sample region:

![ndvi change.pngs](plots/ndvi_change.png)

Fitting the regions to HMM without explicitly controlling the number of hidden states could give intuitive, but unusable results. For example, consider the opimum number of hidden states for a sample region below:

![Markov Hidden States](plots/Hidden_states.png)

Every region would fit to a different number of hidden states because of inherent noise. However, this can be addressed with smoothing the data, or getting better data.











