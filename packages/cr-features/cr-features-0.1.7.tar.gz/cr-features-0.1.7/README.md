# Calculating features

## Usage
- Install the library with:
  ```cmd
  pip install build
  python -m build
  ```
  
  Alternative:
  ```cmd
  pip install pep517
  python -m pep517.build .
  ```

- Basic usage is: 

```python
from cr_features.helper_functions import empatica1d_to_array, convert_to2d, frequency_features, hrv_features, gsr_features
from cr_features.calculate_features import calculate_features
import pandas as pd

pathToHrvCsv = "example_data/S2_E4_Data/BVP.csv"
windowLength = 500

# get an array of values from HRV empatica file
hrv_data, startTimeStamp, sampleRate = empatica1d_to_array(pathToHrvCsv)

# Convert the HRV data into 2D array
hrv_data_2D = convert_to2d(hrv_data, windowLength)

# Create a list with feature names
featureNames = []
featureNames.extend(hrv_features)
featureNames.extend(frequency_features)

pd.set_option('display.max_columns', None)
 
# Calculate features
calculatedFeatures = calculate_features(hrv_data_2D, fs=int(sampleRate), feature_names=featureNames)
```
- More usage examples are located in [usage_examples.ipynb](usage_examples.ipynb) file

## Features
- Features are returned (from calculateFeatures() function) in a Pandas DataFrame object.
- In the case if a feature couldn't be calculated (for example, if input signal is invalid), NaN value is returned.
- Further in this section, the list with descriptions of all possible features is presented. 

### GSR features:
These features are useful for 1D GSR(EDA) signals
- `mean`: mean of the signal
- `std`: standard deviation of signal
- `q25`: 0.25 quantile
- `q75`: 0.75 quantile
- `qd`: q75 - q25
- `deriv`: sum of gradients of the signal
- `power`:  power of the signal (mean of squared signal)
- `numPeaks`: number of EDA peaks
- `ratePeaks`: average number of peaks per second
- `powerPeaks`: power of peaks (mean of signal at indexes of peaks)
- `sumPosDeriv`: sum of positive derivatives divided by number of all derivatives
- `propPosDeriv`: proportion of positive derivatives per all derivatives
- `derivTonic`: sum of gradients of the tonic
- `sigTonicDifference`: mean of tonic subtracted from signal
- `freqFeats`: 
- `maxPeakAmplitudeChangeBefore`: maximum peak amplitude change before peak
- `maxPeakAmplitudeChangeAfter`: maximum peak amplitude change after peak
- `avgPeakAmplitudeChangeBefore`: average peak amplitude change before peak
- `avgPeakAmplitudeChangeAfter`: average peak amplitude change after peak
- `avgPeakChangeRatio`: avg_peak_increase_time / avg_peak_decrease_time
- `maxPeakIncreaseTime`: maximum peak increase time
- `maxPeakDecreaseTime`: maximum peak decrease time
- `maxPeakDuration`: maximum peak duration
- `maxPeakChangeRatio`: max_peak_increase_time / max_peak_decrease_time
- `avgPeakIncreaseTime`: average peak increase time
- `avgPeakDecreaseTime`: average peak decreade time
- `avgPeakDuration`: average peak duration
- `maxPeakResponseSlopeBefore`: maximum peak response slope before peak
- `maxPeakResponseSlopeAfter`: maximum peak response slope after peak
- `signalOverallChange`: maximum difference between samples (max(sig)-min(sig))
- `changeDuration`: duration between maximum and minimum values
- `changeRate`: change_duration / signal_overall_change
- `significantIncrease`:
- `significantDecrease`:

### HRV features:
These features are useful for 1D HRV(BVP) signals.

If number of RR intervals (numRR) is less than `length of sample / (2 * sampling rate)` (30 BPM) or greater than `length of sample / (sampling rate / 4)` (240 BPM), BPM value is incorrect and thus, all other HRV features are set to NaN.

- `meanHr`: mean heart rate
- `ibi`: mean interbeat interval
- `sdnn`: standard deviation of the ibi
- `sdsd`: standard deviation of the differences between all subsequent R-R intervals
- `rmssd`: root of the mean of the list of squared differences
- `pnn20`: the proportion of NN20 intervals to all intervals
- `pnn50`: the proportion of NN50 intervals to all intervals
- `sd`:
- `sd2`:
- `sd1/sd2`: sd / sd2 ratio
- `numRR`: number of RR intervals

### Accelerometer features:
These features are useful for 3D signals from accelerometer
- `meanLow`: mean of low-pass filtered signal
- `areaLow`: area under the low-pass filtered signal
- `totalAbsoluteAreaBand`: sum of absolute areas under the band-pass filtered x, y and z signal
- `totalMagnitudeBand`: square root of sum of squared band-pass filtered x, y and z components
- `entropyBand`: entropy of band-pass filtered signal
- `skewnessBand`: skewness of band-pass filtered signal
- `kurtosisBand`: kurtosis of band-pass filtered signal
- `postureDistanceLow`: calculates difference between mean values for a given sensor (low-pass filtered)
- `absoluteMeanBand`: mean of band-pass filtered signal
- `absoluteAreaBand`: area under the band-pass filtered signal
- `quartilesBand`: quartiles of band-pass filtered signal
- `interQuartileRangeBand`: inter quartile range of band-pass filtered signal
- `varianceBand`: variance of band-pass filtered signal
- `coefficientOfVariationBand`: dispersion of band-pass filtered signal
- `amplitudeBand`: difference between maximum and minimum sample of band-pass filtered signal
- `totalEnergyBand`: total magnitude of band-pass filtered signal
- `dominantFrequencyEnergyBand`: ratio of energy in dominant frequency
- `meanCrossingRateBand`: the number of signal crossings with mean of band-pass filtered signal
- `correlationBand`: Pearson's correlation between band-pass filtered axis
- `quartilesMagnitudesBand`: quartiles at 25%, 50% and 75% per band-pass filtered signal
- `interQuartileRangeMagnitudesBand`: interquartile range of band-pass filtered signal
- `areaUnderAccelerationMagnitude`: area under acceleration magnitude
- `peaksDataLow`: number of peaks, sum of peak values, peak avg, amplitude avg
- `sumPerComponentBand`: sum per component of band-pass filtered signal
- `velocityBand`: velocity of the band-pass filtered signal
- `meanKineticEnergyBand`: mean kinetic energy 1/2*mV^2 of band-pass filtered signal
- `totalKineticEnergyBand`: total kinetic energy 1/2*mV^2 for all axes (band-pass filtered)
- `squareSumOfComponent`: squared sum of component
- `sumOfSquareComponents`: sum of squared components
- `averageVectorLength`: mean of magnitude vector
- `averageVectorLengthPower`: square mean of magnitude vector
- `rollAvgLow`: maximum difference of low-pass filtered roll samples
- `pitchAvgLow`: maximum difference of low-pass filtered pitch samples
- `rollStdDevLow`: standard deviation of roll (calculated from low-pass filtered signal)
- `pitchStdDevLow`: standard deviation of pitch (calculated from low-pass filtered signal)
- `rollMotionAmountLow`: amount of wrist roll (from low-pass filtered signal) motion
- `rollMotionRegularityLow`: regularity of wrist roll motion
- `manipulationLow`: manipulation of low-pass filtered signals
- `rollPeaks`: number of roll peaks, sum of roll peak values, roll peak avg, roll amplitude avg
- `pitchPeaks`: number of pitch peaks, sum of pitch peak values, pitch peak avg, pitch amplitude avg
- `rollPitchCorrelation`: correlation between roll and peak (obtained from low-pass filtered signal)

### Gyroscope features:
These features are useful for 3D signals from gyroscope
- `meanLow`: mean of low-pass filtered signal
- `areaLow`: area under the low-pass filtered signal
- `totalAbsoluteAreaLow`: sum of absolute areas under the low-pass filtered x, y and z signal
- `totalMagnitudeLow`: square root of sum of squared band-pass filtered x, y and z components
- `entropyLow`: entropy of low-pass filtered signal
- `skewnessLow`: skewness of low-pass filtered signal
- `kurtosisLow`: kurtosis of low-pass filtered signal
- `quartilesLow`: quartiles of low-pass filtered signal
- `interQuartileRangeLow`: inter quartile range of low-pass filtered signal
- `varianceLow`: variance of low-pass filtered signal
- `coefficientOfVariationLow`: dispersion of low-pass filtered signal
- `amplitudeLow`: difference between maximum and minimum sample of low-pass filtered signal
- `totalEnergyLow`: total magnitude of low-pass filtered signal
- `dominantFrequencyEnergyLow`: ratio of energy in dominant frequency
- `meanCrossingRateLow`: the number of signal crossings with mean of low-pass filtered signal
- `correlationLow`: Pearson's correlation between low-pass filtered axis
- `quartilesMagnitudeLow`: quartiles at 25%, 50% and 75% per low-pass filtered signal
- `interQuartileRangeMagnitudesLow`: interquartile range of band-pass filtered signal
- `areaUnderMagnitude`: area under magnitude
- `peaksCountLow`: number of peaks in low-pass filtered signal
- `averageVectorLengthLow`: mean of low-pass filtered magnitude vector
- `averageVectorLengthPowerLow`: square mean of low-pass filtered magnitude vector
                         
                    
### Generic features:
These are generic features, useful for many different types of signals
- `autocorrelations`: autocorrelations of the given signal with lags 5, 10, 20, 30, 50, 75 and 100
- `countAboveMean`: number of values in signal that are higher than the mean of signal
- `countBelowMean`: number of values in signal that are lower than the mean of signal
- `maximum`: maximum value of the signal
- `minimum`: minimum value of the signal
- `meanAbsChange`: the mean of absolute differences between subsequent time series values
- `longestStrikeAboveMean`: longest part of signal above mean
- `longestStrikeBelowMean`: longest part of signal below mean
- `stdDev`: standard deviation of the signal
- `median`: median of the signal
- `meanChange`: the mean over the differences between subsequent time series values
- `numberOfZeroCrossings`: number of crossings of signal on 0
- `absEnergy`: the absolute energy of the time series which is the sum over the squared values
- `linearTrendSlope`: a linear least-squares regression for the values of the time series versus the sequence from 0 to length of the time series minus one
- `ratioBeyondRSigma`: ratio of values that are more than r*std(x) (so r sigma) away from the mean of signal. r in this case is 2.5
- `binnedEntropy`: entropy of binned values
- `numOfPeaksAutocorr`: number of peaks of autocorrelations
- `numberOfZeroCrossingsAutocorr`: number of crossings of autocorrelations on 0
- `areaAutocorr`: area under autocorrelations
- `calcMeanCrossingRateAutocorr`: the number of autocorrelation crossings with mean
- `countAboveMeanAutocorr`: umber of values in signal that are higher than the mean of autocorrelation
- `sumPer`: sum per component
- `sumSquared`: squared sum per component
- `squareSumOfComponent`: square sum of component
- `sumOfSquareComponents`:sum of square components
                       
### Frequency features:
These are frequency features, useful for many different types of signals. The signal is converted to power spectral density signal and features are calculated on this signal
- `fqHighestPeakFreqs`: three frequencies corresponding to the largest peaks added to features
- `fqHighestPeaks`: three largest peaks added to features
- `fqEnergyFeat`: energy calculated as the sum of the squared FFT component magnitudes, and normalized
- `fqEntropyFeat`: entropy of the FFT of the signal
- `fqHistogramBins`: Binned distribution (histogram)
- `fqAbsMean`: absolute mean of the raw signal
- `fqSkewness`: skewness of the power spectrum of the data
- `fqKurtosis`: kurtosis of the power spectrum of the data
- `fqInterquart`: inter quartile range of the raw signal

## Contributors

Several people contributed to making this library, both to its implemenetation and feature design: Vito Janko, Matjaž Bostič, Gašper Slapničar, Junoš Lukan, Nina Reščič, Simon Stankoski, Boža Cvetković, Mitja Luštrek